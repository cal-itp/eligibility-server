"""
Simple Test Eligibility Verification API Server.
"""
import logging

from flask import Flask, jsonify, make_response
from flask_restful import Api
from flask.logging import default_handler

from eligibility_server import db
from eligibility_server.keypair import get_server_public_key
from eligibility_server.settings import Configuration
from eligibility_server.verify import Verify


config = Configuration()

app = Flask(__name__)
app.config.from_object("eligibility_server.settings")
app.config.from_envvar("ELIGIBILITY_SERVER_SETTINGS", silent=True)

format_string = "[%(asctime)s] %(levelname)s %(name)s:%(lineno)s %(message)s"

# use an app context for access to config settings
with app.app_context():
    # configure root logger first, to prevent duplicate log entries from Flask's logger
    logging.basicConfig(level=config.log_level, format=format_string)
    # configure Flask's logger
    app.logger.setLevel(config.log_level)
    default_handler.formatter = logging.Formatter(format_string)


def TextResponse(content):
    # from https://stackoverflow.com/a/57302496/453168
    response = make_response(content, 200)
    response.mimetype = "text/plain"
    return response


@app.route("/healthcheck")
def healthcheck():
    app.logger.info("Request healthcheck")
    return TextResponse("Healthy")


@app.route("/publickey")
def publickey():
    app.logger.info("Request public key")
    key = get_server_public_key()
    pem_data = key.export_to_pem(private_key=False)
    return TextResponse(pem_data.decode("utf-8"))


@app.errorhandler(401)
def unauthorized(error):
    app.logger.error(error)
    return jsonify(error=f"{error.code} {error.name}: Unauthorized"), 401


@app.errorhandler(403)
def forbidden(error):
    app.logger.error(error)
    return jsonify(error=f"{error.code} {error.name}: Forbidden"), 403


@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return jsonify(error=f"{error.code} {error.name}: {error.description}"), 404


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error(error)
    return jsonify(error=f"{error.code} {error.name}: Internal server error"), 500


@app.after_request
def enforce_strict_transport_security(response):
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response


api = Api(app)
api.add_resource(Verify, "/verify")

db.init_app(app)

if __name__ == "__main__":
    app.run(host=config.host, debug=config.debug_mode, port="8000")  # nosec
