#!/bin/bash
amazon-linux-extras install docker -y
systemctl enable docker
systemctl start docker
cd /home/ec2-user/tema12/app/
docker build -t tema12 .
docker create --name tema12c tema12
