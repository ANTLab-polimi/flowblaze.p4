import base64
import json
import io
import logging
import argparse

from flask import Flask, request, send_file, redirect, make_response, render_template

from efsm_interpreter import interpret_EFSM
from p4_json_parser import parse_files

app = Flask(__name__,  static_folder="www")


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
                           actions=gui_actions_param)


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
        cli_config, debug_msg = interpret_EFSM(json_str=fsm_json, packet_actions=list(gui_actions_param.keys()), efsm_match=efsm_match_fields)
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


if __name__ == "__main__":
    # Parse and patch index and config file
    parser = argparse.ArgumentParser()
    parser.add_argument('--p4_file', type=str, required=True)
    parser.add_argument('--program_name', type=str, required=False, default=None)
    parser.add_argument('--json_file', type=str, required=True)
    parser.add_argument('--debug', help="Activate debug output", action='store_true')
    args = parser.parse_args()

    p4_file = args.p4_file
    program_name = args.program_name
    if not program_name:
        program_name = p4_file.split("/")[-1]
    json_file = args.json_file
    debug = args.debug

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
