FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    gcc \
    g++ \
    make \
    curl \
    ca-certificates \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir \
    ipykernel \
    jupyterlab \
    pytest \
    numpy \
    pandas \
    scipy \
    matplotlib \
    seaborn \
    scikit-learn \
    openpyxl \
    xarray \
    polars \
    cartopy \
    cmocean \
    geopy \
    gsw \
    netcdf4 \
    h5netcdf \
    plotly

WORKDIR /workspaces