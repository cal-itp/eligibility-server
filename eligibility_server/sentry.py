import logging
import os

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.scrubber import EventScrubber, DEFAULT_DENYLIST

from eligibility_server import __version__
from eligibility_server.settings import Configuration

logger = logging.getLogger(__name__)


SENTRY_ENVIRONMENT = os.environ.get("SENTRY_ENVIRONMENT", "local")


def get_release() -> str:
    return __version__


def get_denylist():
    # custom denylist
    denylist = DEFAULT_DENYLIST + ["sub", "name"]
    return denylist


def get_traces_sample_rate(config: Configuration):
    rate = config.sentry_traces_sample_rate
    if rate < 0.0 or rate > 1.0:
        logger.warning("SENTRY_TRACES_SAMPLE_RATE was not in the range [0.0, 1.0], defaulting to 0.0")
        rate = 0.0
    else:
        logger.info(f"SENTRY_TRACES_SAMPLE_RATE set to: {rate}")

    return rate


def configure(config: Configuration):
    SENTRY_DSN = config.sentry_dsn
    if SENTRY_DSN:
        release = get_release()
        logger.info(f"Enabling Sentry for environment '{SENTRY_ENVIRONMENT}', release '{release}'...")

        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[
                FlaskIntegration(),
            ],
            traces_sample_rate=get_traces_sample_rate(config),
            environment=SENTRY_ENVIRONMENT,
            release=release,
            in_app_include=["eligibility_server"],
            # send_default_pii must be False (the default) for a custom EventScrubber/denylist
            # https://docs.sentry.io/platforms/python/data-management/sensitive-data/#event_scrubber
            send_default_pii=False,
            event_scrubber=EventScrubber(denylist=get_denylist()),
        )

        sentry_sdk.set_tag("agency_name", config.agency_name)
    else:
        logger.warning("SENTRY_DSN not set, so won't send events")
