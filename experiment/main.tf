terraform {
  // see version in experiment-pipeline.yml
  required_version = ">= 1.1.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0.0, < 4.0.0"
    }
  }

  backend "azurerm" {
    # needs to match experiment-pipeline.yml
    resource_group_name  = "experiment-terraform"
    storage_account_name = "experimentterraform"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }

}

provider "azurerm" {
  features {}
}

locals {
  is_prod  = terraform.workspace == "default"
  is_test  = terraform.workspace == "test"
  env_name = local.is_prod ? "prod" : terraform.workspace
}

resource "azurerm_resource_group" "rg" {
  name     = "myTFResourceGroup-${local.env_name}"
  location = "westus2"
}
