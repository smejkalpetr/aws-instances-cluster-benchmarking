#!/bin/bash

# #::: launchVMs.sh :::#
# This script launches all needed VMs.

# launch desired instances
aws ec2 run-instances --image-id "$1" --count "$4" --instance-type "$5" --key-name "$2" --security-group-ids "$3" --subnet-id subnet-09307f70fe9b46d26
