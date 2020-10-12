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

import base64
import json
import io
import logging
import argparse

from flask import Flask, request, send_file, redirect, make_response, render_template

from efsm_interpreter import interpret_EFSM
from onos_rest import push_efsm_table, push_conditions, push_pkt_actions, DEFAULT_ONOS_IP, DEFAULT_ONOS_PORT
from p4_json_parser import parse_files

app = Flask(__name__,  static_folder="www/static", template_folder="www/templates")


@app.route('/')
def root():
    return redirect("index.html")


@app.route('/index.html')
def index():
    # Return the customized index for the specific use case, otherwise return the default index
    return render_template('index.html',
                           p4_program_name=program_name,
                           flow_scope=flow_scope,
                           header_condition_field=header_condition_field if header_condition_field else "none",
                           efsm_match_fields=efsm_match_fields if efsm_match_fields else [],
                           actions=gui_actions_param,
                           onos=onos_cfg)


@app.route('/<path:path>')
def static_files(path):
    return app.send_static_file(path)


# TODO: change name, it's misleading, we are just generating the control plane rules
@app.route("/generateCfg", methods=['POST'])
def generate_p4():
    if gui_actions_param is None:
        response = make_response()
        response.headers['debug_msg'] = base64.b64encode("GUI ACTIONS PARAMETERS NOT SET".encode("utf-8"))
        return response
    if request.method == 'POST':
        fsm_json = json.loads(request.data.decode('UTF-8'))
        cli_config, debug_msg, _ = interpret_EFSM(json_str=fsm_json, packet_actions=list(gui_actions_param.keys()), efsm_match=efsm_match_fields)
        if cli_config:
            mem = io.BytesIO()
            mem.write(cli_config.encode("utf-8"))
            mem.seek(0)
            file = send_file(
                mem,
                mimetype="text/plain",
                attachment_filename="out.cli",
                as_attachment=True,
                cache_timeout=0)
            response = make_response(file)
        else:
            response = make_response()
        response.headers['debug_msg'] = base64.b64encode(debug_msg.encode("utf-8"))

        return response
    return


@app.route("/generateCfgOnos", methods=['POST'])
def push_cfg_onos():
    if gui_actions_param is None:
        response = make_response()
        response.headers['debug_msg'] = base64.b64encode("GUI ACTIONS PARAMETERS NOT SET".encode("utf-8"))
        return response
    if request.method == 'POST':
        fsm_json = json.loads(request.data.decode('UTF-8'))
        onos_ip = request.args.get("onosIp", default=DEFAULT_ONOS_IP, type=str)
        onos_port = request.args.get("onosPort", default=DEFAULT_ONOS_PORT, type=int)
        cli_config, debug_msg, onos_cfg = interpret_EFSM(json_str=fsm_json, packet_actions=list(gui_actions_param.keys()), efsm_match=efsm_match_fields)
        onos_error = False
        response = make_response()
        if cli_config:
            response.headers["gen_ok"] = True
            # SEND TO ONOS
            for entry in onos_cfg["efsmEntries"]:
                if not push_efsm_table(entry, onos_ip, onos_port):
                    onos_error = True
                    debug_msg += ("\nFailed to push EFSM entry: %s" % entry)
            if not push_conditions({"conditions": onos_cfg["conditions"]}, onos_ip, onos_port):
                onos_error = True
                debug_msg += ("\nFailed to push Conditions: %s" % onos_cfg["conditions"])
            if not push_pkt_actions({"pktActions": onos_cfg["pktActions"]}, onos_ip, onos_port):
                onos_error = True
                debug_msg += ("\nFailed to push Packet actions: %s" % onos_cfg["pktActions"])

        else:
            response.headers["gen_ok"] = False
        response.headers["onos_ok"] = not onos_error
        response.headers['debug_msg'] = base64.b64encode(debug_msg.encode("utf-8"))
        return response
    return


if __name__ == "__main__":
    # Parse and patch index and config file
    parser = argparse.ArgumentParser()
    parser.add_argument('--p4_file', type=str, required=True)
    parser.add_argument('--program_name', type=str, required=False, default=None)
    parser.add_argument('--json_file', type=str, required=True)
    parser.add_argument('--onos_cfg', help='Activate ONOS configuration', action='store_true')
    parser.add_argument('--debug', help="Activate debug output", action='store_true')
    args = parser.parse_args()

    p4_file = args.p4_file
    program_name = args.program_name
    if not program_name:
        program_name = p4_file.split("/")[-1]
    json_file = args.json_file
    debug = args.debug
    onos_cfg = args.onos_cfg

    if debug:
        logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s][%(levelname)s] %(message)s ")
    else:
        logging.basicConfig(level=logging.INFO, format="[%(asctime)s][%(levelname)s] %(message)s ")

    # Parse P4 and Json file to build the custom GUI
    gui_actions_param, efsm_match_fields, flow_scope, header_condition_field = parse_files(p4_file, json_file)
    logging.info(gui_actions_param)
    logging.info(efsm_match_fields)
    logging.info(flow_scope)
    logging.info(header_condition_field)
    app.run(host='0.0.0.0', port=8000)