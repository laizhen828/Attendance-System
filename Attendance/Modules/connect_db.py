import os
import colorama
import sqlalchemy as db
from sqlalchemy.inspection import inspect
from sqlalchemy_utils import database_exists, create_database
from colorama import Fore, Style, Back
from werkzeug.security import generate_password_hash, check_password_hash
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
User = db.Table(
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
            print("Creating Default Admin Account...")
            print("Username: " + Fore.LIGHTYELLOW_EX + "admin")
            print("Password: " + Fore.LIGHTYELLOW_EX + "admin")
            query = db.insert(User).values(
                username="admin",
                name="admin",
                email="admin@admin.com",
                password=generate_password_hash("admin",method='SHA256')
            )
            print("Attempt to Update Database Table...")
            from .add import db_execute
            db_execute(engine, query)
            print("Proceeding to Authentication...")
            return
        else:
            print("Database Schema (" + Fore.CYAN + db_name + Fore.RESET + ") already exists!")
            print("Proceeding to Authentication...")
            return
    except:
        print(f"Unable to connect to MySQL Database on ({ip}:{port})")

def authentication(sqlcred):
    db_url = 'mysql://' + sqlcred["user"] + ':' + sqlcred["password"] + '@' + sqlcred["ip"] + ':' + sqlcred["port"] + '/' + sqlcred["db_name"]
    engine = db.create_engine(db_url)
    while True:
        try:
            print(" ")
            print("[Login]")
            username = input("Username: ")
            password = input("Password: ")
            authentication_query = db.select([User]).where(User.columns.username == username)
            username_exists = engine.connect().execute(authentication_query).fetchone()
            username_check = username_exists[0]
            password_check = username_exists[3]
            if username_exists:
                if check_password_hash(password_check, password):
                    print(Fore.LIGHTGREEN_EX + "Login Successful")
                    print("Proceeding to Main Menu...")
                    print(" ")
                    return "Authenticated", username
                else:
                    print(Fore.LIGHTRED_EX + "Authentication Failed")
                    return "Unauthenticated"
            else:
                print(Fore.LIGHTRED_EX + "Authentication Failed")
                return "Unauthenticated"
        except:
            print(Fore.LIGHTRED_EX + "Authentication Failed")
            return "Unauthenticated"