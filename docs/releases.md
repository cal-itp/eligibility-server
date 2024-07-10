# Releases

The `eligibility-server` is published as a Docker image on the GitHub Container Registry. It can be accessed from the [repository package page](https://github.com/cal-itp/eligibility-server/pkgs/container/eligibility-server).

Every push to the `main` (default) branch that changes files relevant to the application builds and pushes a new package tagged with the corresponding Git commit hash, via the [`docker-publish`](https://github.com/cal-itp/eligibility-server/blob/main/.github/workflows/docker-publish.yml) GitHub Action.

Commits that are tagged with our version number format for release candidates and releases will also push a new package.

## Versions

All versions of the package may be viewed on the [package all versions page](https://github.com/cal-itp/eligibility-server/pkgs/container/eligibility-server/versions).

## Version number format

`eligibility-server` uses the [CalVer](https://calver.org/) versioning scheme, where version numbers for releases look like: `YYYY.0M.R`

- `YYYY` is the 4-digit year of the release; e.g. `2021`, `2022`
- `0M` is the 2-digit, 0-padded month of the release; e.g. `02` is February, `12`
  is December.
- `R` is the 1-based release counter for the given year and month;
  e.g. `1` for the first release of the month, `2` for the second, and so on.

Version numbers for release candidates append `-rcR`, where `R` is the 1-based release counter for the anticipated release. For example, the first release candidate for the `2024.01.1` release would be `2024.01.1-rc1`.

## Making a release

This list outlines the manual steps needed to make a new release of `eligibility-server`.

A release is made by pushing an annotated tag. The name of the tag must use the version number format mentioned above. This kicks off a deployment to the production environment and creates a GitHub release. The version number for the app and the release will be the tag's name.

More details about the deployment steps and release creation can be found in the [`docker-publish`](https://github.com/cal-itp/eligibility-server/tree/main/.github/workflows/docker-publish.yml) workflow. [`release`](https://github.com/cal-itp/eligibility-server/tree/main/.github/workflows/release.yml) workflow.

The list of releases can be found on the [repository Releases page](https://github.com/cal-itp/eligibility-server/tags) on GitHub.

[Start a new Release on Github](https://github.com/cal-itp/eligibility-server/issues/new?labels=release&template=release.yml&title=Make+a+Release){ .md-button }
