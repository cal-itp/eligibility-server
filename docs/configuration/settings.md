# Settings

The sections below outline in more detail the settings that you either must set or may want to override, and their purpose.

`*` Asterisk indicates a setting that you must set

## App settings

### `APP_NAME`

The name set on the Flask app

### `DEBUG_MODE`

Value passed as a keyword argument for `debug` in `app.run`

### `HOST`

Value passed as a keyword argument for `host` in `app.run`

### `LOG_LEVEL`

The log level used for the server's logging.

## Server settings

These settings configure how the server parses, composes, and validates requests and responses according to the [Eligibility API specification](https://docs.calitp.org/eligibility-api/specification/).

### `AUTH_HEADER`

The header name that the server expects to see from authenticated/authorized requests.

See the Eligibility API's documentation on [Authentication/Authorization](https://docs.calitp.org/eligibility-api/specification/#authenticationauthorization).

### `AUTH_TOKEN`

The header value that the server expects to see from authenticated/authorized requests.

See the Eligibility API's documentation on [Authentication/Authorization](https://docs.calitp.org/eligibility-api/specification/#authenticationauthorization).

### `TOKEN_HEADER`

The header name that the server expects to see for the header containing the token value.

### `JWE_CEK_ENC`

The value used for `enc` in the JOSE header of the [JWE](https://jwcrypto.readthedocs.io/en/latest/jwe.html).

See the Eligibility API's documentation on [Composing a message](https://docs.calitp.org/eligibility-api/specification/#composing-a-message).

### `JWE_ENCRYPTION_ALG`

The value used for `alg` in the JOSE header of the [JWE](https://jwcrypto.readthedocs.io/en/latest/jwe.html).

See the Eligibility API's documentation on [Composing a message](https://docs.calitp.org/eligibility-api/specification/#composing-a-message).

### `JWS_SIGNING_ALG`

The value used for `alg` in the JOSE header of the [JWS](https://jwcrypto.readthedocs.io/en/latest/jwt.html#jwcrypto.jwt.JWT.make_signed_token)

See the Eligibility API's documentation on [Composing a message](https://docs.calitp.org/eligibility-api/specification/#composing-a-message).

### `SUB_FORMAT_REGEX`

A regular expression that the request's `sub` field must match.

## Database settings

### `SQLALCHEMY_DATABASE_URI`

The URI that should be used for database connection.

!!! note
    See other configurable settings from [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/).

## Data settings

### `IMPORT_FILE_PATH`*

The path to file containing data to be imported into the server's database. Must be either CSV or JSON.

### `INPUT_HASH_ALGO`

Must be one of the types available in the [`hashlib` library's `algorithms_available` function](https://docs.python.org/3/library/hashlib.html#hashlib.algorithms_available).

## CSV-specific settings

When using a CSV import file, the following variables can be configured:

### `CSV_DELIMITER`

Specify a custom delimiter or use the default ","

### `CSV_NEWLINE`

Specify a newline or use the default of ""

### `CSV_QUOTECHAR`

Specify a quote character or use the default of none

### `CSV_QUOTING`

Default of 3 (no quotes)

These are the possible values for the `CSV_QUOTING` variable:

- `csv.QUOTE_MINIMAL`: 0 - To be used when the CSV file has quotes around entries which contain special characters such as delimiters, quotechar or any of the characters in lineterminator
- `csv.QUOTE_ALL`: 1 - To be used when all the values in the CSV file are present inside quotation marks
- `csv.QUOTE_NONNUMERIC`: 2 - To be used when the CSV file uses quotes around non-numeric entries
- `csv.QUOTE_NONE`: 3 - To be used when the CSV file does not use quotes around entries
