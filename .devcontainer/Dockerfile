FROM eligibility_server:latest

# install python tooling
COPY .devcontainer/requirements.txt .devcontainer/requirements.txt
RUN pip install --no-cache-dir -r .devcontainer/requirements.txt

# install docs tooling
COPY docs/requirements.txt docs/requirements.txt
RUN pip install --no-cache-dir -r docs/requirements.txt

# install test tooling
COPY tests/requirements.txt tests/requirements.txt
RUN pip install -r tests/requirements.txt
