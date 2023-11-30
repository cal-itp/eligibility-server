FROM eligibility_server:latest

# docs requirements are in a separate file for the GitHub Action
COPY docs/requirements.txt docs/requirements.txt
RUN pip install --no-cache-dir -r docs/requirements.txt

# install devcontainer requirements
COPY .git .git
RUN pip install -e .[dev,test]
