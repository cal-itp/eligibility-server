"""
Default settings for server.
"""

APP_NAME = "eligibility_server.app"
DEBUG_MODE = True
HOST = "0.0.0.0"  # nosec

# Database Configs

SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Server Configs

AUTH_HEADER = "X-Server-API-Key"
AUTH_TOKEN = "server-auth-token"
TOKEN_HEADER = "Authorization"
JWE_CEK_ENC = "A256CBC-HS512"
JWE_ENCRYPTION_ALG = "RSA-OAEP"
JWS_SIGNING_ALG = "RS256"
SUB_FORMAT_REGEX = ".*"

# Hash Configs

INPUT_HASH_ALGO = ""

# CSV Configs
CSV_DELIMITER = ","
CSV_NEWLINE = ""
CSV_QUOTING = 3
CSV_QUOTECHAR = ""
