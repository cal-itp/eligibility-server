"""
Simple Test Eligibility Verification API Server.
"""

from flask import Flask
from flask_restful import Api

from . import settings
from .verify import Verify


app = Flask(__name__)
app.name = settings.APP_NAME


@app.route("/healthcheck")
def healthcheck():
    return "Healthy"


api = Api(app)
api.add_resource(Verify, "/verify")


if __name__ == settings.__name__:
    app.run(host=settings.HOST, debug=settings.DEBUG_MODE)  # nosec
