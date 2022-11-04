# Infrastructure

The infrastructure is configured as code via [Terraform](https://www.terraform.io/), for [various reasons](https://techcommunity.microsoft.com/t5/fasttrack-for-azure/the-benefits-of-infrastructure-as-code/ba-p/2069350).

## Architecture

## Resources outside of Terraform

The following things in Azure are managed outside of Terraform:

- Subcriptions
- Active Directory (users, groups, service principals, etc.)
- Service connections
- Configuration files, stored as blobs

## Environments

| Environment | Azure Resource Group              | Terraform Workspace | Git Branch |
| ----------- | --------------------------------- | ------------------- | ---------- |
| Dev         | `courtesy-cards-eligibility-dev`  | `dev`               | `dev`      |
| Test        | `courtesy-cards-eligibility-test` | `test`              | `test`     |
| Prod        | `courtesy-cards-eligibility-prod` | `default`           | `prod`     |

All resources in these Resource Groups should be reflected in Terraform in this repository. The exceptions are:

- Secrets, such as values under [Key Vault](https://azure.microsoft.com/en-us/services/key-vault/). [`prevent_destroy`](https://developer.hashicorp.com/terraform/tutorials/state/resource-lifecycle#prevent-resource-deletion) is used on these Resources.
- Things managed outside of [Terraform](#resources-outside-of-terraform)

For browsing the [Azure portal](https://portal.azure.com), you can [switch your `Default subscription filter`](https://docs.microsoft.com/en-us/azure/azure-portal/set-preferences).

## Monitoring

We have [ping tests](https://docs.microsoft.com/en-us/azure/azure-monitor/app/monitor-web-app-availability) set up to notify about availability of each environment. Alerts go to [#benefits-notify](https://cal-itp.slack.com/archives/C022HHSEE3F).

## Logs

Logs can be found a couple of places:

### Azure App Service Logs

[Open the `Logs` for the environment you are interested in.](https://docs.google.com/document/d/11EPDIROBvg7cRtU2V42c6VBxcW_o8HhcyORALNtL_XY/edit#heading=h.6pxjhslhxwvj) The following tables are likely of interest:

- `AppServiceConsoleLogs`: `stdout` and `stderr` coming from the container
- `AppServiceHTTPLogs`: requests coming through App Service
- `AppServicePlatformLogs`: deployment information

For some pre-defined queries, click `Queries`, then `Group by: Query type`, and look under `Query pack queries`.

### [Azure Monitor Logs](https://docs.microsoft.com/en-us/azure/azure-monitor/logs/data-platform-logs)

[Open the `Logs` for the environment you are interested in.](https://docs.google.com/document/d/11EPDIROBvg7cRtU2V42c6VBxcW_o8HhcyORALNtL_XY/edit#heading=h.n0oq4r1jo7zs)

The following [tables](https://docs.microsoft.com/en-us/azure/azure-monitor/app/opencensus-python#telemetry-type-mappings) are likely of interest:

- `requests`
- `traces`

In the latter two, you should see recent log output. Note [there is some latency](https://docs.microsoft.com/en-us/azure/azure-monitor/logs/data-ingestion-time).

See [`Failures`](https://docs.microsoft.com/en-us/azure/azure-monitor/app/asp-net-exceptions#diagnose-failures-using-the-azure-portal) in the sidebar (or `exceptions` under `Logs`) for application errors/exceptions.

### Live tail

After [setting up the Azure CLI](#making-changes), you can use the following command to [stream live logs](https://docs.microsoft.com/en-us/azure/app-service/troubleshoot-diagnostic-logs#in-local-terminal):

```sh
az webapp log tail --resource-group courtesy-cards-eligibility-prod --name mst-courtesy-cards-eligibility-server-prod 2>&1 | grep -v /healthcheck
```

### SCM

[Docker logs](https://mst-courtesy-cards-eligibility-server-dev.scm.azurewebsites.net/api/logs/docker)

## Making changes

[![Build Status](https://dev.azure.com/mstransit/courtesy-cards/_apis/build/status/cal-itp.eligibility-server?branchName=dev)](https://dev.azure.com/mstransit/courtesy-cards/_build/latest?definitionId=1&branchName=dev)

Terraform is [`plan`](https://www.terraform.io/cli/commands/plan)'d when code is pushed to any branch on GitHub, then [`apply`](https://www.terraform.io/cli/commands/apply)'d when merged to `dev`. While other automation for this project is done through GitHub Actions, we use an Azure Pipeline (above) for a couple of reasons:

- Easier authentication with the Azure API using a service connnection
- Log output is hidden, avoiding accidentally leaking secrets

### Local development

1. Get access to the Azure account.
1. Install dependencies:

   - [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
   - [Terraform](https://www.terraform.io/downloads) - see exact version in [`azure-pipelines.yml`](azure-pipelines.yml)

1. [Authenticate using the Azure CLI](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/azure_cli).

   ```sh
   az login
   ```

1. Outside the [dev container](https://docs.calitp.org/eligibility-server/getting-started/), navigate to the `terraform/` directory.
1. Create a `terraform.tfvars` file and specify the [variables](variables.tf):

   ```hcl
   VELOCITY_ETL_SERVICE_PRINCIPAL_ID = "..."
   ```

1. [Initialize Terraform.](https://www.terraform.io/cli/commands/init) You can also use this script later to switch between [environments](#environments).

   ```sh
   ./init.sh <env>
   ```

1. Make changes to Terraform files.
1. Preview the changes, as necessary.

   ```sh
   terraform plan
   ```

1. Submit the changes via pull request.

## Azure environment setup

The steps we took to set up MST's environment are documented in [a separate Google Doc](https://docs.google.com/document/d/12uzuKyvyabHAOaeQc6k2jQIG5pQprdEyBpfST_dY2ME/edit#heading=h.1vs880ltbo58).

This is not a complete step-by-step guide; more a list of things to remember. This may be useful as part of incident response.
