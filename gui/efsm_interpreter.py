import argparse
import copy
import json
import logging
import re

from config import TEMPLATE_CONDITION, META, OPERATIONS, TEMPLATE_ACTION, \
    TEMPLATE_PACKET_ACTION, CONDITIONS, TEMPLATE_SET_DEFAULT_condition_table, REGISTERS, \
    TEMPLATE_SET_DEFAULT_EFSMTable, TEMPLATE_SET_PACKET_ACTIONS, DEFAULT_PRIO_EFSM, EQUAL, \
    MAX_CONDITIONS_NUM, MAX_REG_ACTIONS_PER_TRANSITION, REG_ACTION_REGEX, COND_REGEX, \
    FDV_BASE_REGISTER, GDV_BASE_REGISTER, PKT_ACTION_REGEX

logger = logging.getLogger(__name__)


# REMEMBER: CONDITIONS MUST BE ORDERED!!!!!!

# TODO:
#  - divide parse function in subfunction to ease testing
#  - add unit testing
#  - add PTF/testvector output
# Edges information:
#  - Matches
#  - Conditions
#  - Register update
#  - Actions
# --> MATCHES|CONDITIONS|REG_UPDATE|ACTIONS
# ipv4.srcAddr==10.0.0.1;ipv4.srcAddr==10.0.0.1;|cnt<=5;|cnt=cnt+1|fwd(6)

def normalized_reg_actions(reg_actions):
    # turns "x=y" update actions into "x=y+0"
    normalized_reg_act = []
    for reg_act in reg_actions:
        has_operation = False
        for op in OPERATIONS.keys():
            if op in reg_act and op != 'NOP':
                has_operation = True
                break
        if has_operation:
            normalized_reg_act.append(reg_act)
        else:
            normalized_reg_act.append(reg_act + '+0')

    return normalized_reg_act


def parse_condition(cond):
    m = re.match(COND_REGEX, cond)
    if m:
        op1 = m.group(1)
        cond = m.group(2)
        op2 = m.group(3)
        return op1, cond, op2
    else:
        return None


def parse_reg_action(action):
    m = re.match(REG_ACTION_REGEX, action)
    if m:
        res = m.group(1)
        op1 = m.group(2)
        op = m.group(3)
        op2 = m.group(4)
        return res, op1, op, op2
    else:
        return None


def parse_pkt_action(action):
    m = re.match(PKT_ACTION_REGEX, action)
    if m:
        act = m.group(1)
        args = m.group(2)
        return act, args
    else:
        return None


def fdv_register(reg_id):
    return '0x%02X' % (FDV_BASE_REGISTER + reg_id)


def gdv_register(reg_id):
    return '0x%02X' % (GDV_BASE_REGISTER + (reg_id << 4))


def invalid_transition_str(edge, states):
    return 'Invalid transition ({})->({}): "{}"'.format(states[edge['src']]["text"],
                                                        states[edge['dst']]["text"],
                                                        edge['transition'])


def interpret_EFSM(json_str, packet_actions, efsm_match):
    cli_config = ''
    dbg_msg = ''

    states = json_str['nodes']
    links = json_str['links']

    edges = []
    flow_data_variables = set()
    global_data_variables = set()
    conditions = set()
    reg_actions = set()
    pkt_actions = set()

    no_efsm_matches = ["0&&&0" for _ in efsm_match] if efsm_match else []

    # Parse the states from the FSM nodes. Initial state is 0 or any states ending with *
    i = 1  # custom index of the state, it starts with 0 because the beginning state is always ZERO
    beginning_state = False
    for state in states:
        if state["text"].endswith("*") or state["text"] == '0':
            if beginning_state:
                logger.error("Multiple beginning states")
                dbg_msg += 'Multiple beginning states'
                return None, dbg_msg
            state["ID"] = 0
            beginning_state = True
        else:
            state["ID"] = i
            i += 1
    if not beginning_state:
        logger.error("Missing beginning state")
        dbg_msg += 'Missing beginning state'
        return None, dbg_msg

    # Parse JSON Graph to extract edges, matches, conditions, register updates and actions to be applied in every state transitions
    for link in links:
        logger.debug('Parsing transition: "%s"' % link['text'])
        link['text'] = link['text'].replace(' ', '')

        if link['type'] == 'Link':
            e = {'src': link['nodeA'], 'dst': link['nodeB'], 'transition': link['text']}

        elif link['type'] == 'SelfLink':
            e = {'src': link['node'], 'dst': link['node'], 'transition': link['text']}
        else:
            logger.warning("Other link:" + str(link))
            continue
        tmp = link['text'].split('|')

        matches = list(filter(lambda m: len(m) > 0, tmp[0].split(';')))
        if len(matches) == 0:
            e['match'] = no_efsm_matches
        else:
            e['match'] = []
            i = 0
            for e_m in efsm_match:
                if i < len(matches) and e_m in matches[i]:
                    if "&&&" not in matches[i].split("==")[1]:
                        dbg_msg += 'Cannot parse EFSM packet header matches: "%s"\n' % matches[i]
                        return None, dbg_msg
                    e['match'].append(matches[i].split("==")[1])
                    i += 1
                else:
                    e['match'].append("0&&&0")

        # NB conditions are then parsed in one shot because they are globally configured.
        # Actions on registers are instead parsed individually for each transition
        e['condition'] = list(filter(lambda c: len(c) > 0, tmp[1].split(';')))
        for cond in e['condition']:
            if parse_condition(cond):
                conditions.add(cond)
            else:
                log_msg = ('Cannot parse condition: "%s"\n' % cond) + invalid_transition_str(e, states)
                logger.warning(log_msg)
                dbg_msg += log_msg + '\n'
                return None, dbg_msg

        e['reg_action'] = list(filter(lambda x: len(x) > 0, tmp[2].split(';')))
        e['reg_action'] = normalized_reg_actions(e['reg_action'])
        if len(e['reg_action']) > MAX_REG_ACTIONS_PER_TRANSITION:
            # NB we adopt an all-or-nothing policy so we can avoid parsing ther rest of the transition
            log_msg = 'Too many register actions per transition\n' + invalid_transition_str(e, states)
            logger.warning(log_msg)
            dbg_msg += log_msg + '\n'
            return None, dbg_msg
        for ra in e['reg_action']:
            a = parse_reg_action(ra)
            if a:
                res, op1, op, op2 = a
                # reg_action result validation
                if res[0] == '#':
                    global_data_variables.add(res)
                elif res[0] == '@':
                    log_msg = 'Invalid register action: "%s"' % ra
                    logger.warning(log_msg)
                    dbg_msg += log_msg + "\n"
                    if res in ['@meta', '@now']:
                        log_msg = 'A register action cannot store the result into @meta or @now'
                        logger.warning(log_msg)
                        dbg_msg += log_msg + '\n'
                    else:
                        log_msg = 'Invalid result register: "%s"' % res
                        logger.warning(log_msg)
                        dbg_msg += log_msg + '\n'
                    log_msg = invalid_transition_str(e, states)
                    logger.warning(log_msg)
                    dbg_msg += log_msg + '\n'
                    return None, dbg_msg
                elif res.isnumeric():
                    log_msg = ('Invalid register action: "%s"\n' % ra)
                    log_msg += 'A register action cannot store the result into a constant\n'
                    log_msg += invalid_transition_str(e, states)
                    logger.warning(log_msg)
                    dbg_msg += log_msg + '\n'
                    return None, dbg_msg
                else:
                    flow_data_variables.add(res)
                # reg_action operators validation
                for op in [op1, op2]:
                    if op[0] == '#':
                        global_data_variables.add(op)
                    elif op[0] == '@':
                        if op in ['@meta', '@now']:
                            pass
                        else:
                            log_msg = ('Invalid register action: "%s\n' % ra) + (
                                        'Invalid register operator: "%s"\n' % op)
                            log_msg += invalid_transition_str(e, states)
                            logger.warning(log_msg)
                            dbg_msg += log_msg + '\n'
                            return None, dbg_msg
                    elif op.isnumeric():
                        pass
                    else:
                        flow_data_variables.add(op)
                reg_actions.add(ra)
            else:
                log_msg = ('Cannot parse register action: "%s"\n' % ra) + invalid_transition_str(e, states)
                logger.warning(log_msg)
                dbg_msg += log_msg + '\n'
                return None, dbg_msg

        e['pkt_action'] = list(filter(lambda x: len(x) > 0, tmp[3].split(';')))
        if len(e['pkt_action']) > 1:
            # NB we adopt an all-or-nothing policy so we can avoid parsing ther rest of the transition
            log_msg = 'Too many packet actions per transition\n' + invalid_transition_str(e, states)
            logger.warning(log_msg)
            dbg_msg += log_msg + "\n"
            return None, dbg_msg
        elif len(e['pkt_action']) == 1:
            e['pkt_action'] = e['pkt_action'][0]
            pa = parse_pkt_action(e['pkt_action'])
            if pa:
                # TODO validate the number of parameters!
                found = False
                for possible_pa in packet_actions:
                    if possible_pa == pa[0]:
                        found = True
                        pkt_actions.add(e['pkt_action'])
                        break
                if not found:
                    log_msg = ('Unrecognized packet action: "%s"\n' % e['pkt_action']) + invalid_transition_str(e, states)
                    logger.warning(log_msg)
                    dbg_msg += log_msg + "\n"
                    return None, dbg_msg
            else:
                log_msg = ('Cannot parse packet action: "%s"\n' % e['pkt_action']) + invalid_transition_str(e, states)
                dbg_msg += log_msg + "\n"
                return None, dbg_msg
        else:
            e['pkt_action'] = None
            if link['type'] == 'Link':
                log_msg = "No action specified for ({})->({}) transition '{}': default action will be applied".format(
                    states[e['src']]["text"], states[e['dst']]["text"], e['transition'])
            else:
                log_msg = "No action specified for self-transition in state ({}) '{}': default action will be applied".format(
                    states[e['src']]["text"], e['transition'])
            logger.warning(log_msg)
            dbg_msg += log_msg + "\n"

        edges.append(e)

    # Order all the sets in order to have reproducible runs

    # Now Flow Variable will contain a dict with ID and the name of the variables
    fdv_list = list(flow_data_variables)
    fdv_list.sort()
    flow_data_variables = dict(enumerate(fdv_list))
    flow_data_variables_reverse = {v: k for k, v in flow_data_variables.items()}
    logger.debug("Reversed flow variables: {}".format(flow_data_variables_reverse))

    gdv_list = list(global_data_variables)
    gdv_list.sort()
    global_data_variables = dict(enumerate(gdv_list))
    global_data_variables_reverse = {v: k for k, v in global_data_variables.items()}
    logger.debug("Reversed global variables: {}".format(global_data_variables_reverse))

    conditions_list = list(conditions)
    conditions_list.sort()
    conditions = dict(enumerate(conditions_list))
    conditions_reverse = {v: k for k, v in conditions.items()}
    logger.debug("Reversed conditions: {}".format(conditions_reverse))

    reg_actions_list = list(reg_actions)
    reg_actions_list.sort()
    reg_actions = dict(enumerate(reg_actions_list))
    logger.debug("Actions on registers: {}".format(reg_actions))

    pkt_actions_list = list(pkt_actions)
    pkt_actions_list.sort()
    pkt_actions = dict(enumerate(pkt_actions_list))
    # k+1 is needed to differentiate a un-initialized metadata (that is 0) and an action (that has to be different from 0)
    pkt_actions_reverse = {v: k + 1 for k, v in pkt_actions.items()}
    logger.debug("Reversed packet actions: {}".format(pkt_actions_reverse))

    conditions_parsed = {}
    # ------------------------------ CONDITIONS -----------------------------------------------------------------
    for (i, c) in conditions.items():
        tmp_cond = copy.deepcopy(TEMPLATE_CONDITION)
        cond = parse_condition(c)
        if cond:
            op1, operator, op2 = cond
            tmp_cond['cond'] = CONDITIONS[operator]
            for op_id, op in zip([1, 2], [op1, op2]):
                if op[0] not in ['@', '#']:
                    if op in flow_data_variables_reverse.keys():
                        # It is a FDV
                        tmp_cond['op%d' % op_id] = fdv_register(flow_data_variables_reverse[op])
                    elif not op.isnumeric():
                        logger.warning('Unknown flow data variable "%s"' % op)
                        logger.warning('Fatal error while parsing condition "%s"' % c)
                        dbg_msg += 'Unknown flow data variable "%s"\n' % op
                        dbg_msg += 'Fatal error while parsing condition "%s"\n' % c
                        return None, dbg_msg
                    else:
                        # it is a specific value (number)
                        tmp_cond['op%d' % op_id] = REGISTERS["EXPL"]
                        tmp_cond['operand%d' % op_id] = int(op)
                elif op[0] == '#':
                    if op in global_data_variables_reverse.keys():
                        # It is a GDV
                        tmp_cond['op%d' % op_id] = gdv_register(global_data_variables_reverse[op])
                    else:
                        logger.warning('Unknown global data variable "%s"' % op)
                        logger.warning('Fatal error while parsing condition "%s"' % c)
                        dbg_msg += 'Unknown global data variable "%s"\n' % op
                        dbg_msg += 'Fatal error while parsing condition "%s"\n' % c
                        return None, dbg_msg
                elif op[0] == '@' and op in META:
                    # It is a META (NOW, META)
                    tmp_cond['op%d' % op_id] = REGISTERS[op]
                else:
                    logger.warning('Cannot parse operator "%s"' % op)
                    logger.warning('Fatal error while parsing condition "%s"' % c)
                    dbg_msg += 'Cannot parse operator "%s"\n' % op
                    dbg_msg += 'Fatal error while parsing condition "%s"\n' % c
                    return None, dbg_msg

            conditions_parsed[c] = tmp_cond
        else:
            # It should never happen because we have already validated all the conditions in all the transitions
            logger.warning('Fatal error while parsing condition "%s"' % c)
            dbg_msg += 'Fatal error while parsing condition "%s"\n' % c
            return None, dbg_msg
    # TODO can we understand that "pkt >= 10" and "pkt < 10" are the same condition?
    if len(conditions_parsed) > MAX_CONDITIONS_NUM:
        logger.warning('Too many conditions')
        dbg_msg += 'Too many conditions\n'
        return None, dbg_msg
    logger.info("Parsed Conditions: {}".format(conditions_parsed))
    # -----------------------------------------------------------------------------------------------------------

    # ------------------------------ REG OPERATIONS -----------------------------------------------------------------
    reg_actions_parsed = {}
    for (i, a) in reg_actions.items():
        tmp_action = copy.deepcopy(TEMPLATE_ACTION)
        act = parse_reg_action(a)
        if act:
            res, op1, op, op2 = act
            tmp_action['operation'] = OPERATIONS[op]

            if res in flow_data_variables_reverse.keys():
                tmp_action['result'] = fdv_register(flow_data_variables_reverse[res])
            elif res in global_data_variables_reverse.keys():
                tmp_action['result'] = gdv_register(global_data_variables_reverse[res])
            else:
                logger.warning('Unknown result data variable "%s"' % res)
                logger.warning('Fatal error while parsing reg action "%s"' % a)
                dbg_msg += 'Unknown result data variable "%s"\n' % res
                dbg_msg += 'Fatal error while parsing reg action "%s"\n' % a
                return None, dbg_msg

            for op_id, op in zip([1, 2], [op1, op2]):
                if op[0] not in ['@', '#']:
                    if op in flow_data_variables_reverse.keys():
                        # It is a FDV
                        tmp_action['op%d' % op_id] = fdv_register(flow_data_variables_reverse[op])
                    elif not op.isnumeric():
                        logger.warning('Unknown flow data variable "%s"' % op)
                        logger.warning('Fatal error while parsing reg action "%s"' % a)
                        dbg_msg += 'Unknown flow data variable "%s"\n' % op
                        dbg_msg += 'Fatal error while parsing reg action "%s"\n' % a
                        return None, dbg_msg
                    else:
                        # it is a specific value (number)
                        tmp_action['op%d' % op_id] = REGISTERS["EXPL"]
                        tmp_action['operand%d' % op_id] = int(op)
                elif op[0] == '#':
                    if op in global_data_variables_reverse.keys():
                        # It is a GDV
                        tmp_action['op%d' % op_id] = gdv_register(global_data_variables_reverse[op])
                    else:
                        logger.warning('Unknown global data variable "%s"' % op)
                        logger.warning('Fatal error while parsing reg action "%s"' % a)
                        dbg_msg += 'Unknown global data variable "%s"\n' % op
                        dbg_msg += 'Fatal error while parsing reg action "%s"\n' % a
                        return None, dbg_msg
                elif op[0] == '@' and op in META:
                    # It is a META (NOW, META)
                    tmp_action['op%d' % op_id] = REGISTERS[op]
                else:
                    logger.warning('Cannot parse operator "%s"' % op)
                    logger.warning('Fatal error while parsing reg action "%s"' % a)
                    dbg_msg += 'Cannot parse operator "%s"\n' % op
                    dbg_msg += 'Fatal error while parsing reg action "%s"\n' % a
                    return None, dbg_msg

            reg_actions_parsed[a] = tmp_action
        else:
            # It should never happen because we have already validated all the reg actions in all the transitions
            logger.warning('Fatal error while parsing reg action "%s"' % a)
            dbg_msg += 'Fatal error while parsing reg action "%s"\n' % a
            return None, dbg_msg
    logger.info("REG actions: {}".format(reg_actions_parsed))
    # ---------------------------------------------------------------------------------------------------------------

    # ------------------------------ PACKET ACTIONS -----------------------------------------------------------------
    packet_actions_parsed = {}
    for (i, pkt_a) in pkt_actions.items():
        tmp_pkt_action = copy.deepcopy(TEMPLATE_PACKET_ACTION)
        for pa in packet_actions:
            if pa in pkt_a:
                a = parse_pkt_action(pkt_a)
                if a:
                    name, args = a
                    tmp_pkt_action['name'] = name
                    tmp_pkt_action['parameters'] = args.split(',')
                else:
                    # It should never happen because we have already validated all the reg actions in all the transitions
                    logger.warning('Fatal error while parsing pkt action "%s"' % a)
                    dbg_msg += 'Fatal error while parsing pkt action "%s"\n' % a
                    return None, dbg_msg

        packet_actions_parsed[pkt_a] = tmp_pkt_action
    logger.info("Packet actions: {}".format(packet_actions_parsed))
    # ---------------------------------------------------------------------------------------------------------------

    # ----------------------------- Augment edges with the previously parsed conditions and actions -----------------
    for e in edges:
        e['reg_action_parsed'] = []
        for act in e['reg_action']:
            e['reg_action_parsed'].append(reg_actions_parsed[act])
    # ---------------------------------------------------------------------------------------------------------------

    # ------------------------------------- Generate entry for the condition table  ---------------------------------
    lst_cond = []
    for (cond, cond_par) in conditions_parsed.items():
        lst_cond.append((conditions_reverse[cond], cond, cond_par))
    # Order conditions because order matter in the ID of the condition variable
    lst_cond.sort(key=lambda x: x[0])
    cond_table_config = copy.deepcopy(TEMPLATE_SET_DEFAULT_condition_table)
    for cond in lst_cond:
        cond_table_config += ' ' + str(cond[2]['cond']) + ' ' + str(cond[2]['op1']) + ' ' + str(
            cond[2]['op2']) + ' ' + str(
            cond[2]['operand1']) + ' ' + str(cond[2]['operand2'])
    # Fill-up the cond_table_config to have the 20 parameters required
    for _ in range(len(lst_cond), MAX_CONDITIONS_NUM):
        cond_table_config += ' ' + CONDITIONS["NOP"] + ' 0 0 0 0'
    cli_config += cond_table_config + "\n"
    # --------------------------------------------------------------------------------------------------------------

    # ------------------------------- Generate entries for the EFSM table ------------------------------------------
    for e in edges:
        tmp = {
            'state_match': str(states[e['src']]["ID"]) + "&&&0xFFFF",
            'c0_match': '0&&&0',
            'c1_match': '0&&&0',
            'c2_match': '0&&&0',
            'c3_match': '0&&&0',
            'OTHER_MATCH': '',
            'dest_state': str(states[e['dst']]["ID"]),
        }

        # Map condition on the edge with the previously generated condition variable
        for c in lst_cond:
            if c[1] in e['condition']:
                if c[0] == 0:
                    tmp['c0_match'] = '1&&&1'
                elif c[0] == 1:
                    tmp['c1_match'] = '1&&&1'
                elif c[0] == 2:
                    tmp['c2_match'] = '1&&&1'
                elif c[0] == 3:
                    tmp['c3_match'] = '1&&&1'
        cnt = 0
        # Add the register action to the EFSM Table Action part, the actual action on the register is perfomed by the UpdateLogic control block
        for r_a in e['reg_action_parsed']:
            tmp['operation_' + str(cnt)] = r_a['operation']
            tmp['result_' + str(cnt)] = r_a['result']
            tmp['op1_' + str(cnt)] = r_a['op1']
            tmp['op2_' + str(cnt)] = r_a['op2']
            tmp['operand1_' + str(cnt)] = r_a['operand1']
            tmp['operand2_' + str(cnt)] = r_a['operand2']
            cnt += 1
        logger.info("CNT: %i" % cnt)
        # Fill up with empty value the unused register update actions
        for i in range(cnt, MAX_REG_ACTIONS_PER_TRANSITION):
            tmp['operation_' + str(i)] = OPERATIONS['NOP']
            tmp['result_' + str(i)] = '0'
            tmp['op1_' + str(i)] = '0'
            tmp['op2_' + str(i)] = '0'
            tmp['operand1_' + str(i)] = '0'
            tmp['operand2_' + str(i)] = '0'

        # Set the action to be performed on the packet, the actual action is performed in the pkt_actions table
        if e['pkt_action']:
            tmp['pkt_action'] = pkt_actions_reverse[e['pkt_action']]
        else:
            # The default 0 value for flowblaze_metadata.pkt_action metadata triggers the execution of the default entry
            # in the pkt_action table following the flowblazeLoop
            tmp['pkt_action'] = 0

        # Set the packet header conditions
        tmp['OTHER_MATCH'] = ' '.join(e['match'])
        tmp['priority'] = DEFAULT_PRIO_EFSM  # Default priority

        cli_config += TEMPLATE_SET_DEFAULT_EFSMTable.format(**tmp) + "\n"
    # --------------------------------------------------------------------------------------------------------------

    # --------------------------------- Set the actual packet actions in the pkt_actions table ---------------------
    for (i, pkt_a) in pkt_actions.items():
        action = packet_actions_parsed[pkt_a]['name']
        action_parameters = ' '.join(packet_actions_parsed[pkt_a]['parameters'])
        # i+1 is needed to differentiate a un-initialized metadata (that is 0) and an action (that has to be different from 0)
        cli_config += TEMPLATE_SET_PACKET_ACTIONS.format(action=action, action_match=str(hex(i + 1)) + "&&&0xFF",
                                                         action_parameters=action_parameters, priority='10') + "\n"
    # --------------------------------------------------------------------------------------------------------------
    dbg_msg += '-' * 80 + '\n'
    dbg_msg += 'Flow data variables: '
    if len(flow_data_variables) > 0:
        dbg_msg += ', '.join(map(str, flow_data_variables.values()))
    else:
        dbg_msg += 'none'
    dbg_msg += '\nGlobal data variables: '
    if len(global_data_variables) > 0:
        dbg_msg += ', '.join(map(str, global_data_variables.values()))
    else:
        dbg_msg += 'none'
    dbg_msg += '\n'
    dbg_msg += '-' * 80 + '\n'
    dbg_msg += cli_config

    logger.debug("Generated entries:\n{}".format(cli_config))

    return cli_config, dbg_msg


if __name__ == '__main__':
    EXAMPLE_PACKET_ACTION = ['_drop', 'NoAction', 'forward']
    EXAMPLE_EFSM_MATCH_HEADER = ['hdr.ipv4.srcAddr', 'hdr.ipv4.dstAddr']
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', help='EFSM JSON as from the web gui', type=str, required=True)
    parser.add_argument('--output_file', help='Output file', type=str, required=True)
    parser.add_argument('--debug', help="Activate debug output", action='store_true')
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    debug = args.debug
    if debug:
        logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s][%(levelname)s] %(name)s: %(message)s ")
    else:
        logging.basicConfig(level=logging.INFO, format="[%(asctime)s][%(levelname)s] %(name)s: %(message)s ")

    # Load JSON
    with open(input_file, "r") as in_f:
        input_json = json.loads(in_f.read())

    cli_config, dbg_msg = interpret_EFSM(json_str=input_json, packet_actions=EXAMPLE_PACKET_ACTION,
                                         efsm_match=EXAMPLE_EFSM_MATCH_HEADER)
    if not cli_config:
        logging.error("Failed to parse %s" % input_file)
    else:
        with open(output_file, "w") as out_f:
            out_f.write(cli_config)
