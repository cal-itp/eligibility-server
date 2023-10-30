# Infrastructure

The infrastructure is configured as code via [Terraform](https://www.terraform.io/), for [various reasons](https://techcommunity.microsoft.com/t5/fasttrack-for-azure/the-benefits-of-infrastructure-as-code/ba-p/2069350).

## Architecture

## Resources outside of Terraform

The following things in Azure are managed outside of Terraform:

- Subcriptions
- Active Directory (users, groups, service principals, etc.)
- Service connections
- Configuration files, stored as blobs
- Role assignments

## Environments

| Environment | Azure Resource Group              | Terraform Workspace | Git Branch |
| ----------- | --------------------------------- | ------------------- | ---------- |
| Dev         | `$(AGENCY_RESOURCE_GROUP_PREFIX)-eligibility-dev`  | `dev`               | `dev`      |
| Test        | `$(AGENCY_RESOURCE_GROUP_PREFIX)-eligibility-test` | `test`              | `test`     |
| Prod        | `$(AGENCY_RESOURCE_GROUP_PREFIX)-eligibility-prod` | `default`           | `prod`     |

All resources in these Resource Groups should be reflected in Terraform in this repository. The exceptions are:

- Secrets, such as values under [Key Vault](https://azure.microsoft.com/en-us/services/key-vault/). [`prevent_destroy`](https://developer.hashicorp.com/terraform/tutorials/state/resource-lifecycle#prevent-resource-deletion) is used on these Resources.
- Things managed outside of [Terraform](#resources-outside-of-terraform)

For browsing the [Azure portal](https://portal.azure.com), you can [switch your `Default subscription filter`](https://docs.microsoft.com/en-us/azure/azure-portal/set-preferences).

## Access restrictions

We restrict which IP addresses that can access the app service by using a Web Application Firewall (WAF) configured on a Front Door. There is an exception for the `/healthcheck` and `/static` paths, which can be accessed by any IP address.

The app service itself gives access only to our Front Door and to Azure availability tests.

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
az webapp log tail --resource-group <resource group name> --name <app service name> 2>&1 | grep -v /healthcheck
```

e.g.

```bash
az webapp log tail --resource-group courtesy-cards-eligibility-prod --name mst-courtesy-cards-eligibility-server-prod 2>&1 | grep -v /healthcheck
```

### SCM

Docker logs can be viewed in the Advanced Tools for the instance. The URL pattern is `https://<app service name>.scm.azurewebsites.net/api/logs/docker`

## Making changes

Terraform is [`plan`](https://www.terraform.io/cli/commands/plan)'d when code is pushed to any branch on GitHub, then [`apply`](https://www.terraform.io/cli/commands/apply)'d when merged to `dev`. While other automation for this project is done through GitHub Actions, we use an Azure Pipeline (above) for a couple of reasons:

- Easier authentication with the Azure API using a service connnection
- Log output is hidden, avoiding accidentally leaking secrets

### Local development

1. Get access to the Azure account.
1. Install dependencies:

   - [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
   - [Terraform](https://www.terraform.io/downloads) - see exact version in [`pipeline/deploy.yml`](pipeline/deploy.yml)

1. [Authenticate using the Azure CLI](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/azure_cli).

   ```sh
   az login
   ```

1. Outside the [dev container](https://docs.calitp.org/eligibility-server/getting-started/), navigate to the `terraform/` directory.
1. Create a [`terraform.tfvars` file](https://developer.hashicorp.com/terraform/language/values/variables#variable-definitions-tfvars-files) and specify the [variables](variables.tf).
1. [Initialize Terraform.](https://www.terraform.io/cli/commands/init) You can also use this script later to switch between [environments](#environments).

   ```sh
   ./init.sh <env> <agency>
   ```

1. Make changes to Terraform files.
1. Preview the changes, as necessary.

   ```sh
   terraform plan
   ```

1. Submit the changes via pull request.

## Azure environment setup

The steps we took to set up MST's environment are documented in [a separate Google Doc](https://docs.google.com/document/d/12uzuKyvyabHAOaeQc6k2jQIG5pQprdEyBpfST_dY2ME/edit#heading=h.1vs880ltbo58).

In general, the steps that must be done manually before the pipeline can be run are:

- Create an Azure DevOps organization and project
- Request a free grant of parallel jobs using the form at [https://aka.ms/azpipelines-parallelism-request](https://aka.ms/azpipelines-parallelism-request)
- Create Resource Group and storage account dedicated to the Terraform state
- Create container in storage account for Terraform state
- Create environment Resource Group for each environment, Region: West US
    - We create these manually to avoid having to give the pipeline service connection permissions for creating resource groups
- Create Terraform workspace for each environment
- Trigger a pipeline run to verify `plan` and `apply`
- Known chicken-and-egg problem: Terraform both creates the Key Vault and expects a secret within it, so will always fail on the first deploy. Add the Benefits slack email secret and re-run the pipeline.

Once the pipeline has run, there are a few more steps to be done manually in the Azure portal. These are related to configuring the service principal used for ETL:

- [Create the service principal](https://learn.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#app-registration-app-objects-and-service-principals)
- Give the ETL service principal access to the `prod` storage account created by the pipeline:
    - Navigate to the storage account
    - Select **Access Control (IAM)**
    - Select **Add**, then select **Add role assignment**
    - In the **Role** tab, select `Storage Blob Data Contributor`
    - In the **Members** tab, select `Select Members` and search for the ETL service principal. Add it to the role.
    - Also in the **Members** tab, add a description of `This role assignment gives write access only for the path of the hashed data file.`
    - In the **Conditions** tab, select **Add condition** and change the editor type to `Code`
    - Add the following condition into the editor, filling in `<filename>` with the appropriate value:

```text
(
 (
  @Resource[Microsoft.Storage/storageAccounts/blobServices/containers/blobs:path] StringLike '<filename>'
 )
)
```
