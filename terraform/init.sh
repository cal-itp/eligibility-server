#!/bin/bash

set -e


ENV=$1

if [ $# -ne 1 ]; then
  echo "Usage: $0 <env>"
  exit 1
fi

echo "Setting the subscription for the Azure CLI..."
az account set --subscription="MST IT"

printf "Intializing Terraform...\n\n"
terraform init

printf "\n\nSelecting the Terraform workspace...\n"
# matching logic in pipeline/workspace.py
if [ "$ENV" = "prod" ]; then
  terraform workspace select default
else
  terraform workspace select "$ENV"
fi

echo "Done!"
