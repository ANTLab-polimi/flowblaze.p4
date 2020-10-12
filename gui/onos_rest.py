# Copyright 2020 Daniele Moro <daniele.moro@polimi.it>
#                Davide Sanvito <davide.sanvito@neclab.eu>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging

import requests

DEFAULT_ONOS_USER = "onos"
DEFAULT_ONOS_PASS = "rocks"
DEFAULT_ONOS_IP = "onos"  # default when running with compose
DEFAULT_ONOS_PORT = 8181
DEFAULT_FLOWBLAZE_DEVICE_ID = "device:leaf1"


def config_flowblaze_device_id(flowblaze_device_id, onos_ip, onos_port):
    logging.debug("Set FlowBlaze device ID: %s" % flowblaze_device_id)
    code = json_get_req('http://%s:%d/onos/flowblaze/setDeviceId/%s' % (onos_ip, onos_port, flowblaze_device_id))
    if code != 200:
        return False
    return True


def push_efsm_table(efsm_table_dict, onos_ip, onos_port):
    logging.debug("Efsm Entry: %s" % str(efsm_table_dict))
    code = json_post_req(('http://%s:%d/onos/flowblaze/setEfsmEntry' % (onos_ip, onos_port)),
                         json.dumps(efsm_table_dict))
    if code != 200:
        return False
    return True


def push_conditions(conditions_dict, onos_ip, onos_port):
    logging.debug("Conditions: %s" % str(conditions_dict))
    code = json_post_req(('http://%s:%d/onos/flowblaze/setConditions' % (onos_ip, onos_port)),
                         json.dumps(conditions_dict))
    if code != 200:
        return False
    return True


def push_pkt_actions(pkt_actions_dict, onos_ip, onos_port):
    logging.debug("Packet Action: %s" % str(pkt_actions_dict))
    code = json_post_req(('http://%s:%d/onos/flowblaze/setPktActions' % (onos_ip, onos_port)),
                         json.dumps(pkt_actions_dict))
    if code != 200:
        return False
    return True


def json_post_req(url, json_data):
    try:
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        response = requests.post(url,
                                 data=json_data,
                                 auth=(DEFAULT_ONOS_USER, DEFAULT_ONOS_PASS), headers=headers,
                                 timeout=0.5)
        logging.debug(response.text)
        return response.status_code
    except IOError as e:
        logging.error(str(e))
        return 500


def json_get_req(url, params=None):
    try:
        response = requests.get(url,
                                params=params,
                                auth=(DEFAULT_ONOS_USER, DEFAULT_ONOS_PASS),
                                timeout=0.5)
        logging.debug(response.text)
        return response.status_code
    except IOError as e:
        logging.error(str(e))
        return 500
