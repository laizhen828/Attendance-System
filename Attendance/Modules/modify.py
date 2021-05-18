import os
import sys

import colorama
import socket
import sqlalchemy as db
from sqlalchemy.inspection import inspect
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.sql.expression import exists
from colorama import Fore, Style, Back
colorama.init(autoreset=True)
from .connect_db import attendance, employee, User, scanner, card, shift
import datetime
from datetime import datetime
from . import db_execute
import configparser

def modify(sqlcred, username):
    config = configparser.ConfigParser()
    config.read("config.ini")
    months = config.get('Static', 'months')
    departments = config.get('Parameters', 'employee departments')
    if not departments == 'Not Set':
        departments.split(',')
    nationalities = config.get('Parameters', 'employee nationalities').split((','))
    config['Parameters'] = {}
    Parameters = config['Parameters']
    db_url = 'mysql://' + sqlcred["user"] + ':' + sqlcred["password"] + '@' + sqlcred["ip"] + ':' + sqlcred["port"] + '/' + sqlcred["db_name"]
    engine = db.create_engine(db_url)
    print("Which category would you like to modify?")
    print("1. Parameters")
    while True:
        try:
            choice = int(input("Choice: "))
            while not 0 < choice < 2:
                choice = int(input("Choice: "))
            break
        except ValueError:
            print("Invalid Choice")
    if choice == 1:
        print("Which Parameter would you like to modify?")
        print("1. Employee Departments")
        print("2. Employee ID Length")
        print("3. Employee Nationalities")
        print("4. Card ID Length")
        print("5. Scanner ID Length")
        print("6. Scanner Locations")
        print("7. Date Format")
        print("8. Time Format")
        while True:
            try:
                choice = int(input("Choice: "))
                while not 0 < choice < 9:
                    choice = int(input("Choice: "))
                break
            except ValueError:
                print("Invalid Choice")
        if choice == 1:
            print(departments)
            if departments == 'Not Set':
                print("There are no departments in the system yet!")
                confirm = input("Do you want to add a new department? (Y/N): ")
                while confirm not in ('Y', 'y', 'N', 'n'):
                    print(Fore.LIGHTRED_EX + "Invalid Option")
                    confirm = input("Do you want to add a new department? (Y/N): ")
                if confirm == 'Y' or confirm == 'y':
                    new_department = input("New Department Name: ")
                    while len(new_department) == 0:
                        print(Fore.LIGHTRED_EX + "Cannot be Blank!")
                        new_department = input("New Department Name: ")
                    config.set('Parameters', 'employee departments', str(new_department))
                    with open("config.ini", 'w') as f:
                        config.write(f)
                else:
                    return
            else:
                print("Which of the departments you want to edit?")
                for department in departments:
                    print(str(departments.index(department) + 1) + ". " + department)
                while True:
                    try:
                        choice = int(input("Choice: "))
                        while not 0 < choice < len(departments):
                            choice = int(input("Choice: "))
                        break
                    except ValueError:
                        print("Invalid Choice")
                old_department = departments[choice - 1]
                print("Editing Department: " + Fore.LIGHTCYAN_EX + old_department)
                print("What would you like to do?")
                print("1." + Fore.LIGHTYELLOW_EX + "Edit Department Name")
                print("2." + Fore.LIGHTRED_EX + "Delete This Department")
                while True:
                    try:
                        choice = int(input("Choice: "))
                        while not 0 < choice < 3:
                            choice = int(input("Choice: "))
                        break
                    except ValueError:
                        print("Invalid Choice")
                if choice == 1:
                    new_department = input("New Department Name: ")
                    while len(new_department) == 0:
                        print(Fore.LIGHTRED_EX + "Cannot be Blank!")
                        new_department = input("New Department Name: ")
                    departments[departments.index(old_department)] = new_department
                    departments_write = ""
                    for department in departments:
                        departments_write = departments_write + department + ","
                    departments_write = departments_write[:-1]
                    Parameters['Employee Departments'] = departments_write
                    with open("config.ini", "w") as f:
                        config.write(f)




