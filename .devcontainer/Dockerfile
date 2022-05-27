FROM eligibility_server:latest

USER root

# install container tooling
RUN apt-get update \
    && apt-get install -qq --no-install-recommends curl git jq ssh build-essential \
    && python -m pip install --upgrade pip

# install python tooling
RUN pip install --no-cache-dir flake8 pre-commit

# install docs tooling
COPY docs/requirements.txt docs/requirements.txt
RUN pip install --no-cache-dir -r docs/requirements.txt

# install test tooling
COPY tests/requirements.txt tests/requirements.txt
RUN pip install -r tests/requirements.txt
