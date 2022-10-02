#!/bin/bash

# read key pair name
echo "Creating new Key Pair..."

read -p "Enter key pair name: " newKeyPairName

# create a new AWS key pair
echo "The new key pair is being created (with suitable rules)..."
aws ec2 create-key-pair --key-name "$newKeyPairName" --query 'KeyMaterial' --output text > "${newKeyPairName}.pem" && \
export newKeyPairName && \
echo "Your new keypair has been saved at the /src/installation/utilities folder."

echo ""
