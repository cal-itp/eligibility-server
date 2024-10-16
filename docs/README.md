# Home

This website provides technical documentation for the `eligibility-server` application, a part of the [`benefits`](https://docs.calitp.org/benefits) application, from the [California Integrated Travel Project (Cal-ITP)](https://www.calitp.org).

Eligibility Server is open-source software that is designed, developed, and maintained by <a href="https://compiler.la" target="_blank">Compiler LLC</a> on behalf of Caltrans, Cal-ITP, and our agency partners.

## Overview

`eligibility-server` is a [Flask web application](https://flask.palletsprojects.com/) that implements an [Eligibility Verification API](https://docs.calitp.org/eligibility-api/specification/).

The API is designed for privacy and security of user information:

- The API communicates with signed and encrypted JSON Web Tokens containing only the most necessary of user data for the purpose of eligibility verification
- The application requires no user accounts and stores no information about the user
- Interaction with the application is anonymous, with only minimal event tracking for usage and problem analysis

The server is published as a Docker container on the [GitHub Container Registry](https://github.com/cal-itp/eligibility-server/pkgs/container/eligibility-server).

## Getting started with the app

Running the application locally is possible with [Docker and Docker Compose](https://www.docker.com/products/docker-desktop).

### Build the Docker container for local development

```bash
cp .env.sample .env
docker compose build server
```

### Use the Docker container locally

```bash
docker pull ghcr.io/cal-itp/eligibility-server:dev
```
