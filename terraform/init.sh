#!/bin/bash

set -e


ENV=$1

echo "Setting the subscription for the Azure CLI..."
az account set --subscription="Azure subscription 1"

printf "Intializing Terraform...\n\n"
terraform init

printf "\n\nSelecting the Terraform workspace...\n"
if [ "$ENV" = "prod" ]; then
  terraform workspace select default
else
  terraform workspace select "$ENV"
fi

echo "Done!"
