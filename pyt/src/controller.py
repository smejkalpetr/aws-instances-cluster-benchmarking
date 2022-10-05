from dataclasses import asdict

import boto3
import src.constants
import src.utilities
from os.path import exists


class Controller:

    vm_instances = []
    client = boto3.client('ec2')
    constants = src.constants.Constants
    utilities = src.utilities

    def initialize_env(self):
        if not exists(self.constants.KEY_PAIR_PATH):
            self.utilities.create_key_pair()
            print("this")

        if self.constants.SECURITY_GROUP_NAME is not None:
            response_sg_id = self.utilities.describe_security_group_id_by_name(self.constants.SECURITY_GROUP_NAME)
            if response_sg_id is not None:
                self.constants.SECURITY_GROUP_ID = response_sg_id


    def printMenu(self):
        print(" M E N U: ")

        print("")
        print("  [a] AUTO SETUP")
        print("")

        print("UTILITIES:")

        print("  [b] CREATE KEY PAIR")
        print("  [c] CHANGE KEY PAIR PATH")
        print("  [d] RESET KEY PAIR PATH")
        print("<<------------------------>>")

        print("  [e] CREATE SECURITY GROUP")
        print("  [f] CHANGE SECURITY GROUP NAME & ID")
        print("  [g] RESET SECURITY GROUP NAME & ID")
        print("<<------------------------>>")

        print("  [h] LAUNCH A NEW VM INSTANCE")
        print("  [i] STOP A VM INSTANCE")
        print("  [j] TERMINATE A VM INSTANCE")
        print("<<------------------------>>")

        print("  [k] LIST MENU")
        print("  [x] QUIT")
        print("")

    def create_kp(self):
        self.constants.KEY_PAIR_PATH = self.utilities.create_key_pair()

    def change_kp_path(self):
        path = input("Insert the new key pair path: ").split()

        if len(path) > 0:
            path = path[0]
        else:
            print("Wrong input!")
            return

        self.constants.KEY_PAIR_PATH = path
        print("Key pair path has been changed.")

    def reset_kp_path(self):
        self.constants.KEY_PAIR_PATH = "./keys/log8145-key-pair.pem"
        print("Key pair path has been reset.")

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
        print("Security Group name and ID have been reset.")

    def launch_one_vm(self):
        if self.constants.KEY_PAIR_PATH is None:
            print("Error: There is no Key Pair path specified. Specify one and then try again.")
            return

        if self.constants.SECURITY_GROUP_NAME is None:
            self.constants.SECURITY_GROUP_ID = self.utilities.create_security_group(self.constants.VPC_ID)

        if self.constants.SECURITY_GROUP_ID is None:
            response_sg_id = self.utilities.describe_security_group_id_by_name(self.constants.SECURITY_GROUP_NAME)
            if response_sg_id is None:
                print("Creating new Security Group...")
                self.constants.SECURITY_GROUP_ID = self.utilities.create_security_group(self.constants.VPC_ID)
            else:
                self.constants.SECURITY_GROUP_ID = response_sg_id

        response_vm = self.utilities.create_ec2_instances(self.constants.SECURITY_GROUP_ID)
        self.vm_instances.append(response_vm[0]['InstanceId'])

        print(f"VM with following ID has been created: {response_vm[0]['InstanceId']}")

    def start_all_vms(self):
        print("start all vms")

    def auto_setup(self):
       print("autosetup")

    def run(self):
        self.initialize_env()

        self.printMenu()

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
                print("stop vm")
            elif cmd_input == 'j':
                print("terminate vm")
            elif cmd_input == 'k':
                self.printMenu()
            elif cmd_input == 'x':
                print("Goodbye! :)")
                break;
            else:
                print("Wrong option, try again!")
                continue

