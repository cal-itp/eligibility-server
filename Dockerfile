FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    USER=calitp \
    FLASK_APP=eligibility_server/app.py

     # create $USER and home directory
RUN useradd --create-home --shell /bin/bash $USER && \
    chown -R $USER /home/$USER

# enter app directory
WORKDIR /home/$USER/app

# install python app dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy source files
COPY . /home/$USER/app/

# switch to non-root $USER
USER $USER

# start app
ENTRYPOINT ["/bin/bash"]
CMD ["bin/start.sh"]
