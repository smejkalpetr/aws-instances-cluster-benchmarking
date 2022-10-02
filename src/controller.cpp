#include <cstdio>
#include <stdio.h>
#include <sys/wait.h>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <ostream>
#include <sstream>
#include <array>

// Source of the next struct & class: https://github.com/RaymiiOrg/cpp-command-output,
// author allows free usage and modification)
struct CommandResult {
    std::string output;
    int exitstatus;
    friend std::ostream &operator<<(std::ostream &os, const CommandResult &result) {
        os << "Command Exit Status: " << result.exitstatus << "\nCommand Output: " << result.output;
        return os;
    }
    bool operator==(const CommandResult & rhs) const {
        return output == rhs.output &&
                exitstatus == rhs.exitstatus;
    }
    bool operator!=(const CommandResult & rhs) const {
        return !(rhs == *this);
    }
};

class Command {
public:
    static CommandResult exec(const std::string & command) {
        int exitcode = 0;
        std::array<char, 1048576> buffer {};
        std::string result;

        FILE *pipe = popen(command.c_str(), "r");
        if (pipe == nullptr) {
            throw std::runtime_error("popen() failed!");
        }
        try {
            std::size_t bytesread;
            while ((bytesread = std::fread(buffer.data(), sizeof(buffer.at(0)), sizeof(buffer), pipe)) != 0) {
                result += std::string(buffer.data(), bytesread);
            }
        } catch (...) {
            pclose(pipe);
            throw;
        }
        int val = pclose(pipe);
        exitcode = WEXITSTATUS(val);
        return CommandResult{result, exitcode};
    }
};

// Environment variables:
std::string keyPairName = "";
std::string securityGroupName = "";
std::string securityGroupId = "";
std::string securityGroupDesc = "";
std::string vpcId = "";
std::string myIp = "";
std::string awsAmi = "ami-0149b2da6ceec4bb0";

void printMenu() {
    std::cout << " M E N U : " << std::endl;
    std::cout << "[S] AUTO SETUP" << std::endl;
    std::cout << "[K] CREATE NEW KEY PAIR" << std::endl;
    std::cout << "[G] CREATE NEW SECURITY GROUP" << std::endl;
    std::cout << "[V] CREATE CREATE NEW VIRTUAL MACHINE" << std::endl;
    std::cout << "[X] EXIT" << std::endl;
    std::cout << "###>>>-------------------------<<<###" << std::endl;
}

void createKeyPair() {
    std::cout << "Creating a new Key Pair..." << std::endl;

    std::cout << "Enter the new Key Pair name: " << std::endl;
    std::cin >> keyPairName;

    std::ostringstream oss;
    oss << "./installation/utilities/createKeyPair.sh" << " " << keyPairName;

    std::cout << "Executing script: " << oss.str() << std::endl;

    std::cout << Command::exec(oss.str().c_str()) << std::endl;
}

std::string parseSecurityGroupId(std::string inp) {
    std::string token = inp.substr(inp.find("GroupId"));
    std::string quote = token.substr(11);
    std::string parsed = quote.substr(0, quote.find("\""));
    
    return parsed;
}

void createSecurityGroup() {
    std::cout << "Creating a new Security Group (and will apply its rules)..." << std::endl;

    std::cout << "Enter your IP address (you can check it on https://checkip.amazonaws.com/): " << std::endl;
    std::cin >> myIp;

    std::cout << "Enter your VPC ID (you can find it on the AWS Dashboard): " << std::endl;
    std::cin >> vpcId;

    std::cout << "Enter the new Security Group name: " << std::endl;
    std::cin >> securityGroupName;

    std::cout << "Enter the new Security Group description: " << std::endl;
    getline(std::cin >> std::ws, securityGroupDesc);

    std::ostringstream oss;
    oss << "./installation/utilities/createSecurityGroup.sh" << " " << vpcId << " " << securityGroupName << " " << '"' << securityGroupDesc << '"' << " " << myIp;

    std::ostringstream oss2;
    std::cout << "Executing script: " << oss.str() << std::endl;
    oss2 << Command::exec(oss.str().c_str());
    securityGroupId = parseSecurityGroupId(oss2.str());
    std::cout << oss2.str() << std::endl;
}

void launchVirtualMachine() {
    int instOpt = 0;
    int instNo = 0;
    std::string instType = "";

    std::cout << "Enter the type of instance that you want to create: " << std::endl;
    std::cout << "[1]: M4.large" << std::endl;
    std::cout << "[2]: T2.large" << std::endl;
    std::cin >> instOpt;

    switch(instOpt) {
        case 1:
            instType = "m4.large";
            break;
        case 2:
            instType = "t2.large";
            break;
        default:
            std::cout << "This is not an available option!" << std::endl;
            return;
    }

     std::cout << "Enter number of instance that you want to create (max 5): " << std::endl;
     std::cin >> instNo;

     if(instNo > 5) { 
        std::cout << "Invalid number of instances!" << std::endl;
        return;
    }

    std::ostringstream oss;
    oss << "./installation/launchVMs.sh" << " " << awsAmi << " " << keyPairName << " " << securityGroupId << " " << instNo << " " << instType;

    std::cout << "Executing script: " << oss.str() << std::endl;

    std::cout << Command::exec(oss.str().c_str()) << std::endl;
}

void createClusters() {

}

void setup() {

}

int main(int argc, char ** argv) {

    bool isRunning = true;

    while(isRunning) {
        printMenu();

        char k = 0;
        std::cin >> k;

        switch(k) {
        case 's':
            setup();
            break;
        case 'k':
            createKeyPair();
            break;
        case 'g':
            createSecurityGroup();
            break;
        case 'v':
            launchVirtualMachine();
            break;
        case 'x':
            isRunning = false;
            std::cout << "Goodbye! :)" << std::endl;
            break;
        default:
            std::cout << "This is a wrong option. Try again!" << std::endl;
            break;
        }
    }

    return 0;
}


