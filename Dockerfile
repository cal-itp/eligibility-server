FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    USER=calitp

     # create $USER and home directory
RUN useradd --create-home --shell /bin/bash $USER && \
    # setup directories and permissions for Flask and gunicorn
    mkdir -p /home/$USER/app/config && \
    mkdir -p /home/$USER/app/run && \
    mkdir -p /home/$USER/app/static && \
    chown -R $USER /home/$USER

# enter app directory
WORKDIR /home/$USER/app

# install tooling: curl, git, jq, ssh
# install python tooling: pip, flake8, debugpy, pre-commit
RUN apt-get update \
    && apt-get install -qq --no-install-recommends curl git jq ssh

# install python app dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir flake8 debugpy pre-commit

# copy source files
COPY . /home/$USER/app/

# switch to non-root $USER
USER $USER

# start app
CMD ["flask", "run", "-h", "0.0.0.0"]
