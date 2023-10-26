#!/bin/bash

set -e


ENV="$1"
AGENCY="$2"

if [ $# -ne 2 ]; then
  echo "Usage: $0 <env> <agency>"
  exit 1
fi

source "$AGENCY/local.env"

echo "Setting the subscription for the Azure CLI..."
az account set --subscription="$SUBSCRIPTION"

printf "Intializing Terraform...\n\n"
terraform init -backend-config="$AGENCY/local.tfbackend"

printf "\n\nSelecting the Terraform workspace...\n"

# matching logic in pipeline/workspace.py
WORKSPACE=$([[ "$ENV" == "prod" ]] && echo "default" || echo "$ENV")

# if the workspace exists, this check will select it
WORKSPACE_EXISTS=$(terraform workspace select "$WORKSPACE" 2> /dev/null; echo $?)
# creating a new workspace also selects it
if [ "$WORKSPACE_EXISTS" -ne 0 ]; then
  terraform workspace new "$WORKSPACE"
fi

echo "Done!"
