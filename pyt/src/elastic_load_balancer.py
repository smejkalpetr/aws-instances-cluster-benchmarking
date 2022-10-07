import boto3 
import src.constants

class ElasticLoadBalancer:
    constants = src.constants.Constants
    utilities = src.utilities

    def create_elb(self):
        response = self.utilities.create_elastic_load_balancer(self.constants.ELASTIC_LOAD_BALANCER_NAME, self.constants.SECURITY_GROUP_ID)
        print("Elastic balancer created.")

    def create_clusters(self):
        self.create_target_group_with_targets(self.constants.TARGET_GROUP_1_NAME, 
                                                self.constants.T2_LARGE, 
                                                self.constants.NUMBER_OF_T2_LARGE_INSTANCES)

        self.create_target_group_with_targets(self.constants.TARGET_GROUP_2_NAME, 
                                                self.constants.M4_LARGE, 
                                                self.constants.NUMBER_OF_M4_LARGE_INSTANCES)

    def create_target_group_with_targets(self, target_group_name, instance_type, number_of_instances):
        target_group = self.utilities.create_target_group(target_group_name, self.constants.VPC_ID)
        print("Target group " + target_group_name + " created.")

        instances = self.utilities.create_ec2_instances(self.constants.SECURITY_GROUP_ID, 
                                                        instance_type, 
                                                        number_of_instances, 
                                                        self.constants.AMI_ID, 
                                                        False)
        print(f'{number_of_instances} instance(s) of type {instance_type} have been created.')
        instance_ids = [i['InstanceId'] for i in instances]
        
        print("Waiting for all " + target_group_name +  " instances to start running...")
        self.utilities.wait_for_instances(instance_ids)

        targets = [{'Id': id, 'Port': 80} for id in instance_ids]
        registration = self.utilities.register_targets(target_group['TargetGroups'][0]['TargetGroupArn'], targets, False)

        print("All instances for target group " + target_group_name + " registered.")

    def create_listeners(self):
        print("Listeners created.")

