#!/bin/bash
docker start tema10c
docker wait tema10c
docker cp tema10c:/tema10/scripts/tweets/ /home/ec2-user/
aws s3 sync /home/ec2-user/tweets/ s3://jt-dataeng-lucasscalon/devopsandcloudbasics/tweets/
