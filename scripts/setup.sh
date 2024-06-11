#!/bin/sh

python3 -m venv ./venv
source ./env/bin/activate
python3 -m pip install pip
pip3 install -r requirements.txt

# psql -h localhost -U root -f db.sql (we already do that process in app/database/config.py)

sh run.sh
