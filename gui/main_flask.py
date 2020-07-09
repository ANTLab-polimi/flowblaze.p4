import json
import io
import logging

from flask import Flask, request, send_file, redirect

from efsm_interpreter import interpret_EFSM

logging.basicConfig(level=logging.INFO, format="[%(asctime)s][%(levelname)s] %(message)s ")
app = Flask(__name__,  static_folder="www")


@app.route('/')
def root():
    return redirect("index.html")


@app.route('/<path:path>')
def static_files(path):
    return app.send_static_file(path)


# TODO: change name, it's misleading, we are just generating the control plane rules
@app.route("/generateP4", methods=['POST'])
def generate_p4():
    if request.method == 'POST':
        fsm_json = json.loads(request.data.decode('UTF-8'))
        result = interpret_EFSM(json_str=fsm_json)
        mem = io.BytesIO()
        mem.write(result.encode("utf-8"))
        mem.seek(0)
        return send_file(
            mem,
            mimetype="text/plain",
            attachment_filename="out.cli",
            as_attachment=True,
            cache_timeout=0)
    return


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
