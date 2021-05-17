import os
import colorama
import configparser
import socket
from colorama import Fore, Style, Back
colorama.init(autoreset=True)
config = configparser.ConfigParser()
from .connect_db import connect_db

def check_conf():
    prompt_installation_msg = "Please Select Installation Method (" + Fore.GREEN + "1" + Fore.RESET + "/" + Fore.LIGHTRED_EX + "2" + Fore.RESET + "): "
    if os.path.exists("config.cfg"):
        try:
            print("Config File Exists. " + Fore.GREEN + "[OK]")
            config.read("config.cfg")
            ip = config.get('Configurations', 'mysql_ip')
            port = config.get('Configurations', 'mysql_port')
            user = config.get('Configurations', 'mysql_user')
            password = config.get('Configurations', 'mysql_password')
            db_name = config.get('Configurations', 'mysql_db_name')
            connect_db(ip, port, user, password, db_name)
            return "True", ip, port, user, password, db_name
        except:
            print("An error occured while reading config file! [" + Fore.RED + "ERROR" + Fore.RESET + "]")
            print(sys.exc_info()[0])
            exit()
    else:
        config['Configurations'] = {}
        Configurations = config['Configurations']
        print("Config File does not exist. " + Fore.RED + "[X]")
        print("Performing first time setup...")
        print(" ")
        print("[" + Fore.BLUE + "First Time Setup" + Fore.RESET + "]")
        setup_option = input("Is the MySQL Server running on this machine? (Y/N): ")
        while setup_option not in ("Y", "y", "N", "n"):
            setup_option = input("Please Enter Y or N")
        if setup_option == "Y" or setup_option == "y":
            self_ip = socket.gethostbyname_ex(socket.gethostname())
            print("Fetching ALL Ip Addresses from all interfaces on this machine...")
            print("Which one of the IP Addressess below is your current network interface?")
            ipcount = 1
            for ip in self_ip[2]:
                print(str(ipcount) + ". " + str(ip))
                ipcount += 1
            while True:
                try:
                    ip_choice = int(input("Choice: "))
                    while not 0 < ip_choice < (len(self_ip[-1]) + 1 ):
                        ip_choice = int(input("Choice: "))
                    break
                except ValueError:
                    print("Enter from the choices above")
            selected_ip = self_ip[2][ip_choice - 1]
            Configurations['MySQL_IP'] = selected_ip
            Configurations['MySQL_Port'] = input("Please Enter the Port for MySQL (Default is 3306): ")
            print("Using default values for Mysql User (" + Fore.YELLOW + "rfidwebapp" + Fore.RESET + ")")
            Configurations['mysql_user'] = 'rfidwebapp'
            print("Using default values for Mysql Password (" + Fore.YELLOW + "rfid12345" + Fore.RESET + ")")
            Configurations['mysql_password'] = 'rfid12345'
            print("Using default values for Mysql Database Name (" + Fore.YELLOW + "rfid" + Fore.RESET + ")")
            Configurations['mysql_db_name'] = 'rfid'
        elif setup_option == "N" or setup_option == "n":
            pass
        with open("config.cfg", "a") as f:
            config.write(f)
        f.close()
        return check_conf()