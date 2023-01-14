#!/bin/bash
source /home/ec2-user/venv/bin/activate
command pip install -r /var/lib/jenkins/workspace/tema10/TrilhaDevOpsandCloudBasics/tema10/app/requirements.txt
/home/ec2-user/venv/bin/python /var/lib/jenkins/workspace/tema10/TrilhaDevOpsandCloudBasics/tema10/app/scripts/test.py
