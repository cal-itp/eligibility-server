# Settings

The sections below outline in more detail the settings that you either must set or may want to override, and their purpose.

`*` Asterisk indicates a setting that you must set

## App settings

### `AGENCY_NAME`

The name of the agency that this server is deployed for

### `APP_NAME`

The name set on the Flask app

### `DEBUG_MODE`

Value passed as a keyword argument for `debug` in `app.run`

### `HOST`

Value passed as a keyword argument for `host` in `app.run`

### `LOG_LEVEL`

The log level used for the server's logging.

## Database settings

!!! note

    See other configurable settings from [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/).

### `SQLALCHEMY_DATABASE_URI`

The URI that should be used for database connection.

## API settings

These settings configure access to the API endpoints on the server.

### `AUTH_HEADER`

The header name that the server expects to see from authenticated/authorized requests.

See the Eligibility API's documentation on [Authentication/Authorization](https://docs.calitp.org/eligibility-api/specification/#authenticationauthorization).

### `AUTH_TOKEN`

The header value that the server expects to see from authenticated/authorized requests.

See the Eligibility API's documentation on [Authentication/Authorization](https://docs.calitp.org/eligibility-api/specification/#authenticationauthorization).

### `TOKEN_HEADER`

The header name that the server expects to see for the header containing the Eligibility Verification request token.

## Eligibility Verification settings

These settings configure how the server parses, composes, and validates requests and responses according to the [Eligibility API specification](https://docs.calitp.org/eligibility-api/specification/).

### `CLIENT_KEY_PATH`

The path to the Eligibility Verification _client's_ public key, stored as a PEM text file. Used to verify the client's request signature, and to encrypt the server's response.

Can be a path to a local file or a remote URL. For URLs, a simple anonymous GET request is made.

### `JWE_CEK_ENC`

The value used for `enc` in the JOSE header of the [JWE](https://jwcrypto.readthedocs.io/en/latest/jwe.html).

See the Eligibility API's documentation on [Composing a message](https://docs.calitp.org/eligibility-api/specification/#composing-a-message).

### `JWE_ENCRYPTION_ALG`

The value used for `alg` in the JOSE header of the [JWE](https://jwcrypto.readthedocs.io/en/latest/jwe.html).

See the Eligibility API's documentation on [Composing a message](https://docs.calitp.org/eligibility-api/specification/#composing-a-message).

### `JWS_SIGNING_ALG`

The value used for `alg` in the JOSE header of the [JWS](https://jwcrypto.readthedocs.io/en/latest/jwt.html#jwcrypto.jwt.JWT.make_signed_token)

See the Eligibility API's documentation on [Composing a message](https://docs.calitp.org/eligibility-api/specification/#composing-a-message).

### `SERVER_PRIVATE_KEY_PATH`

The path to the server's private key, stored as a PEM text file. Used to decrypt the client's request and sign the server's response.

Can be a path to a local file or a remote URL. For URLs, a simple anonymous GET request is made.

### `SERVER_PUBLIC_KEY_PATH`

The path to the public key corresponding to the [server's private key](#server_private_key_path), stored as a PEM text file. Used by clients to encrypt
requests sent to this server.

Can be a path to a local file or a remote URL. For URLs, a simple anonymous GET request is made.

### `SUB_FORMAT_REGEX`

A regular expression that the request's `sub` field must match.

## Data settings

### `IMPORT_FILE_PATH`\*

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

## Sentry

### `SENTRY_DSN`

Cal-ITP's Sentry instance collects both [errors ("Issues")](https://sentry.calitp.org/organizations/sentry/issues/?project=4) and app [performance info](https://sentry.calitp.org/organizations/sentry/performance/?project=4).

[Alerts are sent to #benefits-notify in Slack.](https://sentry.calitp.org/organizations/sentry/alerts/rules/eligibility-server/10/details/) [Others can be configured.](https://sentry.calitp.org/organizations/sentry/alerts/rules/)

You can troubleshoot Sentry itself by [turning on debug mode](#debug_mode) and visiting `/error/`.

!!! tldr "Sentry docs"

    [Data Source Name (DSN)](https://docs.sentry.io/product/sentry-basics/dsn-explainer/)

Enables sending events to Sentry.

### `SENTRY_ENVIRONMENT`

!!! tldr "Sentry docs"

    [`environment` config value](https://docs.sentry.io/platforms/python/configuration/options/#environment)

Segments errors by which deployment they occur in. This defaults to `local`, and can be set to match one of the environment names.

### `SENTRY_TRACES_SAMPLE_RATE`

!!! tldr "Sentry docs"

    [`traces_sample_rate` config value](https://docs.sentry.io/platforms/python/configuration/options/#traces-sample-rate)

Control the volume of transactions sent to Sentry. Value must be a float in the range `[0.0, 1.0]`.

The default is `0.0` (i.e. no transactions are tracked).
