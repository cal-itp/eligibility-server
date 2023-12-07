FROM ghcr.io/cal-itp/docker-python-web:main as build_wheel

WORKDIR /build

# upgrade pip
RUN python -m pip install --upgrade pip

COPY . .
RUN git config --global --add safe.directory /build
RUN pip install build && python -m build

FROM ghcr.io/cal-itp/docker-python-web:main as appcontainer

WORKDIR /home/calitp/app

ENV FLASK_APP=eligibility_server.app:app

COPY --from=build_wheel /build/dist ./dist

# copy source files
COPY bin bin
# install source as a package
RUN pip install $(find -name eligibility_server*.whl)

# start app
ENTRYPOINT ["/bin/bash"]
CMD ["bin/start.sh"]
