import sqlite3
import os.path


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'testDB.db')
    print(db_path)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    values = [(123, 'M', 'WA'),
              (132, 'M', 'PA'),
              (213, 'F', 'Europe')
    ]
    statement = "DROP TABLE IF EXISTS USERS;"
    c.execute(statement)
    statement = "CREATE TABLE users(uid INT PRIMARY KEY NOT NULL,gender TEXT,state TEXT);"
    c.execute(statement)
    c.executemany('INSERT INTO users VALUES (?, ?, ?)', values)
    c.execute("SELECT * FROM USERS;")
    print(c.fetchall())
    c.execute("SELECT * FROM USERS;")
    statement = "DROP TABLE IF EXISTS user_events;"
    c.execute(statement)
    statement = "CREATE TABLE user_events(event_id INT NOT NULL, " \
                "user_id INT NOT NULL," \
                "date TEXT," \
                "event_name TEXT," \
                "reg_before INT," \
                "reg_after INT," \
                "quick_before INT," \
                "quick_after INT," \
                "blitz_before INT," \
                "blitz_after INT," \
                "section TEXT," \
                "state TEXT," \
                "FOREIGN KEY (user_id) REFERENCES users(uid));"
    c.execute(statement)
    values = [(	1, 1, 12-31-94, 'event name', 2000, 2010, 2100, 2200, 2300, 2400, 'section name', 'HI')]
    c.executemany('INSERT INTO user_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', values)
    c.execute("SELECT * FROM user_events;")
    print(c.fetchall())
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
