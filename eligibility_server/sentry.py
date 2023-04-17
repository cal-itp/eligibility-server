import os
import subprocess

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.scrubber import EventScrubber, DEFAULT_DENYLIST

from eligibility_server.settings import Configuration


SENTRY_ENVIRONMENT = os.environ.get("SENTRY_ENVIRONMENT", "local")


# https://stackoverflow.com/a/21901260/358804
def get_git_revision_hash():
    return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("ascii").strip()


def get_release() -> str:
    return get_git_revision_hash()


def get_denylist():
    # custom denylist
    denylist = DEFAULT_DENYLIST + ["sub", "name"]
    return denylist


def configure(config: Configuration):
    SENTRY_DSN = config.sentry_dsn
    if SENTRY_DSN:
        release = get_release()
        print(f"Enabling Sentry for environment '{SENTRY_ENVIRONMENT}', release '{release}'...")

        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[
                FlaskIntegration(),
            ],
            traces_sample_rate=1.0,
            environment=SENTRY_ENVIRONMENT,
            release=release,
            in_app_include=["eligibility_server"],
            # send_default_pii must be False (the default) for a custom EventScrubber/denylist
            # https://docs.sentry.io/platforms/python/data-management/sensitive-data/#event_scrubber
            send_default_pii=False,
            event_scrubber=EventScrubber(denylist=get_denylist()),
        )
    else:
        print("SENTRY_DSN not set, so won't send events")
