FROM ghcr.io/cal-itp/docker-python-web:main

ENV FLASK_APP=eligibility_server/app.py

# upgrade pip
RUN python -m pip install --upgrade pip

# copy source files
COPY bin bin
COPY eligibility_server/ eligibility_server/
COPY pyproject.toml pyproject.toml

# install source as a package
RUN pip install -e .

# start app
ENTRYPOINT ["/bin/bash"]
CMD ["bin/start.sh"]
