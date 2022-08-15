FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    USER=calitp \
    FLASK_APP=eligibility_server/app.py

# create $USER and home directory
RUN useradd --create-home --shell /bin/bash $USER && \
    chown -R $USER /home/$USER

RUN apt-get update \
    && apt-get install -qq --no-install-recommends build-essential \
    && python -m pip install --upgrade pip

# enter app directory
WORKDIR /home/$USER/app

# switch to non-root $USER
USER $USER

# update PATH for local pip installs
ENV PATH "$PATH:/home/$USER/.local/bin"

# install python app dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy source files
COPY . /home/$USER/app/

# start app
ENTRYPOINT ["/bin/bash"]
CMD ["bin/start.sh"]
