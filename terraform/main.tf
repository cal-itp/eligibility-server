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
    resource_group_name  = "courtesy-cards-eligibility-terraform"
    storage_account_name = "courtesycardsterraform"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_client_config" "current" {}
