# Home

This website provides technical documentation for the `eligibility-server` application, a part of the `benefits` application, from the California Integrated Travel Project (Cal-ITP).

Documentation for the `main` (default) branch is available [online](https://docs.calitp.org/benefits).

## Overview

### Getting started with the app

```bash
docker-compose build server
```

### Getting started with the docs

#### Build the docs image

```bash
docker build -t docs -f docs/Dockerfile .
```

#### Run the docs locally

```bash
docker run -p 8000:8000 docs
```

### Deploy and publish docs
