# asks user for their IP address and exports it to the environment

# #::: setup.sh :::#
# This script sets the environment to build VMs and clusters on.

read -p "Enter your IP address (check at https://checkip.amazonaws.com/): " myIp
export myIp

. ./utilities/createKeyPair.sh

. ./utilities/createSecurityGroup.sh

echo "Setup finished."
echo ""
