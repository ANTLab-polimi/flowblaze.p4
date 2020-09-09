import json
import logging

import requests

ONOS_USER = "onos"
ONOS_PASS = "rocks"
ONOS_IP = "172.17.0.4"
ONOS_PORT = 8181


def push_efsm_table(efsm_table_dict):
    logging.debug("Efsm Entry: %s" % str(efsm_table_dict))
    code = json_post_req(('http://%s:%d/onos/flowblaze/setEfsmEntry' % (ONOS_IP, ONOS_PORT)), json.dumps(efsm_table_dict))
    if code != 200:
        return False
    return True


def push_conditions(conditions_dict):
    logging.debug("Conditions: %s" % str(conditions_dict))
    code = json_post_req(('http://%s:%d/onos/flowblaze/setConditions' % (ONOS_IP, ONOS_PORT)), json.dumps(conditions_dict))
    if code != 200:
        return False
    return True


def push_pkt_actions(pkt_actions_dict):
    logging.debug("Packet Action: %s" % str(pkt_actions_dict))
    code = json_post_req(('http://%s:%d/onos/flowblaze/setPktActions' % (ONOS_IP, ONOS_PORT)), json.dumps(pkt_actions_dict))
    if code != 200:
        return False
    return True


def json_post_req(url, json_data):
    try:
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        response = requests.post(url, data=json_data,
                                 auth=(ONOS_USER, ONOS_PASS), headers=headers, timeout=0.5)
        logging.debug(response.text)
        return response.status_code
    except IOError as e:
        logging.error(str(e))
        return 500
