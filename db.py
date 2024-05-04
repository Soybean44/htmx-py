import sqlite3

from flask import g

DATABASE = "database.db"
SCHEMA = "schema.sql"


def get_db() -> sqlite3.Connection:
    db = sqlite3.connect(DATABASE)
    return db


if __name__ == "__main__":
    # Setup Database #
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    with open(SCHEMA) as f:
        schema_script = f.read()
    c.executescript(schema_script)
    db.commit()
    db.close()
