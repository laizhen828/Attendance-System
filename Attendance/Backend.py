import colorama
from colorama import Fore, Style, Back

from Modules.check_conf import check_conf
from Modules.connect_db import connect_db
from Modules.add import add

colorama.init(autoreset=True)

def main_menu(sqlcred):
    print(" ")
    print("[Main Menu]")
    print("What would you like to do?")
    print("1. Add New Data.")
    print("2. Modify Existing Data.")
    print("3. View Data(s).")
    print(Fore.LIGHTYELLOW_EX +  "4. Exit.")
    while True:
        try:
            choice = int(input("Choice: "))
            while not 0 < choice < 5:
                choice = int(input("Choice: "))
            break
        except ValueError:
            print("Invalid Choice")
    if choice == 1:
        add(sqlcred)
        return main_menu(sqlcred)
    elif choice == 2:
        print("Modify")
        return main_menu(sqlcred)
    elif choice == 3:
        print("View")
        return main_menu(sqlcred)
    elif choice == 4:
        print(Fore.LIGHTYELLOW_EX + "Exiting program...")
        exit()

if __name__ == '__main__':
    check = check_conf()
    sqlcred = {}
    sqlcred["ip"] = check[1]
    sqlcred["port"] = check[2]
    sqlcred["user"] = check[3]
    sqlcred["password"] = check[4]
    sqlcred["db_name"] = check[5]
    if check[0] == "True":
        main_menu(sqlcred)