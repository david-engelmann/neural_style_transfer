#!/bin/bash
# Section to install additional OS packages.
apt-get update && export DEBIAN_FRONTEND=noninteractive \
	&& apt-get -y install --no-install-recommends \
		#autoremove \
		build-essential \
		libpython3-dev \
		libboost-all-dev \
		python3 \
		python3-pip \
		python3-wheel \
		#python${PYTHON_VERSION}-dev \
		#python${PYTHON_VERSION}-venv \
		python3-setuptools \
		python3-dev \
		python3-venv \
	&& apt-get update && apt-get -y upgrade 
exec "$@"