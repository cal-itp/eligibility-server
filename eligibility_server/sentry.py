import os

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from eligibility_server.settings import Configuration


SENTRY_ENVIRONMENT = os.environ.get("SENTRY_ENVIRONMENT", "local")


def configure(config: Configuration):
    SENTRY_DSN = config.sentry_dsn
    if SENTRY_DSN:
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[
                FlaskIntegration(),
            ],
            traces_sample_rate=1.0,
            environment=SENTRY_ENVIRONMENT,
        )
    else:
        print("SENTRY_DSN not set, so won't send events")
