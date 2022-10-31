resource "azurerm_key_vault" "main" {
  name                = "eligibility-server"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  sku_name            = "standard"
  tenant_id           = data.azurerm_client_config.current.tenant_id

  lifecycle {
    prevent_destroy = true
    ignore_changes  = [tags]
  }
}
