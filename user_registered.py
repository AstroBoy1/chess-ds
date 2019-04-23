import sqlite3
import os.path


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_name = 'chessDB.db'
    db_path = os.path.join(base_dir, db_name)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    #c.execute("SELECT uid, COUNT(uid) FROM users INNER JOIN user_events on users.uid = user_events.user_id GROUP BY users.uid ORDER BY COUNT(UID);")
    statement = "INSERT INTO events_dim SELECT event_id, date, event_name, state FROM user_events GROUP BY event_id;"
    #statement = "SELECT * FROM events_dim;"
    user_registered_statement = "INSERT INTO user_events_dim SELECT event_id, user_id, date, reg_before, reg_after, state FROM user_events;"
    c.execute(statement)
    counts = c.fetchall()
    #print("Number of dates: ", len(counts))
    print(counts)
    conn.close()


if __name__ == "__main__":
    main()
