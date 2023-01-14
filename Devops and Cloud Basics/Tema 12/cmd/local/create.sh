#!/bin/bash
cd /var/lib/jenkins/workspace/tema12/terraform/
terraform init
terraform apply -auto-approve
