import sqlite3
import os.path


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_name = 'chessDB.db'
    db_path = os.path.join(base_dir, db_name)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    statement = "CREATE TABLE events_dim_cleaned(event_id INT NOT NULL, " \
                "date TEXT," \
                "event_name TEXT," \
                "state TEXT);"
    c.execute(statement)
    conn.close()


if __name__ == "__main__":
    main()
