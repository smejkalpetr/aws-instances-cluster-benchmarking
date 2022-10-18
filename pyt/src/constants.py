
class Constants:
    KEY_PAIR_NAME = "log8145-key-pair"
    KEY_PAIR_PATH = "./keys/log8145-key-pair.pem"
    SECURITY_GROUP_NAME = "log8145-security-group"
    SECURITY_GROUP_ID = None
    AMI_ID = "ami-0149b2da6ceec4bb0"
    ELASTIC_LOAD_BALANCER_NAME = "log8145-elastic-load-balancer"
    TARGET_GROUP_1_NAME = "cluster1"
    TARGET_GROUP_2_NAME = "cluster2"
    T2_LARGE = "t2.large"
    M4_LARGE = "m4.large"
    NUMBER_OF_T2_LARGE_INSTANCES = 4
    NUMBER_OF_M4_LARGE_INSTANCES = 5
    VPC_ID = None
    VM_OUTPUT_DIR = "./out/vms"
    ELB_OUTPUT_DIR = "./out/elb"
    TG_OUTPUT_DIR = "./out/tg"
    METRICS_TYPE_INSTANCE = "InstanceId"
    METRICS_TYPE_ELB = "LoadBalancer"
    METRICS_TYPE_TARGET_GROUP = "TargetGroup"
