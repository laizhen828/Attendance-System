import colorama
from colorama import Fore, Style, Back

from Modules.check_conf import check_conf
from Modules.connect_db import connect_db, authentication
from Modules.add import add
from Modules.modify import modify

colorama.init(autoreset=True)

def main_menu(sqlcred, username):
    print(" ")
    print("[Main Menu]")
    print("What would you like to do?")
    print("1. Add New Data.")
    print("2. Modify Existing Data.")
    print("3. View Data(s).")
    print(Fore.LIGHTYELLOW_EX +  "4. Exit.")
    print(Fore.LIGHTYELLOW_EX +  "5. Log Out.")
    while True:
        try:
            choice = int(input("Choice: "))
            while not 0 < choice < 6:
                choice = int(input("Choice: "))
            break
        except ValueError:
            print("Invalid Choice")
    if choice == 1:
        add(sqlcred, username)
        return main_menu(sqlcred, username)
    elif choice == 2:
        modify(sqlcred, username)
        return main_menu(sqlcred, username)
    elif choice == 3:
        print("View")
        return main_menu(sqlcred, username)
    elif choice == 4:
        print(Fore.LIGHTYELLOW_EX + "Exiting program...")
        exit()
    elif choice == 5:
        print(Fore.LIGHTYELLOW_EX + "Logging Out...")
        login(sqlcred)

def login(sqlcred):
    login_check = authentication(sqlcred)
    while not login_check[0] == 'Authenticated':
        login_check = authentication(sqlcred)
    if login_check[0] == 'Authenticated':
        print("Viewing as " + Fore.LIGHTCYAN_EX + login_check[1])
        main_menu(sqlcred, login_check[1])

if __name__ == '__main__':
    print("[" + Fore.LIGHTCYAN_EX + "Attendance System " + Fore.LIGHTGREEN_EX + "Backend" + Fore.RESET + "]")
    print("Performing Conig Check...")
    check = check_conf()
    sqlcred = {}
    sqlcred["ip"] = check[1]
    sqlcred["port"] = check[2]
    sqlcred["user"] = check[3]
    sqlcred["password"] = check[4]
    sqlcred["db_name"] = check[5]
    if check[0] == "True":
        login(sqlcred)