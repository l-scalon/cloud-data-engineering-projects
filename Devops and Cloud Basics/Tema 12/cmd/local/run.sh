#!/bin/bash
cd /var/lib/jenkins/workspace/tema12/terraform/
output=$(terraform output "public_dns")
public_dns=`echo "$output" | tr -d '"'`
cd /home/ec2-user/tema12/
ssh -i "terraformkp.pem" ec2-user@$public_dns -o StrictHostKeyChecking=no "cd /home/ec2-user/tema12/cmd/remote/ && sudo ./run.sh"
