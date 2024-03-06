import sqlite3


def createDatabase(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = 1")

    # Create tables
    c.execute("CREATE TABLE IF NOT EXISTS User("
              "username TEXT PRIMARY KEY,"
              "password TEXT,"
              "fullname TEXT,"
              "email TEXT,"
              "telno TEXT)")  # telno as TEXT because it may contain + sign as in +90

    c.execute("CREATE TABLE IF NOT EXISTS Category("
              "cid INTEGER PRIMARY KEY,"
              "cname TEXT)")

    c.execute("CREATE TABLE IF NOT EXISTS Advertisement("
              "aid INTEGER PRIMARY KEY AUTOINCREMENT,"
              "title TEXT,"
              "description TEXT,"
              "isactive BOOLEAN,"
              "username TEXT,"
              "cid INTEGER,"
              "FOREIGN KEY (cid) REFERENCES Category(cid),"
              "FOREIGN KEY (username) REFERENCES User(username))")

    conn.commit()
    conn.close()


def insertRecords(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    # Insert records
    users = [("root", "root123", "Root", "root", "root"),
             ("admin", "admin123", "Admin", "admin", "admin")]
    c.executemany("INSERT INTO User VALUES(?, ?, ?, ?, ?)", users)

    categories = [(1, "Clothes"), (2, "Technology"), (3, "Cars"), (4, "Food"), (5, "Drink")]
    c.executemany("INSERT INTO Category VALUES(?, ?)", categories)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    db_name = "website.db"
    createDatabase(db_name)
    # insertRecords(db_name)
