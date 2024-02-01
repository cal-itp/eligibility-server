# Releases

The `eligibility-server` is published as a Docker image on the GitHub Container Registry. It can be accessed from the [repository package page](https://github.com/cal-itp/eligibility-server/pkgs/container/eligibility-server).

Every push to the `main` (default) branch that changes files relevant to the application builds and updates the `dev` package, via the [`docker-publish`](https://github.com/cal-itp/eligibility-server/blob/main/.github/workflows/docker-publish.yml) GitHub Action.

Commits that are tagged with our version number format for release candidates and releases will update the `test` and `prod` packages, respectively.

## Versions

All versions of the package may be viewed on the [package all versions page](https://github.com/cal-itp/eligibility-server/pkgs/container/eligibility-server/versions).

The `main` (default) branch is published at the `dev` tag.

The official releases will be tagged with a version number.

## Version number format

`eligibility-server` uses the [CalVer](https://calver.org/) versioning scheme, where version numbers for releases look like: `YYYY.0M.R`

- `YYYY` is the 4-digit year of the release; e.g. `2021`, `2022`
- `0M` is the 2-digit, 0-padded month of the release; e.g. `02` is February, `12`
  is December.
- `R` is the 1-based release counter for the given year and month;
  e.g. `1` for the first release of the month, `2` for the second, and so on.

Version numbers for release candidates append `-rcR`, where `R` is the 1-based release counter for the anticipated release. For example, the first release candidate for the `2024.01.1` release would be `2024.01.1-rc1`.
