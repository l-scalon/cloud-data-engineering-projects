terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "us-east-2"
}

resource "tls_private_key" "private_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "key_pair" {
  key_name   = "terraformkp"
  public_key = tls_private_key.private_key.public_key_openssh
  provisioner "local-exec" {
    command = "echo '${tls_private_key.private_key.private_key_pem}' > ./terraformkp.pem"
  }
}

resource "aws_instance" "ec2_terraform" {
  depends_on             = [aws_key_pair.key_pair]
  ami                    = "ami-0b614a5d911900a9b"
  instance_type          = "t2.micro"
  availability_zone      = "us-east-2b"
  vpc_security_group_ids = ["sg-045c3e268ea96610e"]
  key_name               = "terraformkp"

  tags = {
    Name             = "devops-cloud-basics-lucasscalon-terraform"
    Owner            = "Lucas Scalon"
    Project          = "ILEGRA-JT-DEVOPSCLOUD"
    EC2_ECONOMIZATOR = "TRUE"
    CustomerID       = "ILEGRA-JTS"
  }
}

output "public_dns" {
  value = aws_instance.ec2_terraform.public_dns
}
