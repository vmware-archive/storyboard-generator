
from storyboardgenerator import everything, actorAttributes

from flask import Flask, send_from_directory, request, safe_join, jsonify
import os.path
import json

app = Flask(__name__)


app.config.from_envvar('ASSETS_SETTINGS')

@app.route("/render", methods=['POST'])
def render():
    data = everything(request.data.decode())


    response = app.response_class(
        response=data,
        status=200,
        mimetype='application/json',
        headers={
            'Access-Control-Allow-Origin': '*',
            "Access-Control-Allow-Methods": "OPTIONS, GET, POST, PUT, PATCH, DELETE",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        }
    )
    return response


@app.route('/assets')
def metadata():
    response = app.response_class(
        response=json.dumps(actorAttributes),
        status=200,
        mimetype='application/json',
        headers={
            'Access-Control-Allow-Origin': '*',
            "Access-Control-Allow-Methods": "OPTIONS, GET, POST, PUT, PATCH, DELETE",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        }
    )
    return response


@app.route('/assets/<path:filename>')
def asset(filename):
    return send_from_directory(app.config['ASSET_PATH'], filename)

@app.route('/assets/<path:directory>/<path:filename>')
def subasset(directory, filename):
    print("Attempting to serve asset_from_directory %s, %s" % (directory, filename))
    return send_from_directory(app.config['ASSET_PATH'], safe_join(directory, filename))

@app.route("/")
@app.route("/home")
@app.route("/documentation")
@app.route("/<filename>")
@app.route('/ui/<filename>')
def serve_ui(filename="index.html"):
    return send_from_directory(app.config['UI_PATH'], filename)


print("Serving UI out of %s" % app.config['UI_PATH'])
print("Serving ASSETS out of %s" % app.config['ASSET_PATH'])

if __name__ == "__main__":
    app.run()
