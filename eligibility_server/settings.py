"""
Default settings for server.
"""

# App Configs

APP_NAME = "eligibility_server.app"
DEBUG_MODE = True
HOST = "0.0.0.0"  # nosec
LOG_LEVEL = "INFO"

# Database Configs

SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# API Configs

AUTH_HEADER = "X-Server-API-Key"
AUTH_TOKEN = "server-auth-token"
TOKEN_HEADER = "Authorization"

# Eligibility Verification Configs

CLIENT_KEY_PATH = "./keys/client.pub"
JWE_CEK_ENC = "A256CBC-HS512"
JWE_ENCRYPTION_ALG = "RSA-OAEP"
JWS_SIGNING_ALG = "RS256"
SERVER_KEY_PATH = "./keys/server.key"
SUB_FORMAT_REGEX = ".*"

# Hashing Configs

INPUT_HASH_ALGO = ""

# CSV Configs

CSV_DELIMITER = ","
CSV_NEWLINE = ""
CSV_QUOTING = 3
CSV_QUOTECHAR = ""
