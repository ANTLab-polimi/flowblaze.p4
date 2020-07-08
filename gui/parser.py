import json
import copy
import logging

from config import TEMPLATE_CONDITION, META, OPERATIONS, TEMPLATE_ACTION, POSSIBLE_PACKET_ACTION, \
    TEMPLATE_PACKET_ACTION, CONDITIONS, TEMPLATE_SET_DEFAULT_condition_table, REGISTERS, TEMPLATE_SET_DEFAULT_EFSMTable, \
    TEMPLATE_SET_PACKET_ACTIONS

FILE_CONFIG = "state_machine.json"
FILE_CONFIG = "rate_limiter.json"

# POSSIBLE_CONDITIONS = ['<=', '>=', '>', '==', '<']
# POSSIBLE_OPERATIONS = ['+', '-', '>>', '<<', '*']
EQUAL = '='


# REMEMBER: CONDITIONS ARE ORDERED!!!!!!


#ipv4.srcAddr==10.0.0.1;ipv4.srcAddr==10.0.0.1;|cnt<=5;|cnt=cnt+1|fwd(6)
def parse(json_str=None):
    output = ""
    if json_str is None:
        with open(FILE_CONFIG, mode='r') as f:
            config = json.loads(f.read())
    else:
        config = json_str

    nodes = config['nodes']
    links = config['links']

    states = []
    for n in nodes:
        states.append(n['text'])
    # print(states)
    # print(config)
    edges = []
    flow_variables = set()
    conditions = set()
    reg_actions = set()
    pkt_actions = set()
    for l in links:
        if l['type'] == 'Link':
            e = {'src': states[int(l['nodeA'])], 'dst': states[int(l['nodeB'])], 'transition': l['text']}

        elif l['type'] == 'SelfLink':
            e = {'src': l['node'], 'dst': l['node'], 'transition': l['text']}
        else:
            print("Other links")
            continue
        tmp = l['text'].split('|')

        e['match'] = list(filter(lambda x: len(x) > 0, tmp[0].split(';')))

        e['condition'] = list(filter(lambda x: len(x) > 0, tmp[1].split(';')))

        for c in e['condition']:
            if len(c) > 0:
                conditions.add(c)

        e['reg_action'] = list(filter(lambda x: len(x) > 0, tmp[2].split(';')))
        for ra in e['reg_action']:
            if len(ra) > 0:
                reg_actions.add(ra)
                if EQUAL in ra:
                    flow_variables.add(ra.split(EQUAL)[0])
        e['pkt_action'] = list(filter(lambda x: len(x) > 0, tmp[3].split(';')))
        for pa in e['pkt_action']:
            if len(pa) > 0:
                pkt_actions.add(pa)
        edges.append(e)

    # Now Flow Variable will contain a dict with ID and the name of the variables
    flow_variables = dict(enumerate(flow_variables))
    flow_variables_reverse = {v: k for k, v in flow_variables.items()}
    # print(flow_variables_reverse)

    conditions = dict(enumerate(conditions))
    conditions_reverse = {v: k for k, v in conditions.items()}
    # print(conditions_reverse)

    reg_actions = dict(enumerate(reg_actions))
    # print(reg_actions)

    pkt_actions = dict(enumerate(pkt_actions))
    pkt_actions_reverse = {v: k for k, v in pkt_actions.items()}

    conditions_parsed = {}
    # ------------------------------ CONDITIONS -----------------------------------------------------------------
    # Let's interpret the CONDITIONS
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
    print(conditions_parsed)
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
                    #po is the actual operation
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
            # print(tmp_action)
            fdv_actions_parsed[a] = tmp_action
        else:
            print(res, 'is not a FLOW DATA VARIABLE')
    print(fdv_actions_parsed)
        # print(a, res, op)
    # ---------------------------------------------------------------------------------------------------------------

    # ------------------------------ PACKET ACTIONS -----------------------------------------------------------------
    packet_actions_parsed = {}
    for (i, pkt_a) in pkt_actions.items():
        tmp_pkt_action = copy.deepcopy(TEMPLATE_PACKET_ACTION)
        for pa in POSSIBLE_PACKET_ACTION:
            if pa in pkt_a:
                tmp_pkt_action['name'] = pa
                print(pa, pkt_a)
                tmp_pkt_action['parameters'] = pkt_a.replace(pa, '').replace('(', '').replace(')', '').split(',')
                print(tmp_action)
                break
        packet_actions_parsed[pkt_a] = tmp_pkt_action
    print(packet_actions_parsed)
    # ---------------------------------------------------------------------------------------------------------------

    # ------------------------------------ Merge the PARSED PART with the actual transition edges -------------------
    print(edges)
    for e in edges:
        e['reg_action_parsed'] = []
        for act in e['reg_action']:
            e['reg_action_parsed'].append(fdv_actions_parsed[act])


        e['cond_parsed'] = []
        for cond in e['condition']:
            e['cond_parsed'].append(conditions_parsed[cond])

        e['pkt_action_parsed']= []
        for actt in e['pkt_action']:
            e['pkt_action_parsed'].append(packet_actions_parsed[actt])
    print(edges)

    # ---------------------------------------------------------------------------------------------------------------

    # ------------------------------------- START generating the condition operation --------------------------------
    lst_cond = []
    for (cond, cond_par) in conditions_parsed.items():
        lst_cond.append( (conditions_reverse[cond], cond, cond_par))
    lst_cond.sort(key=lambda x: x[0])
    cond_table_config = copy.deepcopy(TEMPLATE_SET_DEFAULT_condition_table)

    for cond in lst_cond:
        # d['cond'+str(cond[0])] = cond[2]['cond']
        cond_table_config += str(cond[2]['cond']) + ' ' + str(cond[2]['op1']) + ' ' + str(cond[2]['op2']) + ' ' + str(cond[2]['operand1']) + ' ' + str(cond[2]['operand2']) + ' '

    #{pkt_action} {priority}"

    print(cond_table_config)
    for e in edges:
        tmp = {
            'state_match': str(e['src'])+"&&&0xFFFF",
            'c0_match': '0&&&0',
            'c1_match': '0&&&0',
            'c2_match': '0&&&0',
            'c3_match': '0&&&0',
            'OTHER_MATCH' : '',
            'dest_state': str(e['dst']),
            }
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
        for r_a in e['reg_action_parsed']:
            # print(r_a)
            tmp['operation_'+str(cnt)] = r_a['operation']
            tmp['result_'+str(cnt)] = r_a['result']
            tmp['op1_'+str(cnt)] = r_a['op1']
            tmp['op2_'+str(cnt)] = r_a['op2']
            tmp['operand1_'+str(cnt)] = r_a['operand1']
            tmp['operand2_'+str(cnt)] = r_a['operand2']
            cnt += 1

        for i in range(cnt, 2):
            tmp['operation_' + str(i)] = '0'
            tmp['result_' + str(i)] = '0'
            tmp['op1_' + str(i)] = '0'
            tmp['op2_' + str(i)] = '0'
            tmp['operand1_' + str(i)] = '0'
            tmp['operand2_' + str(i)] = '0'


        for p_action in e['pkt_action_parsed']:
            tmp['pkt_action'] = pkt_actions_reverse[p_action['name']]
        tmp['priority'] = "1"
        # print(tmp)
        output += TEMPLATE_SET_DEFAULT_EFSMTable.format(**tmp) + "\n"
        print(TEMPLATE_SET_DEFAULT_EFSMTable.format(**tmp))

    # TEMPLATE_SET_PACKET_ACTIONS = "table_add ingress.pkt_action {action} {action_match} => {action_parameters} {priority}"
    for (i, pkt_a) in pkt_actions.items():
        output += TEMPLATE_SET_PACKET_ACTIONS.format(action=pkt_a, action_match=str(hex(i))+"&&&0xFF", action_parameters='', priority='10')  + "\n"
        print(TEMPLATE_SET_PACKET_ACTIONS.format(action=pkt_a, action_match=str(hex(i))+"&&&0xFF", action_parameters='', priority='10'))
        # print('asd')

    return output
        # for c in e['condition']:
        #     print (c)
        # TEMPLATE_SET_DEFAULT_EFSMTable.format(state_match)

    # ---------------------------------------------------------------------------------------------------------------


    # print(conditions)
    # print(flow_variables)



    # for e in edges:
    #     tmp = e['transition'].split('|')
    #     e['match'] = tmp[0].split(';')
    #     e['condition'] = tmp[1].split(';')
    #     e['reg_action'] = tmp[2].split(';')
    #     e['pkt_action'] = tmp[3].split(';')
    # print(edges)
    # print(edges)
    # print(links)


# Flow variables: you can find them in conditions and reg_action


    


if __name__ == '__main__':
    parse()
