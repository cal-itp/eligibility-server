FROM ghcr.io/cal-itp/docker-python-web:main as build_wheel

WORKDIR /build

# upgrade pip
RUN python -m pip install --upgrade pip

COPY . .
RUN git config --global --add safe.directory /build

RUN mkdir -p static

# build as root user so unnecessary files are not copied into tarball
USER root
RUN pip install build && python -m build

FROM ghcr.io/cal-itp/docker-python-web:main as appcontainer

WORKDIR /home/calitp/app

# upgrade pip
RUN python -m pip install --upgrade pip

ENV FLASK_APP=eligibility_server.app:app

COPY --from=build_wheel /build/dist /build/dist
COPY --from=build_wheel /build/static static

# copy source files
COPY bin bin
# install source as a package
RUN pip install $(find /build/dist -name eligibility_server*.whl)

# start app
ENTRYPOINT ["/bin/bash"]
CMD ["bin/start.sh"]
