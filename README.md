# Eligibility Verification Server for Benefits

Transit benefits enrollment, minus the paperwork.

This server can be used for testing `benefits` with only local resources via the service defined in [`localhost/docker-compose.yml`](https://github.com/cal-itp/benefits/blob/dev/localhost/docker-compose.yml#L56). Read more about [running the test verification server](https://docs.calitp.org/benefits/getting-started/test-verification-server/).

View the technical documentation online: <https://docs.calitp.org/benefits>

## Getting started

### Create Docker image for server

```bash
docker compose build server
```

### Start development in Dev Container

- Build and Open in Container on VS Code

## Tests

### To run tests

```bash
coverage run -m pytest
```

### To see coverage

```bash
coverage report -m
```
## License

[AGPL-3.0 License](./LICENSE)
