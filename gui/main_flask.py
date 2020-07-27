import base64
import json
import io
import logging
import argparse

from flask import Flask, request, send_file, redirect, make_response

from efsm_interpreter import interpret_EFSM
from p4_json_parser import parse_files

app = Flask(__name__,  static_folder="www")


@app.route('/')
def root():
    return redirect("index.html")


@app.route('/index.html')
def index():
    # Return the customized index for the specific use case, otherwise return the default index
    return html_index if html_index is not None else app.send_static_file("index.html")


@app.route('/<path:path>')
def static_files(path):
    return app.send_static_file(path)


# TODO: change name, it's misleading, we are just generating the control plane rules
@app.route("/generateCfg", methods=['POST'])
def generate_p4():
    if gui_actions is None:
        return
    if request.method == 'POST':
        fsm_json = json.loads(request.data.decode('UTF-8'))
        cli_config, debug_msg = interpret_EFSM(json_str=fsm_json, packet_actions=gui_actions)
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
    parser.add_argument('--json_file', type=str, required=True)
    parser.add_argument('--debug', help="Activate debug output", action='store_true')
    args = parser.parse_args()

    p4_file = args.p4_file
    json_file = args.json_file
    debug = args.debug

    if debug:
        logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s][%(levelname)s] %(message)s ")
    else:
        logging.basicConfig(level=logging.INFO, format="[%(asctime)s][%(levelname)s] %(message)s ")

    # Parse P4 and Json file to build the custom GUI
    html_index, gui_actions = parse_files(p4_file, json_file)

    app.run(host='0.0.0.0', port=8000)
