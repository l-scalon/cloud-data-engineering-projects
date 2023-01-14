#!/bin/bash
cd /var/lib/jenkins/workspace/tema12/terraform/
output=$(terraform output "public_dns")
public_dns=`echo "$output" | tr -d '"'`
mkdir -p /home/ec2-user/tema12/
cd /home/ec2-user/tema12/
cp /var/lib/jenkins/workspace/tema12/terraform/terraformkp.pem .
chmod 400 terraformkp.pem
ssh -i "terraformkp.pem" ec2-user@$public_dns -o StrictHostKeyChecking=no "sudo yum update -y && sudo yum install git -y && sudo git clone https://token@github.com/usuario/repositorio.git"
ssh -i "terraformkp.pem" ec2-user@$public_dns -o StrictHostKeyChecking=no "cd /home/ec2-user/tema12/cmd/ && sudo chmod -R u+x remote"
ssh -i "terraformkp.pem" ec2-user@$public_dns -o StrictHostKeyChecking=no "cd /home/ec2-user/tema12/cmd/remote/ && sudo sed -i -e 's/\r$//' prepare.sh && sudo sed -i -e 's/\r$//' reboot.sh && sudo sed -i -e 's/\r$//' run.sh"
ssh -i "terraformkp.pem" ec2-user@$public_dns -o StrictHostKeyChecking=no "cd /home/ec2-user/tema12/cmd/remote/ && sudo ./prepare.sh"