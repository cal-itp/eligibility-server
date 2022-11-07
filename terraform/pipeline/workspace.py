import os
import sys

REASON = os.environ["REASON"]
# the name of the variable that Azure Pipelines uses for the source branch depends on the type of run, so need to check both
SOURCE = os.environ.get("OTHER_SOURCE") or os.environ["INDIVIDUAL_SOURCE"]
TARGET = os.environ["TARGET"]

# the branches that correspond to environments
ENV_BRANCHES = ["dev", "test", "prod"]

if REASON == "PullRequest" and TARGET in ENV_BRANCHES:
    # it's a pull request against one of the environment branches, so use the target branch
    workspace = TARGET
elif REASON == "IndividualCI" and SOURCE in ENV_BRANCHES:
    # it's being run on one of the environment branches, so use that
    workspace = SOURCE
else:
    # default to running against dev
    workspace = "dev"

# just for troubleshooting
if TARGET is not None:
    deployment_description = f"from {SOURCE} to {TARGET}"
else:
    deployment_description = f"for {SOURCE}"
print(f"Deploying {deployment_description} as a result of {REASON} using workspace {workspace}", file=sys.stderr)

print(workspace)
