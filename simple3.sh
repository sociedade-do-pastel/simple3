#!/bin/bash

if [ "$#" -eq 2 ]
then
	python3 comple.py "$1" "$2"
else
	python3 comple.py "$1"
fi
