__author__ = 'Junfeng'
import sqlite3


def connect_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    return (conn, c)


def create_users_table():
    (conn, c) = connect_db()
    c.execute('''CREATE TABLE users
             (name text, gender text, followers real, upvotes real, thanks real)''')
    conn.commit()


def insert_user_data_many(users_info):
    (conn, c) = connect_db()
    c.executemany("INSERT INTO users VALUES (?,?,?,?,?)", users_info)
    conn.commit()


def insert_user_data(user_info):
    (conn, c) = connect_db()
    c.execute("SELECT * FROM users WHERE name=?", (user_info[0],))
    if len(c.fetchall()) == 0:
        c.execute("INSERT INTO users VALUES(?,?,?,?,?)", user_info)
        conn.commit()
        print('insert complete')


def display_all_user():
    (conn, c) = connect_db()
    c.execute("SELECT * FROM users")
    print(c.fetchall())


if __name__ == '__main__':
    display_all_user()