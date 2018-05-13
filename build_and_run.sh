#!/bin/sh

# build react project and then run

./build_react.sh
. ./setenv.sh
python backend.py
