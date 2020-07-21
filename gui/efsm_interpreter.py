import argparse
import copy
import json
import logging

from config import TEMPLATE_CONDITION, META, OPERATIONS, TEMPLATE_ACTION, POSSIBLE_PACKET_ACTION, \
    TEMPLATE_PACKET_ACTION, CONDITIONS, TEMPLATE_SET_DEFAULT_condition_table, REGISTERS, \
    TEMPLATE_SET_DEFAULT_EFSMTable, TEMPLATE_SET_PACKET_ACTIONS, DEFAULT_PRIO_EFSM, EQUAL

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


def interpret_EFSM(json_str, packet_actions):
    output = ""

    nodes = json_str['nodes']
    links = json_str['links']

    edges = []
    flow_variables = set()
    conditions = set()
    reg_actions = set()
    pkt_actions = set()

    # Parse JSON Graph to extract edges, matches, conditions, register updates and actions to be applied in every state transitions
    for link in links:
        link['text'] = link['text'].replace(' ', '')

        if link['type'] == 'Link':
            e = {'src': link['nodeA'], 'dst': link['nodeB'], 'transition': link['text']}

        elif link['type'] == 'SelfLink':
            e = {'src': link['node'], 'dst': link['node'], 'transition': link['text']}
        else:
            logger.warning("Other link:" + str(link))
            continue
        tmp = link['text'].split('|')

        e['match'] = list(filter(lambda m: len(m) > 0, tmp[0].split(';')))

        e['condition'] = list(filter(lambda c: len(c) > 0, tmp[1].split(';')))

        for cond in e['condition']:
            if len(cond) > 0:
                conditions.add(cond)

        e['reg_action'] = list(filter(lambda x: len(x) > 0, tmp[2].split(';')))
        # turns "x=y" update actions into "x=y+0"
        e['reg_action'] = list(
            map(lambda x: x + '+0' if all(op not in x for op in OPERATIONS.keys() if op is not 'NOP') else x,
                e['reg_action']))
        for ra in e['reg_action']:
            if len(ra) > 0:
                reg_actions.add(ra)
                if EQUAL in ra:
                    flow_variables.add(ra.split(EQUAL)[0])
        e['pkt_action'] = list(filter(lambda x: len(x) > 0, tmp[3].split(';')))
        for pa in e['pkt_action']:
            if len(pa) > 0:
                pkt_actions.add(pa)
        if e['reg_action'] == [] and e['pkt_action'] == []:
            if link['type'] == 'Link':
                logger.warning(
                    "Skipping ({})->({}) transition '{}': at least one action is required".format(e['src'], e['dst'],
                                                                                                  e['transition']))
            else:
                logger.warning(
                    "Skipping self-transition in state ({}) '{}': at least one action is required".format(e['src'], e[
                        'transition']))
            continue
        edges.append(e)

    # Now Flow Variable will contain a dict with ID and the name of the variables
    flow_variables = dict(enumerate(flow_variables))
    flow_variables_reverse = {v: k for k, v in flow_variables.items()}
    logger.debug("Reversed flow variables: {}".format(flow_variables_reverse))

    conditions = dict(enumerate(conditions))
    conditions_reverse = {v: k for k, v in conditions.items()}
    logger.debug("Reversed conditions: {}".format(conditions_reverse))

    reg_actions = dict(enumerate(reg_actions))
    logger.debug("Actions on registers: {}".format(reg_actions))

    pkt_actions = dict(enumerate(pkt_actions))
    pkt_actions_reverse = {v: k for k, v in pkt_actions.items()}
    logger.debug("Reversed packet actions: {}".format(pkt_actions_reverse))

    conditions_parsed = {}
    # ------------------------------ CONDITIONS -----------------------------------------------------------------
    # TODO can we understand that "pkt >= 10" and "pkt < 10" are the same condition?
    # Interpret the conditions, maximum
    for (i, c) in conditions.items():
        tmp_cond = copy.deepcopy(TEMPLATE_CONDITION)
        for pc in CONDITIONS.keys():
            if pc in c:
                cond = c.split(pc)
                tmp_cond['cond'] = CONDITIONS[pc]
                for (x, e) in enumerate(cond):
                    if e in flow_variables_reverse.keys():
                        # It is a FDV
                        if x == 0:
                            tmp_cond['op1'] = flow_variables_reverse[e]
                        elif x == 1:
                            tmp_cond['op2'] = flow_variables_reverse[e]
                    elif e in META:
                        # It is a META (NOW, EXPL, META)
                        if x == 0:
                            tmp_cond['op1'] = REGISTERS[e]
                        elif x == 1:
                            tmp_cond['op2'] = REGISTERS[e]
                    else:
                        # it is a specific value (number)
                        if x == 0:
                            tmp_cond['op1'] = REGISTERS["EXPL"]
                            tmp_cond['operand1'] = int(e)
                        elif x == 1:
                            tmp_cond['op2'] = REGISTERS["EXPL"]
                            tmp_cond['operand2'] = int(e)
                    # print(tmp_cond)
                break
        conditions_parsed[c] = tmp_cond
    logger.info("Parsed Conditions: {}".format(conditions_parsed))
    # -----------------------------------------------------------------------------------------------------------

    # ------------------------------ FDV OPERATIONS -----------------------------------------------------------------
    fdv_actions_parsed = {}
    for (i, a) in reg_actions.items():
        tmp_action = copy.deepcopy(TEMPLATE_ACTION)
        res = a.split(EQUAL)[0]
        op = a.split(EQUAL)[1]
        if res in flow_variables_reverse.keys():
            # Set where result should go
            tmp_action['result'] = flow_variables_reverse[res]
            for po in OPERATIONS.keys():
                if po in op:
                    # po is the actual operation
                    tmp_action['operation'] = OPERATIONS[po]
                    act = op.split(po)
                    for (x, e) in enumerate(act):
                        if e in flow_variables_reverse.keys():
                            # It is a FDV
                            if x == 0:
                                tmp_action['op1'] = flow_variables_reverse[e]
                            elif x == 1:
                                tmp_action['op2'] = flow_variables_reverse[e]
                        elif e in META:
                            # It is a META (NOW, EXPL, META)
                            if x == 0:
                                tmp_action['op1'] = REGISTERS[e]
                            elif x == 1:
                                tmp_action['op2'] = REGISTERS[e]
                        else:
                            # it is a specific value (number)
                            if x == 0:
                                tmp_action['op1'] = REGISTERS["EXPL"]
                                tmp_action['operand1'] = int(e)
                            elif x == 1:
                                tmp_action['op2'] = REGISTERS["EXPL"]
                                tmp_action['operand2'] = int(e)
                    break
            fdv_actions_parsed[a] = tmp_action
        else:
            logger.warning('{} is not a FLOW DATA VARIABLE'.format(res))
    logger.info("FDV actions: {}".format(fdv_actions_parsed))
    # ---------------------------------------------------------------------------------------------------------------

    # ------------------------------ PACKET ACTIONS -----------------------------------------------------------------
    packet_actions_parsed = {}
    for (i, pkt_a) in pkt_actions.items():
        tmp_pkt_action = copy.deepcopy(TEMPLATE_PACKET_ACTION)
        for pa in packet_actions:
            if pa in pkt_a:
                tmp_pkt_action['name'] = pa.split('(')[0]
                tmp_pkt_action['parameters'] = pkt_a.replace(pa, '').replace('(', '').replace(')', '').split(',')
                break
        packet_actions_parsed[pkt_a] = tmp_pkt_action
    logger.info("Packet actions: {}".format(packet_actions_parsed))
    # ---------------------------------------------------------------------------------------------------------------

    # ----------------------------- Augment edges with the previously parsed conditions and actions -----------------
    for e in edges:
        e['reg_action_parsed'] = []
        for act in e['reg_action']:
            e['reg_action_parsed'].append(fdv_actions_parsed[act])

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
        for i in range(cnt, 2):
            tmp['operation_' + str(i)] = '0'
            tmp['result_' + str(i)] = '0'
            tmp['op1_' + str(i)] = '0'
            tmp['op2_' + str(i)] = '0'
            tmp['operand1_' + str(i)] = '0'
            tmp['operand2_' + str(i)] = '0'

        # Set the action to be performed on the packet, the actual action is performed in the pkt_actions table
        for p_action in e['pkt_action']:
            tmp['pkt_action'] = pkt_actions_reverse[p_action]

        tmp['priority'] = DEFAULT_PRIO_EFSM  # Default priority

        output += TEMPLATE_SET_DEFAULT_EFSMTable.format(**tmp) + "\n"
    # --------------------------------------------------------------------------------------------------------------

    # --------------------------------- Set the actual packet actions in the pkt_actions table ---------------------
    for (i, pkt_a) in pkt_actions.items():
        action = packet_actions_parsed[pkt_a]['name']
        action_parameters = ' '.join(packet_actions_parsed[pkt_a]['parameters'])
        output += TEMPLATE_SET_PACKET_ACTIONS.format(action=action, action_match=str(hex(i)) + "&&&0xFF",
                                                     action_parameters=action_parameters, priority='10') + "\n"
    # --------------------------------------------------------------------------------------------------------------

    logger.debug("Generated entries:\n{}".format(output))
    return output

# TODO: parse P4 and JSON files to retrieve the packet actions instead of using the hardcoded one in config.py
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
