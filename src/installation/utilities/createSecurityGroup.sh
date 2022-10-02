#!/bin/bash

# This script screate a security gruoup with suitable rules in order to be able to do the assigment instructions

echo "Creating new Security Group..."

read -p "Enter your VPC ID (you can find it on the AWS Dashboard): " vpcID

read -p "Enter your new security group name: " newSgName

read -p "Enter description for the new security group: " newSgDesc

echo "The new group is being created..."

# this command creates the new security group and parses the new SG ID from the json result
newSgId=$(aws ec2 create-security-group --group-name "$newSgName" --description "$newSgDesc" --vpc-id "$vpcID" | jq -r '.GroupId')

if [ $? -eq 0 ]; then
   echo "Succes: The new Security Group ${newSgId} has been created."
   export newSgId
   export newSgName
else
   echo "Fail: Failed to create a new Security Group."
fi

echo "Applying suitable rules..."
# allows inbound from given IP address
aws ec2 authorize-security-group-ingress --group-name "$newSgName" --protocol tcp --port 22 --cidr "${myIp}/32"

echo ""

if [ $? -eq 0 ]; then
   echo "Succes: All rules have been applied."
else
   echo "Fail: Failed to apply the rules."
fi
echo ""
