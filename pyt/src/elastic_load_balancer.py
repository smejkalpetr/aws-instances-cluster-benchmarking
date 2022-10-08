import boto3 
import src.constants

class ElasticLoadBalancer:
    constants = src.constants.Constants
    utilities = src.utilities
    target_groups = {}
    all_instance_ids = []
    rule_arns = []
    
    def create_elb(self):
        elb = self.utilities.create_elastic_load_balancer(self.constants.ELASTIC_LOAD_BALANCER_NAME, self.constants.SECURITY_GROUP_ID)
        #store load balancer arn to access it when creating listener
        self.load_balancer_arn = elb['LoadBalancers'][0]['LoadBalancerArn']
        self.utilities.print_info("Elastic balancer created.")

    def create_clusters(self):
        self.create_target_group_with_targets(self.constants.TARGET_GROUP_1_NAME, 
                                                self.constants.T2_LARGE, 
                                                self.constants.NUMBER_OF_T2_LARGE_INSTANCES)

        self.create_target_group_with_targets(self.constants.TARGET_GROUP_2_NAME, 
                                                self.constants.M4_LARGE, 
                                                self.constants.NUMBER_OF_M4_LARGE_INSTANCES)

    def create_target_group_with_targets(self, target_group_name, instance_type, number_of_instances):
        #create target group
        target_group = self.utilities.create_target_group(target_group_name, self.constants.VPC_ID)
        target_group_arn = target_group['TargetGroups'][0]['TargetGroupArn']

        with open("./deploy_flask.sh", 'r') as file:
            user_data = file.read() % target_group_name

        #store target group name and its arn to access it when creating listener
        self.target_groups[target_group_name] = target_group_arn
        self.utilities.print_info("Target Group " + target_group_name + " created.")

        #create instances to assign to target group
        instances = self.utilities.create_ec2_instances(self.constants.SECURITY_GROUP_ID, 
                                                        self.constants.KEY_PAIR_NAME,
                                                        instance_type, 
                                                        number_of_instances, 
                                                        self.constants.AMI_ID, 
                                                        False,
                                                        user_data)
        self.utilities.print_info(f'{number_of_instances} Instance(s) of type {instance_type} have been created.')
        instance_ids = [i['InstanceId'] for i in instances]
        self.all_instance_ids.extend(instance_ids)

        #wait until all created instances are running
        self.utilities.print_info("Waiting for all " + target_group_name +  " Instances to start running...")
        self.utilities.wait_for_instances(instance_ids, 'instance_running')

        #register instances to target group
        targets = [{'Id': id, 'Port': 80} for id in instance_ids]
        registration = self.utilities.register_targets(target_group_arn, targets, False)

        self.utilities.print_info("All Instances for Target Group " + target_group_name + " have been registered.")

    def create_listeners(self):
        listener = self.utilities.create_lister(self.load_balancer_arn, silent=False)
        self.listener_arn = listener['Listeners'][0]['ListenerArn']

        #create rule for each target group
        rule_count = 1
        for tg_name in self.target_groups:
            rule = self.utilities.create_rule(self.listener_arn, tg_name, self.target_groups[tg_name], rule_count)
            self.rule_arns.append(rule['Rules'][0]['RuleArn'])
            rule_count += 1

        self.utilities.print_info("Listener(s) have been created.")

    def delete_load_balancer(self):
        for rule in self.rule_arns:
            self.utilities.delete_rule(rule)
        self.utilities.print_info("Rule(s) have been deleted.")

        self.utilities.delete_listener(self.listener_arn)
        self.utilities.print_info("Listener(s) have been deleted.")
        
        self.utilities.delete_load_balancer(self.load_balancer_arn)
        self.utilities.print_info("Load Balancer has been deleted.")

    def delete_target_group_with_targets(self):
        self.utilities.terminate_ec2_instances(self.all_instance_ids)

        self.utilities.print_info("Waiting for all Instances to terminate...")
        self.utilities.wait_for_instances(self.all_instance_ids, 'instance_terminated')
        self.utilities.print_info("All Instances have been teminated.")


        for tg in self.target_groups:
            self.utilities.delete_target_group(self.target_groups[tg])
            self.utilities.print_info("Target Group " + tg + " has been deleted.")
            
