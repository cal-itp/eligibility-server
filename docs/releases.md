# Releases

The `eligibility-server` is published as a Docker image on the GitHub Container Registry. It can be accessed from the [repository package page](https://github.com/cal-itp/eligibility-server/pkgs/container/eligibility-server).

Every push to the `main` (default) branch that changes files relevant to the application builds and updates the `dev` package, via the [`docker-publish`](https://github.com/cal-itp/eligibility-server/blob/main/.github/workflows/docker-publish.yml) GitHub Action.

Every release created also pushes a new package publication.

## Versions

All versions of the package may be viewed on the [package all versions page](https://github.com/cal-itp/eligibility-server/pkgs/container/eligibility-server/versions).

The `main` (default) branch is published at the `dev` tag:

The official releases will be tagged with a version number and their respective environment (`test`, `prod`) tag.
