#!/bin/bash

# #::: createSecurityGroup.sh :::#
# This script creates a security gruoup with suitable rules in order to be able to do the assigment instructions.

# this command creates the new security group and parses the new SG ID from the json result
aws ec2 create-security-group --group-name "$2" --description "$3" --vpc-id "$1"

# allows inbound from the given IP address
aws ec2 authorize-security-group-ingress --group-name "$2" --protocol tcp --port 22 --cidr "${4}/32"
