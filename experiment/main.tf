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
