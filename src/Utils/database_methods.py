import sqlite3
import re
#import csv
import pandas as pd
from datetime import date, time, datetime

from aiogram import types

from src.config import settings


def create_users_db():
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
        user_id integer,
        role TEXT
        )''')

    db.commit()
    cursor.close()
    db.close()


def register_user(data):
    db = sqlite3.connect('users.db')
    cursor = db.cursor()

    create_users_db()

    cursor.execute("""INSERT INTO USERS (name, surname, grade, phone_number, name_in_tg, username, user_id, role) VALUES (
    '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s')""" % (
        data["name"], data["surname"], data["grade"], data["phone_number"],
        data["name_in_tg"], data["username"], data["id"], data["role"]))
    db.commit()
    cursor.close()
    db.close()


def get_all(db_name: str, table: str):
    try:
        db = sqlite3.connect(f'{db_name}.db')
    except Exception as err:
        print(err)
        return

    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table}")
    except Exception as err:
        print(err)
        create_users_db()
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def is_registered(msg: types.Message):
    users_list = get_all('users', 'USERS')
    iss = False
    if users_list:
        for user in users_list:
            if msg.from_user.id == user[7]:
                iss = True
                break
    return iss


def search_for_direct_data(db_name: str, table: str, given_data):
    exp = r'(.)*' + given_data.lower() + r'(.)*'
    data = get_all(db_name, table)
    find_data = []
    for user in data:
        # print(user[1].lower())
        # print(exp.lower())
        # print(re.findall(exp, str(user[1]).lower()))
        if re.findall(exp, str(user[1]).lower()) or re.findall(exp, str(user[2]).lower()):
            find_data.append(user)
    # print(find_data)
    return find_data


def create_db_food():
    db = sqlite3.connect('food.db')
    cursor = db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FOOD (
            id INTEGER PRIMARY KEY,
            meal TEXT NOT NULL,
            answers INTEGER,
            good INTEGER,
            bad INTEGER,
            percentage_good REAL,
            datetime TEXT NOT NULL
        )
    ''')

    db.commit()
    cursor.close()
    db.close()


def register_meal(data):
    db = sqlite3.connect('food.db')
    cursor = db.cursor()

    create_db_food()

    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    percentage = float(data["good"] * 100) / (float(data["good"]) + float(data["bad"]))

    cursor.execute("""INSERT INTO FOOD (meal, answers, good, bad, percentage_good, datetime) VALUES (
    '%s', '%d', '%d', '%d', '%f', '%s')""" % (
        data["meal"], int(data["good"]) + int(data["bad"]), data["good"], data["bad"], percentage, current_datetime))

    db.commit()
    cursor.close()
    db.close()


# def get_all_food():
#     db = sqlite3.connect('food.db')
#     cursor = db.cursor()
#     try:
#         cursor.execute("SELECT * FROM FOOD")
#     except Exception as err:
#         print(err)
#         create_db_food()
#     meals = cursor.fetchall()
#     cursor.close()
#     db.close()
#     return meals


def execute_command(command, db_name: str):
    db = sqlite3.connect(f'{db_name}.db')
    cursor = db.cursor()
    cursor.execute(command)
    db.commit()
    cursor.close()
    db.close()


def get_command(command, db_name: str):
    db = sqlite3.connect(f'{db_name}.db')
    cursor = db.cursor()
    cursor.execute(command)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


# using import csv
# def export_to_csv(db_name: str, table: str):
#     try:
#         with open(f'{db_name}.csv', 'wt') as fp:
#             writer = csv.writer(fp, delimiter=',')
#             writer.writerows(get_command(f'SELECT * FROM {table}', db_name))
#             return True
#     except Exception as err:
#         print(err)


def export_to_excel(db_name: str, table: str):
    try:
        data = get_command(f'SELECT * FROM {table}', db_name)
        conn = sqlite3.connect(f'{db_name}.db')
        cursor = conn.execute(f'SELECT * FROM {table}')
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        df.to_excel(f'{db_name}.xlsx', index=False, sheet_name='meals')
        return True
    except Exception as err:
        print(err)


def sync_db_users():
    data = get_all('users', 'USERS')
    for user in data:
        settings.user_ids.add(user[7])
        if user[8] == 'council':
            settings.council_ids.add(user[7])
        elif user[8] == 'teacher':
            settings.teacher_ids.add(user[7])


def get_role(user_id):
    if user_id in settings.admin_ids:
        return 'admin'
    elif user_id in settings.teacher_ids:
        return 'teacher'
    elif user_id in settings.council_ids:
        return 'council'
    else:
        return 'user'


async def change_role(user_id: int, role: str, msg: types.Message):
    if role not in settings.roles:
        await msg.answer(f'{role} is a wrong role')
        return
    if user_id not in settings.user_ids:
        await msg.answer('User is not registered')
        return
    role_old = get_role(user_id)
    print(role, role_old)
    if role_old == role:
        await msg.answer('Role is already set')
        return

    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    cursor.execute("UPDATE USERS SET role = ? WHERE user_id = ?", (role, user_id))
    db.commit()
    cursor.close()
    db.close()

    if role_old == 'admin':
        settings.admin_ids.discard(user_id)
    elif role_old == 'teacher':
        settings.teacher_ids.discard(user_id)
    elif role_old == 'council':
        settings.council_ids.discard(user_id)

    if role == 'admin':
        settings.admin_ids.add(user_id)
    elif role == 'teacher':
        settings.teacher_ids.add(user_id)
    elif role == 'council':
        settings.council_ids.add(user_id)

    await msg.answer('Role is successfully changed')
    await msg.bot.send_message(user_id, f'Ваша роль изменилась с {role_old} на {role}')