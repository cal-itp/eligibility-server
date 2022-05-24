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
 2. Start the `eligibility-server` app with `F5`

## Set up database and run unit tests

To run the API, you will have to

To set up the database:

```bash
python setup.py
```

To tear down the database:

```bash
python teardown.py
```

### Run unit tests

Unit tests are implemented with [`pytest`](https://docs.pytest.org/en/6.2.x/) and can be found in the [`tests/`](https://github.com/cal-itp/eligibility-server/tree/main/tests) directory in the repository.

The test suite runs against every pull request via a GitHub Action.

`pytest` is installed and available to run directly in the devcontainer.

Once you have the app running locally:

1. From the main directory, run `coverage run -m pytest -m databasetest; coverage run -m pytest -m settingstest`
2. To see the test coverage report, run `coverage report -m`

## Run and develop the Documentation

These docs are built and published with GitHub Actions.

To run the docs locally:

```bash
docker compose up docs
```

Read more on how to run the docs [here](https://docs.calitp.org/benefits/getting-started/documentation/).
