import boto3

# prints unified output
def print_info(message):
    print(f'[INFO] {message}')

# gets the vpc id from the aws to later use it in the program
def get_vpc(silent=False):
    client = boto3.client('ec2')
    try:
        response = client.describe_vpcs()
        return response['Vpcs'][0]['VpcId']
    except Exception as e:
        if not silent:
            print(e)

# created new key pair
def create_key_pair(name="log8145-key-pair", silent=False):
    client = boto3.client('ec2')

    try:
        response = client.create_key_pair(KeyName=name)

        pem_file = open(f"./keys/{name}.pem", "w")
        n = pem_file.write(response['KeyMaterial'])
        pem_file.close()

        if not silent:
            print_info("The new private key has been saved to ./keys directory.")

        return f"./keys/{name}.pem"
    except Exception as e:
        if not silent:
            print(e)

# creates new security group with given name
def create_security_group(
        vpc_id,
        name="log8145-security-group",
        description="SG for VMs used in LOG8145",
        silent=False
):
    client = boto3.client('ec2')

    try:
        response = client.create_security_group(GroupName=name,
                                                Description=description,
                                                VpcId=vpc_id)
        security_group_id = response['GroupId']
        if not silent:
            print_info('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 22,
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        if not silent:
            print_info('Ingress Successfully Set %s' % data)

        return security_group_id
    except Exception as e:
        if not silent:
            print(e)

# describes the security groups id by its given name
def describe_security_group_id_by_name(name, silent=False):
    client = boto3.client('ec2')

    try:
        response = client.describe_security_groups(GroupNames=[name])
        return response['SecurityGroups'][0]['GroupId']
    except Exception as e:
        if not silent:
            print(e)

# describes the security group id
def describe_security_group_by_id(sg_id, silent=False):
    client = boto3.client('ec2')

    try:
        response = client.describe_security_groups(GroupIds=[sg_id])
        return response
    except Exception as e:
        if not silent:
            print(e)

# creates desired number of instances of specific type
def create_ec2_instances(security_group_id,
                         key_name,
                         instance_type="t2.micro",
                         count=1,
                         ami="ami-0149b2da6ceec4bb0",
                         silent=False,
                         user_data=""
    ):
    client = boto3.client('ec2')

    try:
        response = client.run_instances(
            ImageId=ami,
            InstanceType=instance_type,
            KeyName=key_name,
            MaxCount=count,
            MinCount=count,
            Monitoring={
                'Enabled': True
            },
            SecurityGroupIds=[
                security_group_id,
            ],
            UserData=user_data
        )
        return response['Instances']

    except Exception as e:
        if not silent:
            print(e)

# stops chosen instances by their ids
def stop_ec2_instances(instance_ids, silent=False) -> dict:
    client = boto3.client('ec2')

    try:
        response = client.stop_instances(InstanceIds=instance_ids)
        return response
    except Exception as e:
        if not silent:
            print(e)

# starts chosen instances by their ids
def start_ec2_instances(instance_ids, silent=False) -> dict:
    client = boto3.client('ec2')

    try:
        response = client.start_instances(InstanceIds=instance_ids)
        return response
    except Exception as e:
        if not silent:
            print(e)

# terminates chosen instances by their ids
def terminate_ec2_instances(instance_ids, silent=False) -> dict:
    client = boto3.client('ec2')

    try:
        response = client.terminate_instances(InstanceIds=instance_ids)
        return response
    except Exception as e:
        if not silent:
            print(e)

# creates new target group with given name
def create_target_group(name, vpc_id, silent=False) -> dict:
    client = boto3.client('elbv2')

    try:
        response = client.create_target_group(
            Name=name,
            Protocol='HTTP',
            ProtocolVersion='HTTP1',
            Port=80,
            VpcId=vpc_id,
            HealthCheckEnabled=True,
            HealthCheckPath=f'/{name}',
            HealthCheckIntervalSeconds=10,
            HealthyThresholdCount=3,
            TargetType='instance',
            Tags=[
                {
                    'Key': 'Name',
                    'Value': name
                },
            ],
            IpAddressType='ipv4'
        )
        return response
    except Exception as e:
        if not silent:
            print(e)

# creates application load balancer
def create_elastic_load_balancer(name, security_group_id, silent=False) -> dict:
    client = boto3.client('elbv2')
    client_ec2 = boto3.client('ec2')

    try:
        response = client.create_load_balancer(
        Name=name,
        Subnets = [s['SubnetId'] for s in client_ec2.describe_subnets()['Subnets']],
        SecurityGroups=[
            security_group_id
        ],
        Scheme='internet-facing',
        Type='application',
        IpAddressType='ipv4'
        )
        return response
    except Exception as e:
        if not silent:
            print(e)

# registers given instances to given target group
def register_targets(target_group_arn, targets, silent=False) -> dict:
    client = boto3.client('elbv2')

    try:
        response = client.register_targets(
            TargetGroupArn=target_group_arn,
            Targets=targets
        )
        return response
    except Exception as e:
        if not silent:
            print(e)

# waits for all the instances to either start running or to be terminaned based on the given parameter
def wait_for_instances(ids, state, silent=False):
    client = boto3.client('ec2')

    try:
        waiter = client.get_waiter(state)
        waiter.wait(
            InstanceIds=ids,
            WaiterConfig={
                'Delay': 10,
                'MaxAttempts': 30
            }
        )
    except Exception as e:
        if not silent:
            print(e)

# waits for the target group to be in service
def wait_for_target_group(target_group_arn, silent=False):
    client = boto3.client('elbv2')

    try:
        waiter = client.get_waiter('target_in_service')
        waiter.wait(
            TargetGroupArn=target_group_arn, 
            WaiterConfig={ 
                'Delay': 10 ,
                'MaxAttempts': 30
                }
        )
    except Exception as e:
        if not silent:
            print(e)

# creates listener on the load balancer
def create_lister(load_balancer_arn, silent=False) -> dict:
    client = boto3.client('elbv2')

    try:
        response = client.create_listener(
            LoadBalancerArn=load_balancer_arn,
            Protocol='HTTP',
            Port=80,
            DefaultActions=[
                {
                'Type': 'fixed-response',
                'FixedResponseConfig': { 
                    'StatusCode': '200',
                    'ContentType': 'text/plain',
                    'MessageBody': 'Listener listening!'}
                }
            ]
        )
        return response
    except Exception as e:
        if not silent:
            print(e)

# creates rule on the listener
def create_rule(listener_arn, target_group_name, target_group_arn, rule_count, silent=False) -> dict:
    client = boto3.client('elbv2')

    try:
        response = client.create_rule(
            ListenerArn=listener_arn,
            Conditions=[
                {
                    'Field': 'path-pattern',
                    'Values': [ f'/{target_group_name}' ]
                },
            ],
            Priority=rule_count,
            Actions=[
                {
                    'Type': 'forward',
                    'TargetGroupArn': target_group_arn,
                },
            ]
        )
        return response

    except Exception as e:
        if not silent:
            print(e)

# deletes the given listener rule
def delete_rule(rule_arn, silent=False):
    client = boto3.client('elbv2')

    try:
        response = client.delete_rule(RuleArn=rule_arn)

    except Exception as e:
        if not silent:
            print(e)

# deletes the given listener
def delete_listener(listener_arn, silent=False):
    client = boto3.client('elbv2')

    try: 
        response = client.delete_listener(ListenerArn=listener_arn)

    except Exception as e:
        if not silent:
            print(e)

# deleted the load balancer
def delete_load_balancer(load_balancer_arn, silent=False):
    client = boto3.client('elbv2')

    try: 
        response = client.delete_load_balancer(LoadBalancerArn=load_balancer_arn)

    except Exception as e:
        if not silent:
            print(e)

# deletes the given target group
def delete_target_group(target_group_arn, silent=False):
    client = boto3.client('elbv2')

    try: 
        response = client.delete_target_group(TargetGroupArn=target_group_arn)

    except Exception as e:
        if not silent:
            print(e)

# deletes the given security group
def delete_security_group(group_id, silent=False):
    client = boto3.client('ec2')

    try: 
        response = client.delete_security_group(GroupId=group_id)

    except Exception as e:
        if not silent:
            print(e)

# deletes the given key pair
def delete_key_pair(key_pair_name, silent=False):
    client = boto3.client('ec2')

    try: 
        response = client.delete_key_pair(KeyName=key_pair_name)

    except Exception as e:
        if not silent:
            print(e)

# describes the load balancer
def describe_load_balancers(silent=False):
    client = boto3.client('ec2')

    try:
        response = client.describe_load_balancers(
            LoadBalancerArns=[
                'string',
            ],
            Names=[
                'string',
            ],
            Marker='string',
            PageSize=123
        )

    except Exception as e:
        if not silent:
            print(e)
