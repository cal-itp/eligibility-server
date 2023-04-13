import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


def configure():
    sentry_sdk.init(
        integrations=[
            FlaskIntegration(),
        ],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
    )
