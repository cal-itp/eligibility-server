# needs to be uppercase "because Azure DevOps will always transform pipeline variables to uppercase environment variables"
# https://gaunacode.com/terraform-input-variables-using-azure-devops

variable "DEPLOYER_APP_OBJECT_ID" {
  description = "Object ID from the Azure DevOps deployer service principal application in Active Directory"
  type        = string
}

variable "ENGINEERING_GROUP_OBJECT_ID" {
  description = "Object ID from the engineering group (cal-itp-compiler) in Azure Active Directory"
  type        = string
}

variable "VELOCITY_ETL_APP_OBJECT_ID" {
  description = "Object ID from the registered application for the Velocity server ETL uploading: https://cloudsight.zendesk.com/hc/en-us/articles/360016785598-Azure-finding-your-service-principal-object-ID"
  type        = string
}

variable "IP_ADDRESS_WHITELIST_DEV" {
  description = "List of IP addresses allowed to connect to the app service, in CIDR notation: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/linux_web_app#ip_address. By default, all IP addresses are allowed."
  type        = list(string)
  default     = []
}

variable "IP_ADDRESS_WHITELIST_TEST" {
  description = "List of IP addresses allowed to connect to the app service, in CIDR notation: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/linux_web_app#ip_address. By default, all IP addresses are allowed."
  type        = list(string)
  default     = []
}

variable "IP_ADDRESS_WHITELIST_PROD" {
  description = "List of IP addresses allowed to connect to the app service, in CIDR notation: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/linux_web_app#ip_address. By default, all IP addresses are allowed."
  type        = list(string)
  default     = []
}

variable "TF_RESOURCE_GROUP" {
  description = "The name of the resource group used for Terraform backend"
  type        = string
}

variable "TF_STORAGE_ACCOUNT" {
  description = "The name of the storage account used for Terraform backend"
  type        = string
}
