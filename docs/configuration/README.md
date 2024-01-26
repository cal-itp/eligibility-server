# Configuring the Eligibility server

The [Getting Started](./getting-started) section mentions [copying `.env.sample` to `.env` as a template](./getting-started.md#create-an-environment-file). These sample values are sufficient to configure the server to be run locally.

If you want to run with different settings, you should:

1. Create a new Python configuration file in the `config` directory
1. Provide a value for [`IMPORT_FILE_PATH`](./settings.md#import_file_path) (required) and any other settings you want to override (optional)
1. Set the `ELIGIBILITY_SERVER_SETTINGS` environment variable to the path of your new file

!!! note

    The Eligibility server loads in settings using Flask's methods for [Configuration Handling](https://flask.palletsprojects.com/en/2.3.x/config/).

!!! note

    The default settings that will always be loaded are in [eligibility_server/settings.py](https://github.com/cal-itp/eligibility-server/blob/main/eligibility_server/settings.py)

## Creating a new keypair

!!! warning

    The sample keys cannot be used for production. You must create and use a new keypair.

To create a new keypair, start by creating the private key e.g. using [OpenSSL](https://www.openssl.org/docs/man3.1/man1/openssl-genrsa.html):

```console
openssl genrsa -out private.pem -traditional 4096
```

Next, extract the public key e.g. using [OpenSSL](https://www.openssl.org/docs/man3.1/man1/openssl-rsa.html):

```console
openssl rsa -in private.pem -pubout -out public.pem
```

Now there are two files:

- The private key, kept secret for this server instance only: `private.pem`
- The public key, shared with all clients of this server: `public.pem`

The server instance also needs a public key reference from its client, so the above process should be repeated on the client-
side and the client's _public key_ should be shared with the server.
