FROM ghcr.io/cal-itp/docker-python-web:main

ENV FLASK_APP=eligibility_server/app.py

# install python app dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy source files
COPY bin/ bin/
COPY eligibility_server/ eligibility_server/
COPY *.py .

# start app
ENTRYPOINT ["/bin/bash"]
CMD ["bin/start.sh"]
