from pprint import pprint
import json
import re
import sys

def parse_p4(p4_src_file):
	with open(p4_src_file) as f:
		l = f.readlines()

	HEADER_FIELD_EXTRACTOR_REGEX = r'#define[ ]+METADATA_OPERATION_COND[ ]+(\(.*\)[ ]*|)(.*)'
	EFSM_MATCH_FIELDS_REGEX = r'#define[ ]+EFSM_MATCH_FIELDS[ ]+(.*)'

	EFSM_CONDITIONS_FIELD_str = list(filter(lambda x: 'METADATA_OPERATION_COND' in x, l))
	if len(EFSM_CONDITIONS_FIELD_str) > 0:
		EFSM_CONDITIONS_FIELD_str = EFSM_CONDITIONS_FIELD_str[0].strip()
		m = re.search(HEADER_FIELD_EXTRACTOR_REGEX, EFSM_CONDITIONS_FIELD_str)
		if m:
			EFSM_CONDITIONS_FIELD = m.group(2)
		else:
			# empty METADATA_OPERATION_COND macro
			EFSM_CONDITIONS_FIELD = None
	else:
		# missing METADATA_OPERATION_COND macro
		EFSM_CONDITIONS_FIELD = None

	EFSM_MATCH_FIELDS_str = list(filter(lambda x: 'EFSM_MATCH_FIELDS' in x, l))
	if len(EFSM_MATCH_FIELDS_str) > 0:
		EFSM_MATCH_FIELDS_str = EFSM_MATCH_FIELDS_str[0].strip()
		m = re.search(EFSM_MATCH_FIELDS_REGEX, EFSM_MATCH_FIELDS_str)
		if m:
			EFSM_MATCH_FIELDS_str = m.group(1)
			EFSM_MATCH_FIELDS = []
			for f in EFSM_MATCH_FIELDS_str[:-1].split(';'):
				EFSM_MATCH_FIELDS.append(f.split(':')[0].strip())
		else:
			# empty EFSM_MATCH_FIELDS macro
			EFSM_MATCH_FIELDS = None
	else:
		# missing EFSM_MATCH_FIELDS macro
		EFSM_MATCH_FIELDS = None

	return EFSM_CONDITIONS_FIELD, EFSM_MATCH_FIELDS

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
	in_pipeline = list(filter(lambda x: x['name'] == 'ingress', j['pipelines']))[0]
	in_pipeline_tables = list(filter(lambda x: 'ingress.' in x['name'], in_pipeline['tables']))
	for table in in_pipeline_tables:
		#print(table['name'])
		#print('\tkeys:')
		for field in table['key']:
			#print('\t\t' + field['name'])
			if table['name'] == 'ingress.oppLoop.EFSM_table' and 'meta.opp_metadata.' not in field['name']:
				GUI_match_fields.append(field['name'])
		#print('\tactions')
		for action in table['actions']:
			#print('\t\t' + action)
			if table['name'] == 'ingress.pkt_action':
				GUI_actions.append(action.replace('ingress.', ''))

	GUI_actions_parameters = {'NoAction': []}
	for action in GUI_actions:
		if action == 'NoAction':
			continue
		action_data = list(filter(lambda x: x['name'] == 'ingress.' + action, j['actions']))[0]
		GUI_actions_parameters[action] = []
		for param in action_data['runtime_data']:
			GUI_actions_parameters[action].append(param['name'])


	return GUI_match_fields, GUI_actions, GUI_actions_parameters

if __name__ == "__main__":
	assert len(sys.argv) == 3, 'Required args: [P4_file] [JSON_file]'

	# TODO keeping both EFSM_MATCH_FIELDS and GUI_match_fields is redundant...
	EFSM_CONDITIONS_FIELD, EFSM_MATCH_FIELDS = parse_p4(sys.argv[1])
	GUI_match_fields, GUI_actions, GUI_actions_parameters = parse_json(sys.argv[2])

	print('EFSM_CONDITIONS_FIELD:', EFSM_CONDITIONS_FIELD)
	print('EFSM_MATCH_FIELDS:', EFSM_MATCH_FIELDS)
	print()
	print('GUI_match_fields:', GUI_match_fields)
	print('GUI_actions:', GUI_actions)
	print('GUI_actions_parameters:', GUI_actions_parameters)	

	with open('./www/index.html.template', 'r') as f:
		html = f.readlines()

	idx = html.index('  <option value="matchField">matchField</option>\n')
	for match_field in GUI_match_fields[::-1]:
		html.insert(idx + 1, '  <option value="%s">%s</option>\n' % (match_field, match_field))

	idx = html.index('  <option value="action">action</option>\n')
	for action in GUI_actions[::-1]:
		action_str = '%s(%s)' % (action, ''.join(GUI_actions_parameters[action]))
		html.insert(idx + 1, '  <option value="%s">%s</option>\n' % (action, action_str))

	with open('./www/index.html', 'w') as f:
		f.writelines(html)

# davide@davide-PC:~/opp.p4/gui$ python3 p4_json_parser.py ../p4src/rate_limiter/rate_limiter.p4 ../p4build/rate_limiter/bmv2.json