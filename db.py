__author__ = 'Junfeng'
import sqlite3


def connect_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    return (conn, c)


def create_users_table():
    (conn, c) = connect_db()
    c.execute('''CREATE TABLE users
             (name text, gender text, followers real, upvotes real, thanks real,time text)''')
    conn.commit()
    conn.close()


def insert_user_data_many(users_info):
    (conn, c) = connect_db()
    c.executemany("INSERT INTO users VALUES (?,?,?,?,?,?)", users_info)
    conn.commit()
    conn.close()


def insert_user_data(user_info):
    (conn, c) = connect_db()
    c.execute("INSERT INTO users VALUES(?,?,?,?,?,?)", user_info)
    conn.commit()
    conn.close()


def insert_candidate_data(user_info):
    (conn, c) = connect_db()
    c.execute("INSERT INTO candidates VALUES(?)", user_info)
    conn.commit()
    conn.close()


def get_all_candidates():
    (conn, c) = connect_db()
    c.execute("SELECT name FROM candidates")
    return c.fetchall()


def display_all_user():
    (conn, c) = connect_db()
    c.execute("SELECT * FROM users")
    print(c.fetchall())
    conn.close()


if __name__ == '__main__':
    display_all_user()