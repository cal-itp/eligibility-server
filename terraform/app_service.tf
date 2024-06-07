resource "azurerm_service_plan" "main" {
  name                = "eligibility-server"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

locals {
  mount_path = "/home/calitp/app/config"
}

resource "azurerm_linux_web_app" "main" {
  # name needs to be globally unique and is more specific because it's used in the app URL
  name                = "${var.AGENCY_CARD}-eligibility-server-${local.env_name}"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id
  https_only          = true

  site_config {
    always_on     = false
    ftps_state    = "Disabled"
    http2_enabled = true

    vnet_route_all_enabled = true

    ip_restriction {
      name        = "Front Door"
      priority    = 100
      action      = "Allow"
      service_tag = "AzureFrontDoor.Backend"
      headers {
        x_azure_fdid = [azurerm_cdn_frontdoor_profile.main.resource_guid]
      }
    }

    ip_restriction {
      name        = "Availability Test"
      priority    = 200
      action      = "Allow"
      service_tag = "ApplicationInsightsAvailability"
    }
  }

  app_settings = {
    "DOCKER_ENABLE_CI"            = "false",
    "DOCKER_REGISTRY_SERVER_URL"  = "https://ghcr.io/"
    "ELIGIBILITY_SERVER_SETTINGS" = "${local.mount_path}/settings.py"
    # this prevents the filesystem from being obscured by a mount
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "WEBSITES_PORT"                       = "8000"
    "WEBSITES_CONTAINER_START_TIME_LIMIT" = "1800"

    # Sentry
    "SENTRY_ENVIRONMENT" = "${local.env_name}"
  }

  identity {
    identity_ids = []
    type         = "SystemAssigned"
  }

  logs {
    detailed_error_messages = true
    failed_request_tracing  = true

    http_logs {
      file_system {
        retention_in_days = 99999
        retention_in_mb   = 100
      }
    }
  }

  storage_account {
    access_key   = azurerm_storage_account.main.primary_access_key
    account_name = azurerm_storage_account.main.name
    name         = "eligibility-server-config"
    type         = "AzureBlob"
    share_name   = azurerm_storage_container.config.name
    mount_path   = local.mount_path
  }

  lifecycle {
    ignore_changes = [
      # tags get created for Application Insights
      # https://github.com/hashicorp/terraform-provider-azurerm/issues/16569
      tags
    ]
  }
}
