"""
Default settings for server.
"""

# App settings

APP_NAME = "eligibility_server.app"
DEBUG_MODE = True
HOST = "0.0.0.0"  # nosec
LOG_LEVEL = "INFO"

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
SUB_FORMAT_REGEX = ".*"

# Data settings

IMPORT_FILE_PATH = ""
INPUT_HASH_ALGO = ""

# CSV-specific settings

CSV_DELIMITER = ","
CSV_NEWLINE = ""
CSV_QUOTING = 3
CSV_QUOTECHAR = ""
