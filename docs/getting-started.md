# Getting started

Running the Eligibility Server application in a local, non-production environment requires [Docker](https://docs.docker.com/get-docker/).

## Running the app locally for development

The following commands should be run in a terminal program like `bash`.

### Clone the repository

```bash
git clone https://github.com/cal-itp/eligibility-server.git
cd eligibility-server
```

### Create an environment file

Use the sample as the template.

```bash
cp .env.sample .env
```

The .env file specifies the following value:

- `ELIGIBILITY_SERVER_SETTINGS`: Path to a [Python configuration file](https://flask.palletsprojects.com/en/2.2.x/config/#configuring-from-python-files) which will override default settings

See [Configuration](../configuration) for more details on supported settings.

### Build image using Docker Compose

```bash
docker compose build --no-cache server
```

### Start the server

```bash
docker compose up [-d] server
```

The optional `-d` flag will start in detatched mode and allow you to continue using the terminal session. Otherwise your terminal will be attached to the container’s terminal, showing the startup and runtime output.

After initialization, the server is running on `http://localhost` at a port dynamically assigned by Docker. See [Docker dynamic ports](https://docs.calitp.org/benefits/getting-started/docker-dynamic-ports/) for more information on accessing the site on localhost.

### Run healthcheck

To check if the server is running successfully, use your browser to get to the Healthcheck endpoint: `http://localhost:50252/healthcheck`

The page should read "Healthy"

### Stop the server

```bash
docker compose down
```

## Develop with VS Code Remote Containers

This repository comes with a [VS Code Remote Containers](https://code.visualstudio.com/docs/remote/containers) configuration file.

Once you clone the repository locally, open it within VS Code, which will prompt you to re-open the repository within the Remote Container.

 1. Build and Open the Dev Container
 2. Start the `eligibility-server` Flask app and database with `F5`
 3. Now you can run tests from the container.

Starting the Dev Container will run `bin/init.sh`, which runs a command to initialize the database. More specifically, it creates the database and imports and saves users based on the configured settings.

## Run tests

### Run unit tests

Unit tests are implemented with [`pytest`](https://docs.pytest.org/en/6.2.x/) and can be found in the [`tests/`](https://github.com/cal-itp/eligibility-server/tree/main/tests) directory in the repository. `pytest` is installed and available to run directly in the devcontainer.

The test suite runs against every pull request via a GitHub Action.

### Destroy and recreate database

In testing the database, you may need to teardown the database and restart a database from scratch.

The command below will remove all users and drop the database:

```bash
flask drop-db
```

To set up the database with a new import file or other configuration variables, after making any new environment variable changes, run:

```bash
flask init-db
```

## Run and develop the Documentation

These docs are built and published with GitHub Actions.

To run the docs locally:

```bash
docker compose up docs
```

Read more on how to run the docs [here](https://docs.calitp.org/benefits/getting-started/documentation/).
