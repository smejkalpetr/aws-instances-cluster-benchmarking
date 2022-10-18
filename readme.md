
# TP1: Advanced Concepts of Cloud Computing

## Description of the Work

The aim of this work was to learn about Cloud Provider Computing Service using AWS and evaluation of the performance of used services. We launched virtual machines, created two target groups, used load balancer to distribute workloads, set listeners with rules and analysed the overall performance performance. All of this was executed in an automated solution using Pyhon's boto3. 

## Instructions to Run the Code

1. Configure AWS Credentials on your computer:

    * Open the file with AWS credentials:
  
        ``code ~/.aws/credentials``
        
    * Navigate to your AWS Academy account, then to AWS Details and copy your AWS CLI information. 
        
    * Paste the AWS CLI information to the opened credentials file and save and close the file.

 2. Clone the GitHub repository to your desired location:
  
    ``git clone https://github.com/smejkalpetr/cc-tp1.git``
  
3. Proceed to the project's directory:
  
    ``cd cc-tp1``
  
4. Run the automated application:
  
    ``. ./setup.sh auto``
  
5. See the results in the ``./out`` directory.


Link to documentation:
https://www.overleaf.com/project/633713bf7f576a2c756ed882
