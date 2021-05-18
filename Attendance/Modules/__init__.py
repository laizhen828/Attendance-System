import os
import colorama
import configparser
import socket
import sqlalchemy as db
from sqlalchemy.inspection import inspect
from sqlalchemy_utils import database_exists, create_database
from colorama import Fore, Style, Back
colorama.init(autoreset=True)
import configparser


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