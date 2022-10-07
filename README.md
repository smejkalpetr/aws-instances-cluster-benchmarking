# TP1: Advanced Concepts of Cloud Computing

## How to launch to setup.bin

First, you need to open the LearnerLab and start the Lab. Then, on the same page, you have to get the AWS cretentials in order to control AWS with CLI. This is a string in the 'AWS Details' tab. Put the string in ~/.aws/credentials. Don't forget that you have to do this every time you restart the Lab.

Now, navigate to the repository and use the provided `Makefile`. Compile the project and start the `setup.bin` by `make all`.

This will open a menu. You can manually create key pairs, security groups, VMs and clusters, however, just using the 'S' option will do fine for an automatic setup which will start two desired clusters at `IP/cluster1` and `IP/cluster2`.

Link to documentation:
https://www.overleaf.com/project/633713bf7f576a2c756ed882
