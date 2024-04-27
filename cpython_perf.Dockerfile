FROM debian:12 AS python-base
ADD https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tgz /
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gdb \
    lcov \
    libbz2-dev \
    libffi-dev \
    libgdbm-compat-dev \
    libgdbm-dev \
    liblzma-dev \
    libncurses5-dev \
    libreadline6-dev \
    libsqlite3-dev \
    libssl-dev \
    lzma \
    lzma-dev \
    pkg-config \
    tk-dev \
    uuid-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/* && \
    tar -xvf Python-3.12.3.tgz && \
    cd Python-3.12.3 && \
    ./configure --enable-optimizations --with-lto && \
    make -j$(nproc) && \
    make altinstall && \
    cd ../ && \
    rm -rf Python-3.12.3.tgz Python-3.12.3 && \
    ln -s -f /usr/local/bin/python3.12 /usr/local/bin/python && \
    ln -s -f /usr/local/bin/pip3.12 /usr/local/bin/pip

########## BASE ########################################################################

FROM python-base AS base
WORKDIR /onebrc/
COPY ./ ./
RUN apt-get update && apt-get upgrade -y \
    && ./scripts/install_meta_packages.sh --install-system-common-packages \
    && groupadd -r python \
    && useradd --create-home --system --gid python python \
    && chown -R python /onebrc/
USER python
ENV PATH="/home/python/.local/bin:${PATH}"
RUN pip install --upgrade pip

########## BUILD #######################################################################

FROM base AS package-build
RUN ./scripts/install_meta_packages.sh --install-pip-build-packages  \
    && python -m build --wheel

FROM base AS build
COPY --chown=python --from=package-build /onebrc/dist/ dist/
RUN pip install --user --no-cache-dir --find-links dist/ onebrc

FROM build AS build-slim
RUN rm -r *
COPY --chown=python Makefile ./

########## MAIN ########################################################################

FROM build-slim AS prod
CMD ["tail", "-f", "/dev/null"]
