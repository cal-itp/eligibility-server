locals {
  is_prod  = terraform.workspace == "default"
  env_name = local.is_prod ? "prod" : terraform.workspace
}

data "azurerm_resource_group" "main" {
  name = "courtesy-cards-eligibility-${local.env_name}"
}
