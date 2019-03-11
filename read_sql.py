import sqlite3
import os.path


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_name = 'testDB.db'
    db_path = os.path.join(base_dir, db_name)
    print(db_path)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM users;")
    users = c.fetchall()
    print(users)
    print("Number of users: ", len(users))
    c.execute("SELECT * FROM user_events;")
    events = c.fetchall()
    print("Number of events: ", len(events))
    print(events)
    conn.close()
    return users, events


if __name__ == "__main__":
    main()
