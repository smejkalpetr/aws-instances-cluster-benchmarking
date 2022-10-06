import boto3


def create_key_pair(name="log8145-key-pair", silent=False):
    client = boto3.client('ec2')

    try:
        response = client.create_key_pair(KeyName=name)

        pem_file = open(f"./keys/{name}.pem", "w")
        n = pem_file.write(response['KeyMaterial'])
        pem_file.close()

        if not silent:
            print("The new private key has been saved to ./keys directory.")

        return f"./keys/{name}.pem"
    except Exception as e:
        if not silent:
            print(e)


def create_security_group(
        vpc_id,
        name="log8145-security-group",
        description="SG for VMs used in LOG8145"
        silent=False
):
    client = boto3.client('ec2')

    try:
        response = client.create_security_group(GroupName=name,
                                                Description=description,
                                                VpcId=vpc_id)
        security_group_id = response['GroupId']
        if not silent:
            print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

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
            print('Ingress Successfully Set %s' % data)

        return security_group_id
    except Exception as e:
        if not silent:
            print(e)


def describe_security_group_id_by_name(name):
    client = boto3.client('ec2')

    try:
        response = client.describe_security_groups(GroupNames=[name])
        return response['SecurityGroups'][0]['GroupId']
    except Exception as e:
        if not silent:
            print(e)

def describe_security_group_by_id(sg_id, silent=False):
    client = boto3.client('ec2')

    try:
        response = client.describe_security_groups(GroupIds=[sg_id])
        return response
    except Exception as e:
        if not silent:
            print(e)


def create_ec2_instances(security_group_id,
                         instance_type="t2.micro",
                         count=1,
                         ami="ami-0149b2da6ceec4bb0",
                         silent=False
    ):
    client = boto3.client('ec2')

    try:
        response = client.run_instances(
            ImageId=ami,
            InstanceType=instance_type,
            MaxCount=count,
            MinCount=count,
            Monitoring={
                'Enabled': True
            },
            SecurityGroupIds=[
                security_group_id,
            ]
        )
        return response['Instances']
    except Exception as e:
        if not silent:
            print(e)


def stop_ec2_instances(instance_ids):
    print("stop_ec2_instance hello")


def terminate_ec2_instances(instance_ids):
    print("terminate_ec2_instance hello")
