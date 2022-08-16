from logging.config import dictConfig


def configure(log_level: str):
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s %(name)s:%(lineno)s %(message)s",
                    "datefmt": "%d/%b/%Y %H:%M:%S",
                }
            },
            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                }
            },
            "root": {"level": log_level, "handlers": ["wsgi"]},
        }
    )
