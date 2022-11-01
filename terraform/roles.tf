resource "azurerm_role_definition" "velocity_etl" {
  name        = "Velocity ETL"
  scope       = azurerm_storage_container.config.resource_manager_id
  description = "This is a custom role created via Terraform for the Velocity ETL service principal to upload the hashed data file"

  permissions {
    data_actions = ["Microsoft.Storage/storageAccounts/blobServices/containers/blobs/write"]
  }
}

# resource "azurerm_role_assignment" "velocity_etl" {
#   description = "This role assignment gives write access only for the path of the hashed data file."
#   scope              = azurerm_storage_container.config.resource_manager_id
#   role_definition_id = azurerm_role_definition.velocity_etl.role_definition_resource_id
#   principal_id       = "todo"
#   condition          = <<EOF
# (
#  (
#   !(ActionMatches{'Microsoft.Storage/storageAccounts/blobServices/containers/blobs/write'})
#  )
#  OR
#  (
#   @Resource[Microsoft.Storage/storageAccounts/blobServices/containers/blobs:path] StringEquals 'velocity.csv'
#  )
# )
# EOF
#   condition_version = "2.0"
# }
