#!/bin/bash
source /home/ec2-user/venv/bin/activate
sudo chown -R ec2-user /home/ec2-user/
command pip install -r /var/lib/jenkins/workspace/tema09/TrilhaDevOpsandCloudBasics/tema09/Scripts/requirements.txt
