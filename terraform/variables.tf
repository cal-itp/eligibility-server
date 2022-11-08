# needs to be uppercase "because Azure DevOps will always transform pipeline variables to uppercase environment variables"
# https://gaunacode.com/terraform-input-variables-using-azure-devops
variable "VELOCITY_ETL_SERVICE_PRINCIPAL_ID" {
  description = "Object ID from the registered application for the Velocity server ETL uploading: https://cloudsight.zendesk.com/hc/en-us/articles/360016785598-Azure-finding-your-service-principal-object-ID"
}
variable "IP_ADDRESS_WHITELIST" {
  description = "List of IP addresses allowed to connect to the app service."
  type        = list(string)
}
