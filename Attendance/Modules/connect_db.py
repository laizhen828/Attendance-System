import os
import colorama
import sqlalchemy as db
from sqlalchemy.inspection import inspect
from sqlalchemy_utils import database_exists, create_database
from colorama import Fore, Style, Back
colorama.init(autoreset=True)
metadata = db.MetaData()
attendance = db.Table(
                'attendance', metadata,
                db.Column('num_log' ,db.Integer, primary_key=True, nullable=False, autoincrement=True),
                db.Column('id', db.String(20)),
                db.Column('name', db.String(30)),
                db.Column('date', db.String(10)),
                db.Column('time', db.String(8)),
                db.Column('rfidno', db.String(10), db.ForeignKey('card.rfidno')),
                db.Column('scannerid', db.String(20), db.ForeignKey('scanner.id'))
            )
employee = db.Table(
    'employee', metadata,
    db.Column('id', db.String(20), primary_key=True, unique=True),
    db.Column('name', db.String(30)),
    db.Column('gender', db.String(6)),
    db.Column('age', db.Integer),
    db.Column('birthdate', db.String(12)),
    db.Column('department', db.String(20)),
    db.Column('shift', db.String(20), db.ForeignKey('shift.shift')),
    db.Column('nationality', db.String(20))
)
user = db.Table(
    'user', metadata,
    db.Column('username', db.String(20), primary_key=True, unique=True),
    db.Column('name', db.String(30)),
    db.Column('email', db.String(30)),
    db.Column('password', db.String(1000))
)
scanner = db.Table(
    'scanner', metadata,
    db.Column('id', db.String(20), primary_key=True, unique=True),
    db.Column('model', db.String(30)),
    db.Column('location', db.String(30)),
    db.Column('occupied', db.String(10))
)
card = db.Table(
    'card', metadata,
    db.Column('rfidno', db.String(10), primary_key=True, unique=True),
    db.Column('reg_date', db.String(12)),
    db.Column('employee_id', db.String(20), db.ForeignKey('employee.id'))
)
shift = db.Table(
    'shift', metadata,
    db.Column('shift', db.String(20), primary_key=True, unique=True),
    db.Column('start_time', db.String(20)),
    db.Column('end_time', db.String(20))
)

def connect_db(ip, port, user, password, db_name):
    db_url = 'mysql://' + user + ':' + password + '@' + ip + ':' + port + '/' + db_name
    print("Connecting to the MySQL Database...")
    engine = db.create_engine(db_url)
    try:
        print("Connection Successful - Connected to: Rfid Attendance Database")
        print("Checking Schema...")
        if not database_exists(engine.url):
            print("Database Schema (" + Fore.CYAN + db_name + Fore.RESET + ") does not exists!")
            print("Creating Schema (" + Fore.CYAN + db_name + Fore.RESET + ") ...")
            create_database(engine.url)
            print("Created Schema (" + Fore.CYAN + db_name + Fore.RESET + ")")
            inspector = inspect(engine)
            print("Creating Tables...")
            metadata.create_all(engine)
            print("Created the following tables:")
            for table_name in inspector.get_table_names():
                print(f"[{str(table_name)}]")
                for column in inspector.get_columns(table_name):
                    print(str(column['name']))
                print(" ")
            print("Proceeding to Main Menu...")
            return
        else:
            print("Database Schema (" + Fore.CYAN + db_name + Fore.RESET + ") already exists!")
            print("Proceeding to Main Menu...")
            return
    except:
        print(f"Unable to connect to MySQL Database on ({ip}:{port})")