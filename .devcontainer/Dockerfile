FROM eligibility_server:latest

# docs requirements are in a separate file for the GitHub Action
COPY docs/requirements.txt docs/requirements.txt
RUN pip install --no-cache-dir -r docs/requirements.txt

# copy files needed
COPY .git .git
COPY eligibility_server/ eligibility_server/
COPY pyproject.toml pyproject.toml

# install devcontainer requirements
RUN pip install -e .[dev,test]
