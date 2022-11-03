resource "azurerm_role_assignment" "velocity_etl" {
  count = local.is_prod ? 1 : 0

  description          = "This role assignment gives write access only for the path of the hashed data file."
  scope                = azurerm_storage_container.config.resource_manager_id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = var.VELOCITY_ETL_SERVICE_PRINCIPAL_ID
  condition            = <<EOF
(
 (
  @Resource[Microsoft.Storage/storageAccounts/blobServices/containers/blobs:path] StringLike 'velocity.csv'
 )
)
EOF
  condition_version    = "2.0"
}
