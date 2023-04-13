import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from eligibility_server.settings import Configuration


def configure(config: Configuration):
    SENTRY_DSN = config.sentry_dsn
    if SENTRY_DSN:
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[
                FlaskIntegration(),
            ],
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1.0,
        )
    else:
        print("SENTRY_DSN not set, so won't send events")
