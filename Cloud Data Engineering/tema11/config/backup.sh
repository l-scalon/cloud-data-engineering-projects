#!/bin/bash
sudo python3 backup.py
sudo aws s3 sync . s3://path/to/backups --delete
