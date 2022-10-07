import boto3 

class ElasticLoadBalancer:


    def create_elb(self):
        print("Elastic load balancer created!")

    def create_clusters(self, vpc_id):
        self.create_target_group("cluster1", vpc_id)
        self.create_target_group("cluster2", vpc_id)



    def create_target_group(self, name, vpc_id):
        try:
            client = boto3.client('elbv2')
            response = client.create_target_group(
                Name=name,
                Protocol='HTTP',
                Port=80,
                VpcId=vpc_id,
                HealthCheckProtocol='HTTP',
                HealthCheckPort='80',
                HealthCheckEnabled=True,
                HealthCheckIntervalSeconds=10,
                HealthCheckTimeoutSeconds=9,
                HealthyThresholdCount=10,
                UnhealthyThresholdCount=10,
                TargetType='instance',
                Tags=[
                    {
                        'Key': 'Name',
                        'Value': name
                    },
                ],
                IpAddressType='ipv4'
            )
            print("Target group " + name +  " created!")
        except Exception as e:
            if not silent:
                print(e)
                

    def create_listeners(self):
        print("Listeners created!")

    def register_vms_to_tg(self):
        print("VMs registered to target group!")
