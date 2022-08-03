"""
App settings for server.
"""

import os

APP_NAME = "eligibility_server.app"
DEBUG_MODE = True
HOST = "0.0.0.0"  # nosec

# Database Configs

SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
IMPORT_FILE_PATH = os.environ.get("IMPORT_FILE_PATH")
IMPORT_FILE_FORMAT = os.environ.get("IMPORT_FILE_PATH").split(".")[-1]

# Server Configs

AUTH_HEADER = "X-Server-API-Key"
AUTH_TOKEN = "server-auth-token"
TOKEN_HEADER = "Authorization"
JWE_CEK_ENC = "A256CBC-HS512"
JWE_ENCRYPTION_ALG = "RSA-OAEP"
JWS_SIGNING_ALG = "RS256"
SUB_FORMAT_REGEX = os.environ.get("SUB_FORMAT_REGEX", ".*")

# Hash Configs from .env file

INPUT_HASH_ALGO = os.environ.get("INPUT_HASH_ALGO", "")

# CSV Configs from .env file
# To be used only if CSV file is being used
# csv.QUOTE_ALL = 1
# csv.QUOTE_MINIMAL = 0
# csv.QUOTE_NONNUMERIC = 2
# csv.QUOTE_NONE = 3
CSV_DELIMITER = os.environ.get("CSV_DELIMITER", ",")
CSV_NEWLINE = os.environ.get("CSV_NEWLINE", "")
CSV_QUOTING = os.environ.get("CSV_QUOTING", 3)
CSV_QUOTECHAR = os.environ.get("CSV_QUOTECHAR", "")
