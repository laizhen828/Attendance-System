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

def add(sqlcred, username):
    config = configparser.ConfigParser()
    config.read("config.ini")
    months = config.get('Static', 'months')
    departments = config.get('Parameters', 'employee departments')
    if not departments == 'Not Set':
        departments.split(',')
    nationalities = config.get('Parameters', 'employee nationalities').split((','))
    db_url = 'mysql://' + sqlcred["user"] + ':' + sqlcred["password"] + '@' + sqlcred["ip"] + ':' + sqlcred["port"] + '/' + sqlcred["db_name"]
    engine = db.create_engine(db_url)
    print("Which category would you like to register?")
    print("1. Employee")
    print("2. Card")
    print("3. Shift")
    print("4. Scanner")
    if username == 'admin':
        print(Fore.LIGHTCYAN_EX + "5. User Account")
        print(Fore.LIGHTYELLOW_EX + "6. Exit to main menu")
    else:
        print(Fore.LIGHTYELLOW_EX + "5. Exit to main menu")
    while True:
        try:
            choice = int(input("Choice: "))
            while not 0 < choice < 7:
                choice = int(input("Choice: "))
            break
        except ValueError:
            print("Invalid Choice")
    if choice == 1:
        print("[Register New Employee]")
        shifts = engine.connect().execute(db.select([shift])).fetchall()
        if not shifts:
            print(Fore.LIGHTYELLOW_EX + "There are no shifts available yet, please add new shift before registering new employee.")
            return
        elif departments == 'Not Set':
            print(Fore.LIGHTYELLOW_EX + "There are no departments available yet, please add new deparments before registering new employee.")
            return
        else:
            print("Please Key in the following details: ")
            id = input("Employee ID: ")
            search_query = db.select([employee]).where(employee.columns.id == id)
            id_exists = engine.connect().execute(search_query).fetchone()
            #print(id_exists)
            while id_exists:
                print(Fore.LIGHTRED_EX + "Employee already exist!")
                id = input("Employee ID: ")
                search_query = db.select([employee]).where(employee.columns.id == id)
                id_exists = engine.connect().execute(search_query).fetchone()
            while len(id) < 14:
                print(Fore.RED + "Invalid Format!")
                id = input("Employee ID: ")
            name = input("Employee Name: ")
            while len(name) < 1:
                print(Fore.RED + "Must be at least 1 character!")
                name = input("Employee Name: ")
            while True:
                try:
                    gender = input("Employee Gender (M/F): ")
                    while len(gender) < 1 or gender not in ('M', 'F', 'm', 'f'):
                        print(Fore.RED + "Invalid Format!")
                        gender = input("Employee Gender (M/F): ")
                    break
                except:
                    print(Fore.RED + "Invalid Format!")
            if gender == 'M' or gender == 'm':
                gender = 'Male'
            else:
                gender == 'Female'
            currentyear = datetime.now().strftime("%Y")
            sliced_currentyear = int(currentyear[2:4])
            birthyear = id[0:2]
            if sliced_currentyear - int(birthyear) < 0:
                birthyear = "19" + str(birthyear)
            else:
                birthyear = currentyear[0:2] + str(birthyear)
            age = int(currentyear) - int(birthyear)
            birthmonth = months[int(id[2:4]) - 1]
            birthdate = id[4:6] + "/" + birthmonth + "/" + birthyear
            print("Available Departments:")
            for department in departments:
                print(str(int(departments.index(department)) + 1) + ". " + department)
            while True:
                try:
                    choice = int(input("Choice: "))
                    while not 0 < choice < (len(departments) + 1):
                        choice = int(input("Choice: "))
                    break
                except ValueError:
                    print(Fore.RED + "Invalid Choice")
            department = departments[choice - 1]
            shifts = engine.connect().execute(db.select([shift])).fetchall()
            print("Available Shifts:")
            for row in shifts:
                print(str(shifts.index(row) + 1) + ". " + row[0])
            while True:
                try:
                    choice = int(input("Choice: "))
                    while not 0 < choice < (len(shifts) + 1):
                        choice = int(input("Choice: "))
                    break
                except ValueError:
                    print(Fore.RED + "Invalid Choice")
            employee_shift = shifts[choice - 1][0]
            print("Employee Shift: " + employee_shift)
            print("Available Nationalities: ")
            for nationality in nationalities:
                print(str(nationalities.index(nationality) + 1) + ". " + nationality)
            while True:
                try:
                    choice = int(input("Choice: "))
                    while not 0 < choice < (len(nationalities) + 1):
                        choice = int(input("Choice: "))
                    break
                except ValueError:
                    print(Fore.RED + "Invalid Choice")
            nationality = nationalities[choice - 1]
            query = db.insert(employee).values(
                id = id,
                name = name,
                gender = gender,
                age = age,
                birthdate = birthdate,
                department = department,
                shift = employee_shift,
                nationality = nationality
            )
            print("Attempt to Update Database Table...")
            db_execute(engine, query)
    elif choice == 2:
        print("[Register New Card]")
        print("Please Key in the following details: ")
        rfidno = input("Card RFID no.: ")
        search_query = db.select([card]).where(card.columns.rfidno == rfidno)
        id_exists = engine.connect().execute(search_query).fetchone()
        # print(id_exists)
        while id_exists:
            print(Fore.LIGHTRED_EX + "RFID Card already exist!")
            id = input("Card RFID no.: ")
            search_query = db.select([card]).where(card.columns.rfidno == rfidno)
            id_exists = engine.connect().execute(search_query).fetchone()
        now = datetime.now()
        reg_date = now.strftime("%d-%m-%Y")
        print("Registration Date: " + reg_date)
        employee_id = input("Register with Employee ID: ")
        search_query = db.select([employee]).where(employee.columns.id == employee_id)
        id_exists = engine.connect().execute(search_query).fetchone()
        # print(id_exists)
        while not id_exists:
            print(Fore.LIGHTRED_EX + "Employee does not exist!")
            employee_id = input("Employee ID: ")
            search_query = db.select([employee]).where(employee.columns.id == employee_id)
            id_exists = engine.connect().execute(search_query).fetchone()
        query = db.insert(card).values(
            rfidno = rfidno,
            reg_date = reg_date,
            employee_id = employee_id
        )
        print("Attempt to Update Database Table...")
        db_execute(engine, query)
    elif choice == 3:
        print("[Register New Shift]")
        print("Please Key in the following details: ")
        new_shift = input("Shift name: ")
        search_query = db.select([shift]).where(shift.columns.shift == new_shift)
        id_exists = engine.connect().execute(search_query).fetchone()
        # print(id_exists)
        while id_exists:
            print(Fore.LIGHTRED_EX + "Shift already exist!")
            new_shift = input("Shift name: ")
            search_query = db.select([shift]).where(shift.columns.shift == new_shift)
            id_exists = engine.connect().execute(search_query).fetchone()
        start_time = input("Start Time: (?am/pm)")
        end_time = input("Start Time: (?am/pm)")
        query = db.insert(shift).values(
            shift=new_shift,
            start_time=start_time,
            end_time=end_time
        )
        print("Attempt to Update Database Table...")
        db_execute(engine, query)
    elif choice == 4:
        print("[Register New Scanner]")
        print("Please Key in the following details: ")
        scanner_id = input("Scanner ID: ")
        search_query = db.select([scanner]).where(scanner.columns.id == scanner_id)
        id_exists = engine.connect().execute(search_query).fetchone()
        # print(id_exists)
        while id_exists:
            print(Fore.LIGHTRED_EX + "Scanner already exist!")
            scanner_id = input("Scanner ID: ")
            search_query = db.select([scanner]).where(scanner.columns.id == scanner_id)
            id_exists = engine.connect().execute(search_query).fetchone()
        model = input("Scanner Model: ")
        location = input("Scanner Location: ")
        query = db.insert(scanner).values(
            id=scanner_id,
            model=model,
            location=location,
            occupied='Not Yet'
        )
        print("Attempt to Update Database Table...")
        db_execute(engine, query)
    elif choice == 5:
        if username == "admin":
            print("[Register New User Account]")
            print("Please Key in the following details: ")
            new_user = input("Username: ")
            while len(new_user) == 0 or len(new_user) > 20:
                print(Fore.LIGHTRED_EX + "Username too short or too long")
                new_user = input("Username: ")
            search_query = db.select([User]).where(User.columns.username == new_user)
            id_exists = engine.connect().execute(search_query).fetchone()
            # print(id_exists)
            while id_exists:
                print(Fore.LIGHTRED_EX + "Username already exist!")
                new_user = input("Username: ")
                while len(new_user) == 0 or len(new_user) > 20:
                    print(Fore.LIGHTRED_EX + "Username too short or too long")
                    new_user = input("Username: ")
                search_query = db.select([User]).where(User.columns.username == new_user)
                id_exists = engine.connect().execute(search_query).fetchone()
            name = input("Name: ")
            while len(name) == 0 or len(name) > 30:
                print(Fore.LIGHTRED_EX + "Name too short or too long")
                name = input("Username: ")
            email = input("Email: ")
            while len(email) == 0 or len(email) > 30:
                print(Fore.LIGHTRED_EX + "Email too short or too long")
                email = input("Email: ")
            password1 = input("Password: ")
            while len(password1) == 0 or len(password1) > 30:
                print(Fore.LIGHTRED_EX + "Password too short or too long")
                password1 = input("Password: ")
            password2 = input("Retype Password: ")
            while len(password2) == 0 or len(password2) > 30:
                print(Fore.LIGHTRED_EX + "Password too short or too long")
                password2 = input("Password: ")
            if password1 != password2:
                while password1 != password2:
                    print(Fore.LIGHTRED_EX + "Passwords Does Not Match!")
                    password1 = input("Password: ")
                    while len(password1) == 0 or len(password1) > 30:
                        print(Fore.LIGHTRED_EX + "Password too short or too long")
                        password1 = input("Password: ")
                    password2 = input("Retype Password: ")
                    while len(password2) == 0 or len(password2) > 30:
                        print(Fore.LIGHTRED_EX + "Password too short or too long")
                        password2 = input("Password: ")
            from .connect_db import generate_password_hash
            if password1 == password2:
                query = db.insert(User).values(
                    username=new_user,
                    name=name,
                    email=email,
                    password=generate_password_hash(password1,method='SHA256')
                )
                print("Attempt to Update Database Table...")
                db_execute(engine, query)



def db_execute(engine, query):
    while True:
        try:
            confirm = input("Are you Confirm with the details above? (Y/N): ")
            while confirm not in ('Y', 'y', 'N', 'n'):
                print(Fore.LIGHTRED_EX + "Invalid Option")
                confirm = input("Are you Confirm with the details above? (Y/N): ")
            if confirm == 'Y' or confirm == 'y':
                try:
                    engine.connect().execute(query)
                    print(Fore.GREEN + "Success!")
                except:
                    print(Fore.RED + "Failed")
                    print(sys.exc_info())
            else:
                print("Returning to Main Menu...")
                return
        except:
            print(Fore.LIGHTRED_EX + "Invalid Option")
