import sqlite3
import os.path


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_name = 'chessDB.db'
    db_path = os.path.join(base_dir, db_name)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    statement = "DROP TABLE IF EXISTS user_events_dim;"
    c.execute(statement)
    statement = "CREATE TABLE user_events_dim(event_id INT NOT NULL, " \
                "user_id INT NOT NULL," \
                "date TEXT," \
                "reg_before TEXT," \
                "reg_after TEXT," \
                "state TEXT," \
                "FOREIGN KEY (user_id) REFERENCES users(uid));"
    c.execute(statement)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
