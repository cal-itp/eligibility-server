# Eligibility Server

Server implementation of the [Eligibility Verification API](https://docs.calitp.org/benefits/eligibility-verification/). See
the client implementation in [`benefits`](https://github.com/cal-itp/benefits).

## Getting started

### Create Docker image for server

```bash
docker compose build server
```

### Start development in Dev Container

- Build and Open in Container on VS Code
- Check the Ports tab to find the dynamically-assigned localhost port, or run `docker ps -f name=eligibility-server` and go to `http://localhost:XXXX`

## Tests

### Run tests
```bash
coverage run -m pytest
```

### Check test coverage

```bash
coverage report -m
```

## License

[AGPL-3.0 License](./LICENSE)
