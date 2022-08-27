"""
Simple Test Eligibility Verification API Server.
"""
import logging

from flask import Flask, jsonify, make_response
from flask_restful import Api
from flask.logging import default_handler

from .verify import Verify
from .keypair import get_server_public_key
from .db import models

app = Flask(__name__)
app.config.from_object("eligibility_server.settings")
app.config.from_envvar("ELIGIBILITY_SERVER_SETTINGS", silent=True)

app.logger.setLevel(app.config["LOG_LEVEL"])
default_handler.formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s:%(lineno)s %(message)s")


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


api = Api(app)
api.add_resource(Verify, "/verify")

models.init_app(app)

if __name__ == "__main__":
    app.run(host=app.config["HOST"], debug=app.config["DEBUG_MODE"], port="8000")  # nosec
