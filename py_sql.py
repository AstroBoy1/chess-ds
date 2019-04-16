import sqlite3
import os.path


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_name = 'testDB2.db'
    db_path = os.path.join(base_dir, db_name)
    print(db_path)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    statement = "DROP TABLE IF EXISTS USERS;"
    c.execute(statement)
    statement = "CREATE TABLE users(uid INT PRIMARY KEY NOT NULL,gender TEXT,state TEXT);"
    c.execute(statement)
    statement = "DROP TABLE IF EXISTS user_events;"
    c.execute(statement)
    statement = "CREATE TABLE user_events(event_id INT NOT NULL, " \
                "user_id INT NOT NULL," \
                "date TEXT," \
                "event_name TEXT," \
                "reg_before TEXT," \
                "reg_after TEXT," \
                "quick_before TEXT," \
                "quick_after TEXT," \
                "blitz_before TEXT," \
                "blitz_after TEXT," \
                "section TEXT," \
                "state TEXT," \
                "FOREIGN KEY (user_id) REFERENCES users(uid));"
    c.execute(statement)

    # Test inserting
    # values = [(123, 'M', 'WA'),
    #           (132, 'M', 'PA'),
    #           (213, 'F', 'Europe')
    # ]
    # c.executemany('INSERT INTO users VALUES (?, ?, ?)', values)
    # c.execute("SELECT * FROM USERS;")
    # print(c.fetchall())
    # c.execute("SELECT * FROM USERS;")
    # values = [(	1, 1, 12-31-94, 'event name', 2000, 2010, 2100, 2200, 2300, 2400, 'section name', 'HI')]
    # c.executemany('INSERT INTO user_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', values)
    # c.execute("SELECT * FROM user_events;")
    # print(c.fetchall())

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
