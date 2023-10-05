#!/bin/bash

set -e


ENV="$1"
AGENCY="$2"

if [ $# -ne 2 ]; then
  echo "Usage: $0 <env> <agency>"
  exit 1
fi

source "$AGENCY/env"

echo "Setting the subscription for the Azure CLI..."
az account set --subscription="$SUBSCRIPTION"

printf "Intializing Terraform...\n\n"
terraform init -backend-config="$AGENCY/config.azurerm.tfbackend"

printf "\n\nSelecting the Terraform workspace...\n"
# matching logic in pipeline/workspace.py
if [ "$ENV" = "prod" ]; then
  terraform workspace select default
else
  terraform workspace select "$ENV"
fi

echo "Done!"
