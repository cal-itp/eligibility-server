# Configuring the Eligibility server

The [Getting Started](./getting-started) section mentions [copying `.env.sample` to `.env` as a template](./getting-started.md#create-an-environment-file). These sample values are sufficient to configure the server to be run locally.

If you want to run with different settings, you should:

1. Create a new Python configuration file in the `config` directory
1. Provide a value for [`IMPORT_FILE_PATH`](./settings.md#import_file_path) (required) and any other settings you want to override (optional)
1. Set the `ELIGIBILITY_SERVER_SETTINGS` environment variable to the path of your new file

!!! note
The Eligibility server loads in settings using Flask's methods for [Configuration Handling](https://flask.palletsprojects.com/en/2.2.x/config/).

!!! important
The default settings that will always be loaded are in [eligibility_server/settings.py](https://github.com/cal-itp/eligibility-server/blob/dev/eligibility_server/settings.py)
