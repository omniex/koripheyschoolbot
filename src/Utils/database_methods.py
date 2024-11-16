import sqlite3


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
    cursor.execute("SELECT * FROM USERS")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return users


def execute_command(command):
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    cursor.execute(command)
    db.commit()
    cursor.close()
    db.close()
