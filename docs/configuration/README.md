# Configuring the Eligibility server

The settings that can be overriden are:

- `APP_NAME`: The name set on the Flask app
- `DEBUG_MODE`: Value passed as a keyword argument for `debug` in `app.run`
- `HOST`: Value passed as a keyword argument for `host` in `app.run`
- `LOG_LEVEL`: The log level used in the application's [logging configuration](https://flask.palletsprojects.com/en/2.2.x/logging/). If `DEBUG_MODE` is set to `True`, this will not have any effect.
- `IMPORT_FILE_PATH`*: Must be either CSV or JSON.
- `INPUT_HASH_ALGO`: Must be one of the types available in the [`hashlib` library's `algorithms_available` function](https://docs.python.org/3/library/hashlib.html#hashlib.algorithms_available).

When using a CSV file, the following variables can be configured:

- `CSV_DELIMITER`: specify a custom delimiter or use the default ","
- `CSV_NEWLINE`: specify a newline or use the default of ""
- `CSV_QUOTECHAR`: specify a quote character or use the default of none
- `CSV_QUOTING`: default of 3 (no quotes)

These are the possible values for the `CSV_QUOTING` variable:

- `csv.QUOTE_MINIMAL`: 0 - To be used when the CSV file has quotes around entries which contain special characters such as delimiters, quotechar or any of the characters in lineterminator
- `csv.QUOTE_ALL`: 1 - To be used when all the values in the CSV file are present inside quotation marks
- `csv.QUOTE_NONNUMERIC`: 2 - To be used when the CSV file uses quotes around non-numeric entries
- `csv.QUOTE_NONE`: 3 - To be used when the CSV file does not use quotes around entries

Asterisk * indicates required
