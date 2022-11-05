#!/usr/bin/env bash
# set -x

cd /code || exit 1

if [[ $1 == "server" ]]; then
  uvicorn pyxor.main:app --host 0.0.0.0 --port 5001
elif [[ $1 == "bash" ]]; then
  /bin/bash
else
  python3 pyxor/pyxor.py "$@"
fi


