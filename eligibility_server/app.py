"""
Simple Test Eligibility Verification API Server.
"""

from flask import Flask
from flask_restful import Api
from eligibility_server.verify import Verify

app = Flask(__name__)
api = Api(app)


@app.route("/healthcheck")
def healthcheck():
    return "Healthy"


api.add_resource(Verify, "/verify")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)  # nosec
