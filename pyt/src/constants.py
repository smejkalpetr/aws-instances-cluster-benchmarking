
class Constants:
    KEY_PAIR_NAME = "log8145-key-pair"
    KEY_PAIR_PATH = "./keys/log8145-key-pair.pem"
    SECURITY_GROUP_NAME = "log8145-security-group"
    SECURITY_GROUP_ID = None
    AMI_ID = "ami-0149b2da6ceec4bb0"
    ELASTIC_LOAD_BALANCER_NAME = "log8145-elastic-load-balancer"
    TARGET_GROUP_1_NAME = "cluster1"
    TARGET_GROUP_2_NAME = "cluster2"
    T2_LARGE = "t2.micro"
    M4_LARGE = "t2.micro"
    NUMBER_OF_T2_LARGE_INSTANCES = 1
    NUMBER_OF_M4_LARGE_INSTANCES = 1

    # You need to change VPC_ID to your own before using the program
    # You can find it on the EC2 Dashboard
    VPC_ID_SET = "vpc-0afbee2a2cf707f72"
    VPC_ID = None

    SUBNET1_ID = None
    SUBNET2_ID = None

    INSTANCE_TYPE1 = None
    INSTANCE_TYPE2 = None
