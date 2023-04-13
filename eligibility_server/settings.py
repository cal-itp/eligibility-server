"""
Default settings for server.
"""
from flask import current_app

# App settings

APP_NAME = "eligibility_server.app"
DEBUG_MODE = True
HOST = "0.0.0.0"  # nosec
LOG_LEVEL = "INFO"
REQUEST_TIMEOUT = (3, 20)

# Database settings

SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# API settings

AUTH_HEADER = "X-Server-API-Key"
AUTH_TOKEN = "server-auth-token"
TOKEN_HEADER = "Authorization"

# Eligibility Verification settings

CLIENT_KEY_PATH = "./keys/client.pub"
JWE_CEK_ENC = "A256CBC-HS512"
JWE_ENCRYPTION_ALG = "RSA-OAEP"
JWS_SIGNING_ALG = "RS256"
SERVER_PRIVATE_KEY_PATH = "./keys/server.key"
SERVER_PUBLIC_KEY_PATH = "./keys/server.pub"
SUB_FORMAT_REGEX = ".*"

# Data settings

IMPORT_FILE_PATH = "data/server.csv"
INPUT_HASH_ALGO = "sha512"

# CSV-specific settings

CSV_DELIMITER = ","
CSV_QUOTING = 3
CSV_QUOTECHAR = '"'

# Sentry

SENTRY_DSN = None


class Configuration:
    # App settings

    @property
    def app_name(self):
        return str(current_app.config["APP_NAME"])

    @property
    def debug_mode(self):
        return bool(current_app.config["DEBUG_MODE"])

    @property
    def host(self):
        return str(current_app.config["HOST"])

    @property
    def log_level(self):
        return str(current_app.config["LOG_LEVEL"])

    @property
    def request_timeout(self):
        return current_app.config["REQUEST_TIMEOUT"]

    # API settings

    @property
    def auth_header(self):
        return str(current_app.config["AUTH_HEADER"])

    @property
    def auth_token(self):
        return str(current_app.config["AUTH_TOKEN"])

    @property
    def token_header(self):
        return str(current_app.config["TOKEN_HEADER"])

    # Eligibility Verification settings

    @property
    def client_key_path(self):
        return str(current_app.config["CLIENT_KEY_PATH"])

    @property
    def jwe_cek_enc(self):
        return str(current_app.config["JWE_CEK_ENC"])

    @property
    def jwe_encryption_alg(self):
        return str(current_app.config["JWE_ENCRYPTION_ALG"])

    @property
    def jws_signing_alg(self):
        return str(current_app.config["JWS_SIGNING_ALG"])

    @property
    def server_private_key_path(self):
        return str(current_app.config["SERVER_PRIVATE_KEY_PATH"])

    @property
    def server_public_key_path(self):
        return str(current_app.config["SERVER_PUBLIC_KEY_PATH"])

    @property
    def sub_format_regex(self):
        return str(current_app.config["SUB_FORMAT_REGEX"])

    # Data settings

    @property
    def import_file_path(self):
        return str(current_app.config["IMPORT_FILE_PATH"])

    @property
    def input_hash_algo(self):
        return str(current_app.config["INPUT_HASH_ALGO"])

    # CSV-specific settings

    @property
    def csv_delimiter(self):
        return str(current_app.config["CSV_DELIMITER"])

    @property
    def csv_quoting(self):
        return int(current_app.config["CSV_QUOTING"])

    @property
    def csv_quotechar(self):
        return str(current_app.config["CSV_QUOTECHAR"])

    # Sentry

    @property
    def sentry_dsn(self):
        sentry_dsn = current_app.config["SENTRY_DSN"]
        return str(sentry_dsn) if sentry_dsn else None
