import os

REASON = os.environ["REASON"]
SOURCE = os.environ["SOURCE"]
TARGET = os.environ["TARGET"]

# the branches that correspond to environments
ENV_BRANCHES = ["dev", "test", "prod"]

if REASON == "PullRequest" and TARGET in ENV_BRANCHES:
    # it's a pull requests against one of the environment branches, so use the target branch
    print(TARGET)
elif SOURCE in ENV_BRANCHES:
    # it's being run on one of the environment branches, so use that
    print(SOURCE)
else:
    # default to running against dev
    print("dev")
