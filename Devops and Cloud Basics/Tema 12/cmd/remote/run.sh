#!/bin/bash
chown -R ec2-user /home/ec2-user/
docker start tema12c
docker wait tema12c
docker cp tema12c:/tema12/scripts/output/ /home/ec2-user/
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_REGION=
aws s3 sync /home/ec2-user/output/ s3://path/to/tweets/
