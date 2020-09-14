import json
import logging
import re
import sys


def parse_p4(p4_src_file):
    with open(p4_src_file) as f:
        l = f.readlines()

    HEADER_FIELD_EXTRACTOR_REGEX = r'#define[ ]+METADATA_OPERATION_COND[ ]+(\(.*\)[ ]*|)(.*)'
    EFSM_MATCH_FIELDS_REGEX = r'#define[ ]+EFSM_MATCH_FIELDS[ ]+(.*)'
    FLOW_HASH_FIELDS_REGEX = r'#define[ ]+FLOW_SCOPE[ ]+{(.*)}'

    EFSM_CONDITIONS_FIELD_str = list(filter(lambda x: 'METADATA_OPERATION_COND' in x, l))
    EFSM_CONDITIONS_FIELD = None
    for cond_field in EFSM_CONDITIONS_FIELD_str:
        m = re.search(HEADER_FIELD_EXTRACTOR_REGEX, cond_field.strip())
        if m:
            EFSM_CONDITIONS_FIELD = m.group(2)
    # TODO: parse also the type of match (exact, lpm, ternary ...)
    EFSM_MATCH_FIELDS_str = list(filter(lambda x: 'EFSM_MATCH_FIELDS' in x, l))
    EFSM_MATCH_FIELDS = None
    for efsm_match in EFSM_MATCH_FIELDS_str:
        m = re.search(EFSM_MATCH_FIELDS_REGEX, efsm_match.strip())
        if m:
            EFSM_MATCH_FIELDS = []
            for fi in m.group(1)[:-1].split(';'):
                EFSM_MATCH_FIELDS.append(fi.split(':')[0].strip())

    FLOW_HASH_FIELDS_REGEX_str = list(filter(lambda x: 'FLOW_SCOPE' in x, l))
    EFSM_LOOKUP_FIELDS = None
    for flow_fields in FLOW_HASH_FIELDS_REGEX_str:
        m = re.search(FLOW_HASH_FIELDS_REGEX, flow_fields.strip())
        if m:
            EFSM_LOOKUP_FIELDS = list(map(lambda x: x.strip(), m.group(1).split(',')))

    return EFSM_CONDITIONS_FIELD, EFSM_MATCH_FIELDS, EFSM_LOOKUP_FIELDS


def parse_json(json_file):
    with open(json_file) as f:
        j = f.read()

    j = json.loads(j)

    '''
    headers = list(filter(lambda x: x['metadata'] == False, j['headers']))
    fields = []
    for hdr in headers:
        hdr_type_data = filter(lambda x: x['name'] == hdr['header_type'], j['header_types'])
        for h in hdr_type_data:
            for field in h['fields']:
                fields.append('%s.%s' % (hdr['name'], field[0]))

    for field in fields:
        print(field)
    '''

    GUI_match_fields = []
    GUI_actions = []
    flowblaze_pipeline = list(filter(lambda x: x['name'] == 'ingress', j['pipelines']))[0]
    flowblaze_pipeline_tables = list(filter(lambda x: 'FlowBlaze.' in x['name'], flowblaze_pipeline['tables']))
    for table in flowblaze_pipeline_tables:
        # print(table['name'])
        # print('\tkeys:')
        for field in table['key']:
            # print('\t\t' + field['name'])
            if table['name'] == 'FlowBlaze.EFSM_table' and 'meta.flowblaze_metadata.' not in field['name']:
                GUI_match_fields.append(field['name'])
        # print('\tactions')
        for action in table['actions']:
            # print('\t\t' + action)
            if table['name'] == 'FlowBlaze.pkt_action':
                GUI_actions.append(action.replace('FlowBlaze.', ''))

    GUI_actions_parameters = {'NoAction': []}
    for action in GUI_actions:
        if action == 'NoAction':
            continue
        action_data = list(filter(lambda x: x['name'] == 'FlowBlaze.' + action, j['actions']))[0]
        GUI_actions_parameters[action] = []
        for param in action_data['runtime_data']:
            GUI_actions_parameters[action].append(param['name'])

    return GUI_match_fields, GUI_actions, GUI_actions_parameters


def parse_files(p4_file, json_file):
    # TODO keeping both EFSM_MATCH_FIELDS and GUI_match_fields is redundant...
    EFSM_CONDITIONS_FIELD, EFSM_MATCH_FIELDS, EFSM_LOOKUP_FIELDS = parse_p4(p4_file)
    GUI_match_fields, GUI_actions, GUI_actions_parameters = parse_json(json_file)

    logging.info('EFSM_CONDITIONS_FIELD: %s' % EFSM_CONDITIONS_FIELD)
    logging.info('EFSM_MATCH_FIELDS: %s' % EFSM_MATCH_FIELDS)
    logging.info('EFSM_LOOKUP_FIELDS: %s' % EFSM_LOOKUP_FIELDS)
    logging.info('')
    logging.info('GUI_match_fields: %s' % GUI_match_fields)
    logging.info('GUI_actions: %s' % GUI_actions)
    logging.info('GUI_actions_parameters: %s' % GUI_actions_parameters)

    return GUI_actions_parameters, EFSM_MATCH_FIELDS, EFSM_LOOKUP_FIELDS, EFSM_CONDITIONS_FIELD


if __name__ == "__main__":
    current_index = './www/index.html'
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s][%(levelname)s] %(name)s: %(message)s ')

    assert len(sys.argv) == 3, 'Required args: [P4_file] [JSON_file]'

    GUI_actions_parameters, _, _, _ = parse_files(sys.argv[1], sys.argv[2])
