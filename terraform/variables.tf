# Some of these are defined in <agency name>/azure-vars.yml. Others are defined in Azure DevOps UI.

# needs to be uppercase "because Azure DevOps will always transform pipeline variables to uppercase environment variables"
# https://gaunacode.com/terraform-input-variables-using-azure-devops

variable "AGENCY_CARD" {
  description = "The name of the agency's card program"
  type        = string
}

variable "AGENCY_RESOURCE_GROUP_PREFIX" {
  description = "The prefix to the name of the resource group for each environment"
  type        = string
}

variable "AGENCY_STORAGE_ACCOUNT_PREFIX" {
  description = "The prefix to the name of the storage account for each environment"
  type        = string
}

variable "DEPLOYER_APP_OBJECT_ID" {
  description = "Object ID from the Azure DevOps deployer service principal application in Active Directory"
  type        = string
}

variable "ENGINEERING_GROUP_OBJECT_ID" {
  description = "Object ID from the engineering group (cal-itp-compiler) in Azure Active Directory"
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
