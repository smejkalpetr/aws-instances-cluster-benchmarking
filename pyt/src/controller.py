from dataclasses import asdict

import boto3
import src.constants
import src.utilities
import src.elastic_load_balancer
from os.path import exists
import os 


class Controller:

    vm_instances = []
    client = boto3.client('ec2')
    constants = src.constants.Constants
    utilities = src.utilities
    elastic_load_balancer = None

    def initialize_env(self):
        self.utilities.print_info("Initializing...")

        self.constants.VPC_ID = self.utilities.get_vpc()

        if not exists(self.constants.KEY_PAIR_PATH):
            self.utilities.create_key_pair()

        if self.constants.SECURITY_GROUP_NAME is not None:
            response_sg_id = self.utilities.describe_security_group_id_by_name(self.constants.SECURITY_GROUP_NAME, silent=True)
            if response_sg_id is not None:
                self.constants.SECURITY_GROUP_ID = response_sg_id
        
        self.utilities.print_info("Initialization done.")


    def print_menu(self):
        print("<<------------------------>>")
        print("APPLICATION MENU: ")
        print("  [a] AUTO SETUP")
        print("<<------------------------>>")

        print("UTILITIES:")

        print("  [b] CREATE KEY PAIR")
        print("  [c] CHANGE KEY PAIR PATH")
        print("  [d] RESET KEY PAIR PATH")
        print("  <<---------------------->>")

        print("  [e] CREATE SECURITY GROUP")
        print("  [f] CHANGE SECURITY GROUP NAME & ID")
        print("  [g] RESET SECURITY GROUP NAME & ID")
        print("  <<---------------------->>")

        print("  [h] LAUNCH A NEW VM INSTANCE")
        print("  [i] STOP A VM INSTANCE")
        print("  [j] TERMINATE A VM INSTANCE")
        print("  [k] START A VM INSTANCE")
        print("  <<---------------------->>")

        print("  [l] LIST MENU")
        print("  [x] QUIT")
        print("<<------------------------>>")

    def create_kp(self):
        self.utilities.print_info("Creating a new Key Pair...")
        self.constants.KEY_PAIR_PATH = self.utilities.create_key_pair()

    def change_kp_path(self):
        path = input("Insert the new key pair path: ").split()

        if len(path) > 0:
            path = path[0]
        else:
            print("Wrong input!")
            return

        self.constants.KEY_PAIR_PATH = path
        self.utilities.print_info("Key pair path has been changed.")

    def reset_kp_path(self):
        self.constants.KEY_PAIR_PATH = "./keys/log8145-key-pair.pem"
        self.utilities.print_info("Key pair path has been reset.")

    def create_sg(self):

        name = input("Insert the new Security Group name: ").split()

        if len(name) > 0:
            name = name[0]
        else:
            print("Wrong input!")
            return

        description = input("Insert the new Security Group description: ")

        if len(description) <= 0:
            print("Wrong input!")
            return

        self.constants.SECURITY_GROUP_ID = self.utilities.create_security_group(
                                                self.constants.VPC_ID,
                                                name,
                                                description
                                            )
        self.constants.SECURITY_GROUP_NAME = name

    def change_sg_name_and_id(self):
        name = input("Insert the new Security Group name: ").split()

        if len(name) > 0:
            name = name[0]
        else:
            print("Wrong input!")
            return

        sg_id = input("Insert the new Security Group ID: ").split()

        if len(name) > 0:
            name = name[0]
        else:
            print("Wrong input!")
            return

        self.constants.SECURITY_GROUP_NAME = name
        self.constants.SECURITY_GROUP_ID = sg_id

    def reset_sg_name_and_id(self):
        self.constants.SECURITY_GROUP_NAME = "log8145-security-group"
        self.constants.SECURITY_GROUP_ID = None
        self.utilities.print_info("Security Group name and ID have been reset.")

    def check_sg_and_kp(self):
        if self.constants.KEY_PAIR_PATH is None:
            print("[ERROR]: There is no Key Pair path specified. Specify one and then try again.")
            return

        if self.constants.SECURITY_GROUP_NAME is None:
            self.constants.SECURITY_GROUP_ID = self.utilities.create_security_group(self.constants.VPC_ID, silent=True)

        if self.constants.SECURITY_GROUP_ID is None:
            response_sg_id = self.utilities.describe_security_group_id_by_name(self.constants.SECURITY_GROUP_NAME, silent=True)
            if response_sg_id is None:
                self.utilities.print_info("Creating new Security Group...")
                self.constants.SECURITY_GROUP_ID = self.utilities.create_security_group(self.constants.VPC_ID, silent=True)
                self.utilities.print_info("New Security Group " + self.constants.SECURITY_GROUP_NAME + " has been created.")

            else:
                self.constants.SECURITY_GROUP_ID = response_sg_id

    def launch_one_vm(self):
        self.check_sg_and_kp()

        self.utilities.print_info("Creating a new VM instance...")
        response_vm = self.utilities.create_ec2_instances(self.constants.SECURITY_GROUP_ID, self.constants.KEY_PAIR_NAME)
        self.vm_instances.append(response_vm[0]['InstanceId'])

        self.utilities.print_info(f"VM with the following ID has been created: {response_vm[0]['InstanceId']}")

    def start_one_vm(self):
        instance_id = input("Insert the instance ID: ").split()

        if len(instance_id) > 0:
            instance_id = instance_id[0]
        else:
            print("Wrong input!")
            return

        response = self.utilities.start_ec2_instances([instance_id])
        print(response)

    def stop_one_vm(self):
        instance_id = input("Insert the instance ID: ").split()

        if len(instance_id) > 0:
            instance_id = instance_id[0]
        else:
            print("Wrong input!")
            return

        response = self.utilities.stop_ec2_instances([instance_id])
        print(response)

    def terminate_one_vm(self):
        instance_id = input("Insert the instance ID: ").split()

        if len(instance_id) > 0:
            instance_id = instance_id[0]
        else:
            print("Wrong input!")
            return

        response = self.utilities.terminate_ec2_instances([instance_id])
        print(response)
    

    def auto_setup(self):
        self.check_sg_and_kp()
        self.elastic_load_balancer = src.elastic_load_balancer.ElasticLoadBalancer()
        
        self.elastic_load_balancer.create_elb()
        self.elastic_load_balancer.create_clusters()
        self.elastic_load_balancer.create_listeners()

    def delete_key_pair(self):
        self.utilities.delete_key_pair(self.constants.KEY_PAIR_NAME)

        cctp1_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        keys_path = os.path.abspath(os.path.join(cctp1_path, 'keys'))
        os.remove(os.path.join(keys_path, self.constants.KEY_PAIR_NAME +'.pem'))

        self.utilities.print_info("Key Pair "+ self.constants.KEY_PAIR_NAME + " has been deleted.")

    def delete_security_group(self):
        self.utilities.delete_security_group(self.constants.SECURITY_GROUP_ID)
        self.utilities.print_info("Security Group " + self.constants.SECURITY_GROUP_NAME + " has been deleted.")

    def auto_shutdown(self):
        if self.elastic_load_balancer is not None:
            self.elastic_load_balancer.delete_load_balancer()
            self.elastic_load_balancer.delete_target_group_with_targets()

        if self.constants.SECURITY_GROUP_ID is not None:
            self.delete_security_group()
        self.delete_key_pair()

    def run(self):
        self.initialize_env()

        self.print_menu()

        while True:
            cmd_input_line = input("-> ").split()

            if len(cmd_input_line) < 1:
                print("Choose a command and try again!")
                continue

            cmd_input = cmd_input_line[0]

            if cmd_input == 'a':
                self.auto_setup()
            elif cmd_input == 'b':
                self.create_kp()
            elif cmd_input == 'c':
                self.change_kp_path()
            elif cmd_input == 'd':
                self.reset_kp_path()
            elif cmd_input == 'e':
                self.create_sg()
            elif cmd_input == 'f':
                self.change_sg_name_and_id()
            elif cmd_input == 'g':
                self.reset_sg_name_and_id()
            elif cmd_input == 'h':
                self.launch_one_vm()
            elif cmd_input == 'i':
                self.stop_one_vm()
            elif cmd_input == 'j':
                self.terminate_one_vm()
            elif cmd_input == 'k':
                self.start_one_vm()
            elif cmd_input == 'l':
                self.printMenu()
            elif cmd_input == 'x':
                self.auto_shutdown()
                print("Goodbye! :)")
                break
            else:
                print("Wrong option, try again!")
                continue

