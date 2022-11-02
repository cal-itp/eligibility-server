resource "azurerm_service_plan" "main" {
  name                = "eligibility-server"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "P2v2"

  lifecycle {
    ignore_changes = [tags]
  }
}

locals {
  mount_path = "/home/calitp/app/config"
}

resource "azurerm_linux_web_app" "main" {
  # name needs to be globally unique and is more specific because it's used in the app URL
  name                = "mst-courtesy-cards-eligibility-server-${local.env_name}"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id
  https_only          = true

  site_config {
    ftps_state             = "Disabled"
    vnet_route_all_enabled = true
    application_stack {
      docker_image     = "ghcr.io/cal-itp/eligibility-server"
      docker_image_tag = "main"
    }
  }

  app_settings = {
    "ELIGIBILITY_SERVER_SETTINGS" = "${local.mount_path}/settings.py"
  }

  identity {
    identity_ids = []
    type         = "SystemAssigned"
  }

  logs {
    detailed_error_messages = false
    failed_request_tracing  = false

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
    prevent_destroy = true
    ignore_changes  = [tags]
  }
}