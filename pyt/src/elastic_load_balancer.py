import boto3 
import src.constants

class ElasticLoadBalancer:
    constants = src.constants.Constants
    utilities = src.utilities
    target_groups = {}
    
    def create_elb(self):
        elb = self.utilities.create_elastic_load_balancer(self.constants.ELASTIC_LOAD_BALANCER_NAME, self.constants.SECURITY_GROUP_ID)
        #store load balancer arn to access it when creating listener
        self.load_balancer_arn = elb['LoadBalancers'][0]['LoadBalancerArn']
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
        target_group_arn = target_group['TargetGroups'][0]['TargetGroupArn']
        #store target group name and its arn to access it when creating listener
        self.target_groups[target_group_name] = target_group_arn
        print("Target group " + target_group_name + " created.")

        instances = self.utilities.create_ec2_instances(self.constants.SECURITY_GROUP_ID, 
                                                        self.constants.KEY_PAIR_NAME,
                                                        instance_type, 
                                                        number_of_instances, 
                                                        self.constants.AMI_ID, 
                                                        False)
        print(f'{number_of_instances} instance(s) of type {instance_type} have been created.')
        instance_ids = [i['InstanceId'] for i in instances]
        
        print("Waiting for all " + target_group_name +  " instances to start running...")
        self.utilities.wait_for_instances(instance_ids)

        targets = [{'Id': id, 'Port': 80} for id in instance_ids]
        registration = self.utilities.register_targets(target_group_arn, targets, False)

        print("All instances for target group " + target_group_name + " registered.")

    def create_listeners(self):
        listener = self.utilities.create_lister(self.load_balancer_arn, silent=False)
        self.listener_arn = listener['Listeners'][0]['ListenerArn']

        #create rule for each target group
        rule_count = 1
        for tg_name in self.target_groups:
            self.utilities.create_rule(self.listener_arn, tg_name, self.target_groups[tg_name], rule_count)
            rule_count += 1

        print("Listeners created.")

