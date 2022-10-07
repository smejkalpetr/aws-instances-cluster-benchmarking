import boto3 
import src.constants

class ElasticLoadBalancer:
    constants = src.constants.Constants
    utilities = src.utilities

    def create_elb(self):
        response = self.utilities.create_elastic_load_balancer(self.constants.ELASTIC_LOAD_BALANCER_NAME, self.constants.SECURITY_GROUP_ID)
        print("Elastic balancer created...")

    def create_clusters(self):
        response1 = self.utilities.create_target_group(self.constants.TARGET_GROUP_1_NAME, self.constants.VPC_ID)
        response2 = self.utilities.create_target_group(self.constants.TARGET_GROUP_2_NAME, self.constants.VPC_ID)
        print("Target groups created...")

    def create_listeners(self):
        print("Listeners created...")

    def register_vms_to_tg(self):
        print("VMs registered to target group...")
