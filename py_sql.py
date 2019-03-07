import sqlite3
import os.path


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'testDB.db')
    print(db_path)
    #print(os.getcwd())
    conn = sqlite3.connect(db_path)
    #conn.text_factory = sqlite3.OptimizedUnicode
    c = conn.cursor()
    values = [(123, 'M', 'WA'),
              (132, 'M', 'PA'),
              (213, 'F', 'Europe')
    ]
    c.execute("SELECT * FROM users;")
    #c.executemany('INSERT INTO users VALUES (?, ?, ?)', values)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
