FROM python:3.12.3-slim-bookworm AS python-base

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
