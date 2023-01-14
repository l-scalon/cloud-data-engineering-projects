#!/bin/bash
sudo mkdir -p /home/ec2-user/tema10/cmd/
sudo cp -f -r /var/lib/jenkins/workspace/tema10/TrilhaDevOpsandCloudBasics/tema10/cmd/run.sh /home/ec2-user/tema10/cmd/
sudo chmod u+x /home/ec2-user/tema10/cmd/run.sh
docker stop tema10c || true && docker rm tema10c || true
