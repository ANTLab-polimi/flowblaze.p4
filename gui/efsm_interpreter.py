import argparse
import copy
import json
import logging
import re

from config import TEMPLATE_CONDITION, META, OPERATIONS, TEMPLATE_ACTION, POSSIBLE_PACKET_ACTION, \
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
    return '0x%02X' % (GDV_BASE_REGISTER + (reg_id<<4))

def invalid_transition_str(edge):
    return 'Skipping invalid transition ({})->({}): "{}"'.format(edge['src'], edge['dst'], edge['transition'])

def interpret_EFSM(json_str, packet_actions):
    cli_config = ''
    dbg_msg = ''

    nodes = json_str['nodes']
    links = json_str['links']

    edges = []
    flow_data_variables = set()
    global_data_variables = set()
    conditions = set()
    reg_actions = set()
    pkt_actions = set()

    # Parse JSON Graph to extract edges, matches, conditions, register updates and actions to be applied in every state transitions
    for link in links:
        logger.debug('Parsing transition: "%s"' % link['text'])
        link['text'] = link['text'].replace(' ', '')
        # temporary structures
        _conditions = []
        _global_data_variables = []
        _flow_data_variables = []
        _reg_actions = []
        _pkt_actions = []
        illegal_transition = False

        if link['type'] == 'Link':
            e = {'src': link['nodeA'], 'dst': link['nodeB'], 'transition': link['text']}

        elif link['type'] == 'SelfLink':
            e = {'src': link['node'], 'dst': link['node'], 'transition': link['text']}
        else:
            logger.warning("Other link:" + str(link))
            continue
        tmp = link['text'].split('|')

        e['match'] = list(filter(lambda m: len(m) > 0, tmp[0].split(';')))
        # TODO how is 'match' data handled afterwards?

        # NB conditions are then parsed in one shot because they are globally configured.
        # Actions on registers are instead parsed individually for each transition
        e['condition'] = list(filter(lambda c: len(c) > 0, tmp[1].split(';')))
        for cond in e['condition']:
            if parse_condition(cond):
                _conditions.append(cond)
            else:
                illegal_transition = True
                logger.warning('Cannot parse condition: "%s"' % cond)
                dbg_msg += 'Cannot parse condition: "%s"\n' % cond
                break
        if illegal_transition:
            # NB we adopt an all-or-nothing policy so we can avoid parsing ther rest of the transition
            logger.warning(invalid_transition_str(e))
            dbg_msg += invalid_transition_str(e) + '\n'
            continue

        e['reg_action'] = list(filter(lambda x: len(x) > 0, tmp[2].split(';')))
        e['reg_action'] = normalized_reg_actions(e['reg_action'])
        if len(e['reg_action']) > MAX_REG_ACTIONS_PER_TRANSITION:
            # NB we adopt an all-or-nothing policy so we can avoid parsing ther rest of the transition
            logger.warning('Too many register actions per transition')
            logger.warning(invalid_transition_str(e))
            dbg_msg += 'Too many register actions per transition\n'
            dbg_msg += invalid_transition_str(e) + '\n'
            continue
        for ra in e['reg_action']:
            a = parse_reg_action(ra)
            if a:
                res, op1, op, op2 = a
                # reg_action result validation
                if res[0] == '#':
                    _global_data_variables.append(res)
                elif res[0] == '@':
                    illegal_transition = True
                    logger.warning('Invalid register action: "%s"' % ra)
                    dbg_msg += 'Invalid register action: "%s"\n' % ra
                    if res in ['@meta', '@now']:
                        logger.warning('A register action cannot store the result into @meta or @now')
                        dbg_msg += 'A register action cannot store the result into @meta or @now\n'
                    else:
                        logger.warning('Invalid result register: "%s"' % res)
                        dbg_msg += 'Invalid result register: "%s"\n' % res
                    break
                elif res.isnumeric():
                    illegal_transition = True
                    logger.warning('Invalid register action: "%s"' % ra)
                    logger.warning('A register action cannot store the result into a constant')
                    dbg_msg += 'Invalid register action: "%s"\n' % ra
                    dbg_msg += 'A register action cannot store the result into a constant\n'
                    break
                else:
                    _flow_data_variables.append(res)
                # reg_action operators validation
                for op in [op1, op2]:
                    if op[0] == '#':
                        _global_data_variables.append(op)
                    elif op[0] == '@':
                        if op in ['@meta', '@now']:
                            pass
                        else:
                            illegal_transition = True
                            logger.warning('Invalid register action: "%s"' % ra)
                            logger.warning('Invalid register operator: "%s"' % op)
                            dbg_msg += 'Invalid register action: "%s"\n' % ra
                            dbg_msg += 'Invalid register operator: "%s"\n' % op
                            break
                    elif op.isnumeric():
                        pass
                    else:
                        _flow_data_variables.append(op)
                if illegal_transition:
                    # we can avoid parsing ther rest of the register actions
                    break
                else:
                    _reg_actions.append(ra)
            else:
                illegal_transition = True
                logger.warning('Cannot parse register action: "%s"' % ra)
                dbg_msg += 'Cannot parse register action: "%s"\n' % ra
                break
        if illegal_transition:
            # NB we adopt an all-or-nothing policy so we can avoid parsing ther rest of the transition
            logger.warning(invalid_transition_str(e))
            dbg_msg += invalid_transition_str(e) + '\n'
            continue

        e['pkt_action'] = list(filter(lambda x: len(x) > 0, tmp[3].split(';')))
        for pa in e['pkt_action']:
            if parse_pkt_action(pa):
                # TODO validate the number of parameters!
                found = False
                for possible_pa in packet_actions:
                    if possible_pa in pa:
                        found = True
                        _pkt_actions.append(pa)
                        break
                if not found:
                    illegal_transition = True
                    logger.warning('Unrecognized packet action: "%s"' % pa)
                    dbg_msg += 'Unrecognized packet action: "%s"\n' % pa
                    break
            else:
                illegal_transition = True
                logger.warning('Cannot parse packet action: "%s"' % ra)
                dbg_msg += 'Cannot parse packet action: "%s"\n' % ra
                break
        if illegal_transition:
            # NB we adopt an all-or-nothing policy so we can avoid parsing ther rest of the transition
            logger.warning(invalid_transition_str(e))
            dbg_msg += invalid_transition_str(e) + '\n'
            continue

        if e['pkt_action'] == []:
            if link['type'] == 'Link':
                logger.warning(
                    "No action specified for ({})->({}) transition '{}': default action will be applied".format(e['src'], e['dst'],
                                                                                                  e['transition']))
                dbg_msg += "No action specified for ({})->({}) transition '{}': default action will be applied\n".format(e['src'], e['dst'],
                                                                                                  e['transition'])
            else:
                logger.warning(
                    "No action specified for self-transition in state ({}) '{}': default action will be applied".format(e['src'], e[
                        'transition']))
                dbg_msg += "No action specified for self-transition in state ({}) '{}': default action will be applied\n".format(e['src'], e[
                        'transition'])

        # now that we are sure the transition is fully valid we can update all the structures
        for x in _conditions:
            conditions.add(x)
        for x in _global_data_variables:
            global_data_variables.add(x)
        for x in _flow_data_variables:
            flow_data_variables.add(x)
        for x in _reg_actions:
            reg_actions.add(x)
        for x in _pkt_actions:
            pkt_actions.add(x)

        edges.append(e)

    # Now Flow Variable will contain a dict with ID and the name of the variables
    flow_data_variables = dict(enumerate(flow_data_variables))
    flow_data_variables_reverse = {v: k for k, v in flow_data_variables.items()}
    logger.debug("Reversed flow variables: {}".format(flow_data_variables_reverse))

    global_data_variables = dict(enumerate(global_data_variables))
    global_data_variables_reverse = {v: k for k, v in global_data_variables.items()}
    logger.debug("Reversed global variables: {}".format(global_data_variables_reverse))

    conditions = dict(enumerate(conditions))
    conditions_reverse = {v: k for k, v in conditions.items()}
    logger.debug("Reversed conditions: {}".format(conditions_reverse))

    reg_actions = dict(enumerate(reg_actions))
    logger.debug("Actions on registers: {}".format(reg_actions))

    pkt_actions = dict(enumerate(pkt_actions))
    # k+1 is needed to differentiate a un-initialized metadata (that is 0) and an action (that has to be different from 0)
    pkt_actions_reverse = {v: k+1 for k, v in pkt_actions.items()}
    logger.debug("Reversed packet actions: {}".format(pkt_actions_reverse))

    conditions_parsed = {}
    # ------------------------------ CONDITIONS -----------------------------------------------------------------
    condition_parsing_failure = False
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
                        condition_parsing_failure = True
                        logger.warning('Unknown flow data variable "%s"' % op)
                        dbg_msg += 'Unknown flow data variable "%s"\n' % op
                        break
                    else:
                        # it is a specific value (number)
                        tmp_cond['op%d' % op_id] = REGISTERS["EXPL"]
                        tmp_cond['operand%d' % op_id] = int(op)
                elif op[0] == '#':
                    if op in global_data_variables_reverse.keys():
                        # It is a GDV
                        tmp_cond['op%d' % op_id] = gdv_register(global_data_variables_reverse[op])
                    else:
                        condition_parsing_failure = True
                        logger.warning('Unknown global data variable "%s"' % op)
                        dbg_msg += 'Unknown global data variable "%s"\n' % op
                        break
                elif op[0] == '@' and op in META:
                    # It is a META (NOW, META)
                    tmp_cond['op%d' % op_id] = REGISTERS[op]
                else:
                    condition_parsing_failure = True
                    logger.warning('Cannot parse operator "%s"' % op)
                    dbg_msg += 'Cannot parse operator "%s"\n' % op
                    break

            if condition_parsing_failure:
                break
            conditions_parsed[c] = tmp_cond
        else:
            # It should never happen because we have already validated all the conditions in all the transitions
            condition_parsing_failure = True
            break
    if condition_parsing_failure:
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
    reg_action_parsing_failure = False
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
                reg_action_parsing_failure = True
                logger.warning('Unknown result data variable "%s"' % res)
                dbg_msg += 'Unknown result data variable "%s"\n' % res
                break

            for op_id, op in zip([1, 2], [op1, op2]):
                if op[0] not in ['@', '#']:
                    if op in flow_data_variables_reverse.keys():
                        # It is a FDV
                        tmp_action['op%d' % op_id] = fdv_register(flow_data_variables_reverse[op])
                    elif not op.isnumeric():
                        reg_action_parsing_failure = True
                        logger.warning('Unknown flow data variable "%s"' % op)
                        dbg_msg += 'Unknown flow data variable "%s"\n' % op
                        break
                    else:
                        # it is a specific value (number)
                        tmp_action['op%d' % op_id] = REGISTERS["EXPL"]
                        tmp_action['operand%d' % op_id] = int(op)
                elif op[0] == '#':
                    if op in global_data_variables_reverse.keys():
                        # It is a GDV
                        tmp_action['op%d' % op_id] = gdv_register(global_data_variables_reverse[op])
                    else:
                        reg_action_parsing_failure = True
                        logger.warning('Unknown global data variable "%s"' % op)
                        dbg_msg += 'Unknown global data variable "%s"\n' % op
                        break
                elif op[0] == '@' and op in META:
                    # It is a META (NOW, META)
                    tmp_action['op%d' % op_id] = REGISTERS[op]
                else:
                    reg_action_parsing_failure = True
                    logger.warning('Cannot parse operator "%s"' % op)
                    dbg_msg += 'Cannot parse operator "%s"\n' % op
                    break

            if reg_action_parsing_failure:
                break
            reg_actions_parsed[a] = tmp_action
        else:
            # It should never happen because we have already validated all the reg actions in all the transitions
            reg_action_parsing_failure = True
            break
    if reg_action_parsing_failure:
        logger.warning('Fatal error while parsing reg action "%s"' % a)
        dbg_msg += 'Fatal error while parsing reg action "%s"\n' % a
        return None, dbg_msg
    logger.info("REG actions: {}".format(reg_actions_parsed))
    # ---------------------------------------------------------------------------------------------------------------

    # ------------------------------ PACKET ACTIONS -----------------------------------------------------------------
    packet_actions_parsed = {}
    pkt_action_parsing_failure = False
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
                    pkt_action_parsing_failure = True
                    break
        packet_actions_parsed[pkt_a] = tmp_pkt_action
    if pkt_action_parsing_failure:
        logger.warning('Fatal error while parsing pkt action "%s"' % a)
        dbg_msg += 'Fatal error while parsing pkt action "%s"\n' % a
        return None, dbg_msg
    logger.info("Packet actions: {}".format(packet_actions_parsed))
    # ---------------------------------------------------------------------------------------------------------------

    # ----------------------------- Augment edges with the previously parsed conditions and actions -----------------
    for e in edges:
        e['reg_action_parsed'] = []
        for act in e['reg_action']:
            e['reg_action_parsed'].append(reg_actions_parsed[act])

        e['cond_parsed'] = []
        for cond in e['condition']:
            e['cond_parsed'].append(conditions_parsed[cond])

        e['pkt_action_parsed'] = []
        for actt in e['pkt_action']:
            e['pkt_action_parsed'].append(packet_actions_parsed[actt])
    # ---------------------------------------------------------------------------------------------------------------

    # ------------------------------------- Generate entry for the condition table  ---------------------------------
    lst_cond = []
    for (cond, cond_par) in conditions_parsed.items():
        lst_cond.append((conditions_reverse[cond], cond, cond_par))
    # Order conditions because order matter in the ID of the condition variable
    lst_cond.sort(key=lambda x: x[0])
    cond_table_config = copy.deepcopy(TEMPLATE_SET_DEFAULT_condition_table)
    for cond in lst_cond:
        cond_table_config += str(cond[2]['cond']) + ' ' + str(cond[2]['op1']) + ' ' + str(cond[2]['op2']) + ' ' + str(
            cond[2]['operand1']) + ' ' + str(cond[2]['operand2']) + ' '
    # Fill-up the cond_table_config to have the 20 parameters required
    for _ in range(len(lst_cond), MAX_CONDITIONS_NUM):
        cond_table_config += CONDITIONS["NOP"] + ' 0 0 0 0 '
    cli_config += cond_table_config +"\n"
    # --------------------------------------------------------------------------------------------------------------

    # ------------------------------- Generate entries for the EFSM table ------------------------------------------
    for e in edges:
        tmp = {
            'state_match': str(e['src']) + "&&&0xFFFF",
            'c0_match': '0&&&0',
            'c1_match': '0&&&0',
            'c2_match': '0&&&0',
            'c3_match': '0&&&0',
            'OTHER_MATCH': '',
            'dest_state': str(e['dst']),
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
        # Fill up with empty value the unused register update actions
        for i in range(cnt, MAX_REG_ACTIONS_PER_TRANSITION):
            tmp['operation_' + str(i)] = OPERATIONS['NOP']
            tmp['result_' + str(i)] = '0'
            tmp['op1_' + str(i)] = '0'
            tmp['op2_' + str(i)] = '0'
            tmp['operand1_' + str(i)] = '0'
            tmp['operand2_' + str(i)] = '0'

        # Set the action to be performed on the packet, the actual action is performed in the pkt_actions table
        for p_action in e['pkt_action']:
            tmp['pkt_action'] = pkt_actions_reverse[p_action]
        if len(e['pkt_action']) == 0:
            # We set a dummy value for the pkt_action parameter so that an unknown value for opp_metadata.pkt_action
            # metadata triggers the execution of the default entry in the pkt_action table following the oppLoop
            tmp['pkt_action'] = max(pkt_actions_reverse.values()) + 1

        tmp['priority'] = DEFAULT_PRIO_EFSM  # Default priority

        cli_config += TEMPLATE_SET_DEFAULT_EFSMTable.format(**tmp) + "\n"
    # --------------------------------------------------------------------------------------------------------------

    # --------------------------------- Set the actual packet actions in the pkt_actions table ---------------------
    for (i, pkt_a) in pkt_actions.items():
        action = packet_actions_parsed[pkt_a]['name']
        action_parameters = ' '.join(packet_actions_parsed[pkt_a]['parameters'])
        # i+1 is needed to differentiate a un-initialized metadata (that is 0) and an action (that has to be different from 0)
        cli_config += TEMPLATE_SET_PACKET_ACTIONS.format(action=action, action_match=str(hex(i+1)) + "&&&0xFF",
                                                     action_parameters=action_parameters, priority='10') + "\n"
    # --------------------------------------------------------------------------------------------------------------
    dbg_msg += '-'*80 + '\n'
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
    dbg_msg += '-'*80 + '\n'
    dbg_msg += cli_config

    logger.debug("Generated entries:\n{}".format(cli_config))

    return cli_config, dbg_msg

if __name__ == '__main__':
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

    cli_commands = interpret_EFSM(json_str=input_json, packet_actions=POSSIBLE_PACKET_ACTION)

    with open(output_file, "w") as out_f:
        out_f.write(cli_commands)
