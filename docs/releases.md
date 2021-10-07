# Releases

The `eligibility-server` is published as a Docker image on the GitHub Container Registry. It can be accessed [here](https://github.com/cal-itp/eligibility-server/pkgs/container/eligibility-server).

Every push to the `main` (default) branch that changes files relevant to the application builds and updates the `main` package, via the [`docker-publish`](https://github.com/cal-itp/eligibility-server/blob/main/.github/workflows/docker-publish.yml) GitHub Action.

Every release created also pushes a new package publication.

## Versions

All versions of the package may be viewed [here](https://github.com/cal-itp/eligibility-server/pkgs/container/eligibility-server/versions).

The `main` (default) branch is published at the `main` tag:

The official releases will be tagged with a version number and the `latest` tag.
