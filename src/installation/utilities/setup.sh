# asks user for their IP address and exports it to the environment

read -p "Enter your IP address (check at https://checkip.amazonaws.com/): " myIp
export myIp

export awsAmi="ami-0149b2da6ceec4bb0"

echo ""

./createKeyPair.sh && ./createSecurityGroup.sh

echo ""
echo "Setup finished."
