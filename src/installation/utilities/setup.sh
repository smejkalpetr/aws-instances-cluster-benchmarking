# asks user for their IP address and exports it to the environment

echo "###>>>>---------------<<<<###"
read -p "Enter your IP address (check at https://checkip.amazonaws.com/): " myIp
export myIp

./createKeyPair.sh && \

./createSecurityGroup.sh
