FROM eligibility_server:latest

# install Terraform
USER root
COPY .devcontainer/install_terraform.sh .devcontainer/install_terraform.sh
RUN ./.devcontainer/install_terraform.sh
# switch to non-root $USER
USER $USER

# install python tooling
COPY .devcontainer/requirements.txt .devcontainer/requirements.txt
RUN pip install --no-cache-dir -r .devcontainer/requirements.txt

# install docs tooling
COPY docs/requirements.txt docs/requirements.txt
RUN pip install --no-cache-dir -r docs/requirements.txt

# install test tooling
COPY tests/requirements.txt tests/requirements.txt
RUN pip install -r tests/requirements.txt
