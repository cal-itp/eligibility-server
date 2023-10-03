terraform {
  // see version in pipeline/azure-pipelines.yml

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0.0, < 4.0.0"
    }
  }

  backend "azurerm" {
    # needs to match pipeline/azure-pipelines.yml
    resource_group_name  = var.TF_RESOURCE_GROUP
    storage_account_name = var.TF_STORAGE_ACCOUNT
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_client_config" "current" {}
