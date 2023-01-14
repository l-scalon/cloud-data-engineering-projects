#!/bin/bash
source /path/to/venv/bin/activate
python /path/to/Scripts/main.py
aws s3 sync /path/to/Scripts/tweets/ s3://path/to/tweets/