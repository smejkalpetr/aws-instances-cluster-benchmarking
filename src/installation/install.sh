#!/bin/bash

# starts the VMs, installs OS, deploys Flask framework on the VMs and 
# creates target groups with a loadbalancers

# the clusters should be available at /cluster1 and /cluster2

# those commands execute parts of the process explained above (and reports its success/failure)
echo "Starting to execute..."

if ./installation/launchVMs.sh ; then
    echo "Success: Started all VMs."
else
    echo "Error: Failed to start the VMs."
fi

if ./installation/installUbuntu.sh ; then
    echo "Success: Installed Ubuntu on all VMs."
else
    echo "Error: Failed to install Ubunti on the VMs."
fi

if ./installation/deployFlask.sh ; then
    echo "Success: Deployed Flask to all VMs."
else
    echo "Error: Failed to deploy flask to the VMs."
fi

if ./installation/createClusters.sh ; then
    echo "Success: Created all required loadbalanced clusters."
else
    echo "Error: Failed to create clusters."
fi
