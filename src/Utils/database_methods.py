import sqlite3
import re

from aiogram import types


def create_db():
    db = sqlite3.connect('users.db')
    cursor = db.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS USERS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        surname TEXT,
        grade TEXT,
        phone_number TEXT,
        name_in_tg TEXT,
        username TEXT,
        user_id integer
        )''')

    db.commit()
    cursor.close()
    db.close()


def register_user(data):
    db = sqlite3.connect('users.db')
    cursor = db.cursor()

    create_db()

    cursor.execute("""INSERT INTO USERS (name, surname, grade, phone_number, name_in_tg, username, user_id) VALUES (
    '%s', '%s', '%s', '%s', '%s', '%s', '%d')""" % (data["name"], data["surname"], data["grade"], data["phone_number"],
                                                    data["name_in_tg"], data["username"], data["id"]))
    db.commit()
    cursor.close()
    db.close()


def get_all_users():
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM USERS")
    except Exception as err:
        print(err)
        create_db()
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return users


def is_registered(msg: types.Message):
    users_list = get_all_users()
    iss = False
    if users_list:
        for user in users_list:
            if msg.from_user.id == user[7]:
                iss = True
                break
    return iss


def execute_command(command):
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    cursor.execute(command)
    db.commit()
    cursor.close()
    db.close()


def get_command(command):
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    cursor.execute(command)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def search_for_direct_user(given_data):
    exp = r'(.)*' + given_data.lower() + r'(.)*'
    data = get_all_users()
    find_data = []
    for user in data:
        # print(user[1].lower())
        # print(exp.lower())
        # print(re.findall(exp, str(user[1]).lower()))
        if re.findall(exp, str(user[1]).lower()) or re.findall(exp, str(user[2]).lower()):
            find_data.append(user)
    # print(find_data)
    return find_data
