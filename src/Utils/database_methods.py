import sqlite3
import re
import pandas as pd
from datetime import date, time, datetime

from aiogram import types

from src.Utils.keyboards import approve_or_reject
from src.config import settings


async def create_users_db():
    db = sqlite3.connect('db/users.db')
    cursor = db.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS USERS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        surname TEXT,
        grade TEXT,
        phone_number TEXT,
        name_in_tg TEXT,
        username TEXT,
        user_id integer,
        role TEXT,
        status TEXT,
        datetime TEXT
        )''')

    db.commit()
    cursor.close()
    db.close()


async def register_user(data):
    db = sqlite3.connect('db/users.db')
    cursor = db.cursor()

    await create_users_db()

    current_datetime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    cursor.execute("""INSERT INTO USERS (name, surname, grade, phone_number, name_in_tg, username, user_id, role, status, datetime) VALUES (
    '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s')""" % (
        data["name"], data["surname"], data["grade"], data["phone_number"],
        data["name_in_tg"], data["username"], data["id"], data["role"], data["status"], current_datetime))
    db.commit()
    cursor.close()
    db.close()

    settings.pending_users.add(data["id"])
    settings.user_ids.add(data["id"])

    await send_request_of_register(data)


async def create_news_db():
    db = sqlite3.connect('db/news.db')
    cursor = db.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS NEWS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        for_who TEXT,
        information TEXT,
        datetime TEXT
        )''')

    db.commit()
    cursor.close()
    db.close()


async def register_news(data):
    db = sqlite3.connect('db/news.db')
    cursor = db.cursor()

    await create_news_db()

    current_datetime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    cursor.execute("""INSERT INTO NEWS (for_who, information, datetime) VALUES ('%s', '%s', '%s')""" % (
        data["who"], data["information"], current_datetime))
    db.commit()
    cursor.close()
    db.close()


async def create_notes_table():
    db = sqlite3.connect("db/notes.db")
    cursor = db.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        note TEXT,
        interval INTEGER,
        next_send INTEGER
    )''')

    db.commit()
    db.close()


async def create_tickets_db():
    db = sqlite3.connect('db/tickets.db')
    cursor = db.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TICKETS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT,
        full_name TEXT,
        user_id INTEGER,
        ticket TEXT,
        room TEXT,
        status TEXT,
        datetime TEXT
        )''')

    db.commit()
    cursor.close()
    db.close()


async def create_ideas_db():
    db = sqlite3.connect('db/ideas.db')
    cursor = db.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS IDEAS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT,
        full_name TEXT,
        user_id INTEGER,
        ticket TEXT,
        status TEXT,
        datetime TEXT
        )''')

    db.commit()
    cursor.close()
    db.close()


async def register_idea(data):
    db = sqlite3.connect('db/ideas.db')
    cursor = db.cursor()

    await create_tickets_db()

    current_datetime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    cursor.execute("SELECT COUNT(*) FROM IDEAS WHERE user_id = ?", (data["user_id"],))
    request_count = cursor.fetchone()[0] + 1

    idea_id = f"{data["user_id"]}_{request_count}"

    cursor.execute(
        """INSERT INTO IDEAS (ticket_id, full_name, user_id, ticket, datetime) VALUES ('%s', '%s', '%d', '%s', '%s')""" % (
            idea_id, data["full_name"], data["user_id"], data["text"],
            current_datetime))
    db.commit()
    cursor.close()
    db.close()

    return idea_id


async def register_ticket(data):
    db = sqlite3.connect('db/tickets.db')
    cursor = db.cursor()

    await create_tickets_db()

    current_datetime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    cursor.execute("SELECT COUNT(*) FROM TICKETS WHERE user_id = ?", (data["user_id"],))
    request_count = cursor.fetchone()[0] + 1

    ticket_id = f"{data["user_id"]}_{request_count}"

    cursor.execute(
        """INSERT INTO TICKETS (ticket_id, full_name, user_id, ticket, room, status, datetime) VALUES ('%s', '%s', '%d', '%s', '%s', '%s', '%s')""" % (
            ticket_id, data["full_name"], data["user_id"], data["text"], data['room'], data["status"],
            current_datetime))
    db.commit()
    cursor.close()
    db.close()

    return ticket_id


async def get_all(db_name: str, table: str):
    try:
        db = sqlite3.connect(f'db/{db_name}.db')
    except Exception as err:
        print(err)
        return

    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table}")
    except Exception as err:
        print(err)
        await create_users_db()
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


async def is_registered(msg: types.Message):
    users_list = await get_all('users', 'USERS')
    iss = False
    if users_list:
        for user in users_list:
            if msg.from_user.id == user[7]:
                iss = True
                break
    return iss


async def search_for_direct_data(db_name: str, table: str, given_data):
    exp = r'(.)*' + given_data.lower() + r'(.)*'
    data = await get_all(db_name, table)
    find_data = []
    for user in data:
        if re.findall(exp, str(user[1]).lower()) or re.findall(exp, str(user[2]).lower()):
            find_data.append(user)
    return find_data


async def create_db_food():
    db = sqlite3.connect('db/food.db')
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


async def register_meal(data):
    db = sqlite3.connect('db/food.db')
    cursor = db.cursor()

    await create_db_food()

    current_datetime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    percentage = float(data["good"] * 100) / (float(data["good"]) + float(data["bad"]))

    cursor.execute("""INSERT INTO FOOD (meal, answers, good, bad, percentage_good, datetime) VALUES (
    '%s', '%d', '%d', '%d', '%f', '%s')""" % (
        data["meal"], int(data["good"]) + int(data["bad"]), data["good"], data["bad"], percentage, current_datetime))

    db.commit()
    cursor.close()
    db.close()


# def get_all_food():
#     db = sqlite3.connect('db/food.db')
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


async def execute_command(command, db_name: str):
    db = sqlite3.connect(f'db/{db_name}.db')
    cursor = db.cursor()
    cursor.execute(command)
    db.commit()
    cursor.close()
    db.close()


async def get_command(command, db_name: str):
    db = sqlite3.connect(f'db/{db_name}.db')
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


async def export_to_excel(db_name: str, table: str):
    try:
        data = await get_command(f'SELECT * FROM {table}', db_name)
        conn = sqlite3.connect(f'db/{db_name}.db')
        cursor = conn.execute(f'SELECT * FROM {table}')
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        df.to_excel(f'{db_name}.xlsx', index=False, sheet_name='meals')
        return True
    except Exception as err:
        print(err)


async def sync_db_users():
    data = await get_all('users', 'USERS')
    for user in data:
        settings.user_ids.add(user[7])
        if user[8] == 'council':
            settings.council_ids.add(user[7])
        elif user[8] == 'teacher':
            settings.teacher_ids.add(user[7])
        elif user[8] == 'banned':
            settings.banned_ids.add(user[7])
        elif user[8] == 'admin':
            if user[3] != '666':
                print(user[8], user[3], user[7])
                await set_db_grade(user[7], '666')

        if user[9] == 'pending':
            settings.pending_users.add(user[7])
        elif user[9] == 'rejected':
            settings.rejected_users.add(user[7])
        elif user[9] == 'approved':
            settings.approved_users.add(user[7])


async def set_db_grade(user_id, grade):
    db = sqlite3.connect('db/users.db')
    cursor = db.cursor()
    cursor.execute("UPDATE USERS SET grade = ? WHERE user_id = ?", (grade, user_id))
    db.commit()
    cursor.close()
    db.close()


async def sync_db_tickets():
    data = await get_all('tickets', 'TICKETS')
    for ticket in data:
        if ticket[5] == 'not completed':
            settings.not_completed_tickets.add(ticket[0])
            settings.not_completed_tickets.add(ticket[0])


async def get_role(user_id):
    if user_id in settings.admin_ids:
        return 'admin'
    elif user_id in settings.teacher_ids:
        return 'teacher'
    elif user_id in settings.council_ids:
        return 'council'
    elif user_id in settings.banned_ids:
        return 'council'
    else:
        return 'user'


async def get_status(user_id):
    if user_id in settings.pending_users:
        return 'pending'
    elif user_id in settings.rejected_users:
        return 'rejected'
    elif user_id in settings.approved_users:
        return 'approved'
    else:
        return 'None'


async def get_status_ticket(ticket_id):
    data = await get_all('tickets', 'TICKETS')
    for elem in data:
        if elem[1] == ticket_id:
            return elem[5]
    return 'None'


async def change_role(user_id: int, role: str, msg: types.Message):
    if role not in settings.roles:
        await msg.answer(f'{role} is a wrong role')
        return
    if user_id not in settings.user_ids:
        await msg.answer('User is not registered')
        return
    role_old = await get_role(user_id)
    # print(role, role_old)
    if role_old == role:
        await msg.answer('Role is already set')
        return

    db = sqlite3.connect('db/users.db')
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
    elif role_old == 'admin':
        settings.banned_ids.discard(user_id)
    elif role_old == 'user':
        settings.user_ids.discard(user_id)

    if role == 'admin':
        settings.admin_ids.add(user_id)
    elif role == 'teacher':
        settings.teacher_ids.add(user_id)
    elif role == 'council':
        settings.council_ids.add(user_id)
    elif role == 'banned':
        settings.banned_ids.add(user_id)

    await msg.answer('Role is successfully changed')
    #await msg.bot.send_message(user_id, f'Ваша роль изменилась с {role_old} на {role}')


async def change_status(user_id: int, status: str, msg: types.Message):
    if status not in settings.statuses:
        await msg.answer(f'{status} is a wrong status')
        return
    if user_id not in settings.user_ids:
        await msg.answer('User is not registered')
        return
    status_old = await get_status(user_id)
    if status_old == status:
        await msg.answer(f'Status is already set to {status}')
        return

    db = sqlite3.connect('db/users.db')
    cursor = db.cursor()
    cursor.execute("UPDATE USERS SET status = ? WHERE user_id = ?", (status, user_id))
    db.commit()
    cursor.close()
    db.close()

    if status_old == 'pending':
        settings.pending_users.discard(user_id)
    elif status_old == 'rejected':
        settings.rejected_users.discard(user_id)
    elif status_old == 'approved':
        settings.approved_users.discard(user_id)

    if status == 'pending':
        settings.pending_users.add(user_id)
    elif status == 'rejected':
        settings.rejected_users.add(user_id)
    elif status == 'approved':
        settings.approved_users.add(user_id)

    #await msg.answer('Status is successfully changed')
    #await msg.bot.send_message(user_id, f'Ваш статус заявки изменился с {status_old} на {status}')


async def change_status_ticket(ticket_id: str, status: str, msg: types.Message):
    if status not in settings.statuses_ticket:
        await msg.answer(f'"{status}" is a wrong status for ticket')
        return
    status_old = await get_status_ticket(ticket_id)
    if status_old == 'None':
        await msg.answer('Ticket is not registered')
        return
    if status_old == status:
        await msg.answer(f'Status of ticket is already set to {status}')
        return

    db = sqlite3.connect('db/tickets.db')
    cursor = db.cursor()
    cursor.execute("UPDATE TICKETS SET status = ? WHERE ticket_id = ?", (status, ticket_id))
    db.commit()
    cursor.close()
    db.close()

    user_id = ticket_id.split('_')[0]

    if status_old == 'not compeleted':
        settings.not_completed_tickets.discard(user_id)
    elif status_old == 'in work':
        settings.in_work_tickets.discard(user_id)
    elif status_old == 'completed':
        settings.completed_tickets.discard(user_id)

    if status == 'completed':
        settings.completed_tickets.add(user_id)
    elif status == 'in work':
        settings.in_work_tickets.add(user_id)
    elif status == 'not completed':
        settings.not_completed_tickets.add(user_id)

    #await msg.answer('Status is successfully changed')


async def send_request_of_register(user):
    from src.main import bot
    if user['id'] in settings.admin_ids:
        return
    for admin in settings.admin_ids:
        await bot.send_message(admin,
                               f'Новый пользователь подал заявку на регистрацию.\n\nИмя: {user['name']}\nФамилия: {user['surname']}\nКласс: {user['grade']}\nНомер телефона: {user['phone_number']}\nИмя в телеграм: {user['name_in_tg']}\nusername: @{user['username']}\nid: {user['id']}\n\nПожалуйста, рассмотрите её в кротчайшие сроки',
                               reply_markup=await approve_or_reject(user["id"]))


async def get_role_for_send(data):
    if data['who'] == '🥷Администрация':
        return 'admin'
    elif data['who'] == '🫂Совет Гимназистов':
        return 'council'
    elif data['who'] == '👸Учителя':
        return 'teacher'
    elif data['who'] == 'Все пользователи':
        return 'user'


async def get_ids_for_send(data):
    if data['who'] == '🥷Администрация':
        return settings.admin_ids
    elif data['who'] == '🫂Совет Гимназистов':
        return settings.council_ids
    elif data['who'] == '👸Учителя':
        return settings.teacher_ids
    elif data['who'] == 'Все пользователи':
        return settings.user_ids


async def get_full_name(user_id: int):
    data = await get_all('users', 'USERS')
    for i in data:
        if i[7] == int(user_id):
            return f'{i[1]} {i[2]}'
    return f'Пользователь не найден'
