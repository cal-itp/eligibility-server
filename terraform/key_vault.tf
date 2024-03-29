resource "azurerm_key_vault" "main" {
  # name needs to be globally unique
  name                = "${var.AGENCY_CARD}-${local.env_name}"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  sku_name            = "standard"
  tenant_id           = data.azurerm_client_config.current.tenant_id

  soft_delete_retention_days = 90
  purge_protection_enabled   = true

  # allow engineers to fully manage secrets
  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = var.ENGINEERING_GROUP_OBJECT_ID

    secret_permissions = [
      "Backup",
      "Delete",
      "Get",
      "List",
      "Purge",
      "Recover",
      "Restore",
      "Set"
    ]
  }

  # allow the Pipeline to read secrets
  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = var.DEPLOYER_APP_OBJECT_ID

    secret_permissions = [
      "Get"
    ]
  }

  lifecycle {
    prevent_destroy = true
  }
}
