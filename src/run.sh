#!/bin/bash

# this script configuers the clusers (starts VMs, installs OS + deploys Flask on them, creates target groups) 
# and then runs a benchmark and finally reports the results

# add execute permission for each script in the src folder if not present
echo "Checking permission to execute the required scripts..."

find ./installation -type f -exec chmod 700 {} \;

if [ $? -eq 0 ]; then
   echo "Execute permisions for installation have been set."
else
   echo "Failed to modify installation permissions."
fi

find ./benchmarking -type f -exec chmod 700 {} \;

if [ $? -eq 0 ]; then
   echo "Execute permisions for benchmarking have been set."
else
   echo "Failed to modify benchmarking permissions."
fi

# run install.sh and if it succeedes, run benchmark.sh
./installation/install.sh && ./benchmarking/benchmark.sh
