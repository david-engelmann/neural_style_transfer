#!/bin/bash
# Make venv
apt install -y python3.9-venv
python3 -m venv ${VIRTUAL_ENV}

. $VIRTUAL_ENV/bin/activate

pip3 install --upgrade pip setuptools wheel \
	&& pip3 install --no-cache-dir -r requirements.txt
exec "$@"