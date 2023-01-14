#!/bin/bash
source /home/ec2-user/venv/bin/activate
python /home/ec2-user/tema09/Scripts/main.py
aws s3 sync /home/ec2-user/tema09/Scripts/tweets/ s3://jt-dataeng-lucasscalon/devopsandcloudbasics/tweets/
