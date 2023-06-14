import mysql.connector
import os
import pytest


@pytest.fixture()
def db_cursor():
    db = mysql.connector.connect(
        host=os.getenv("DBHOST"),
        port=os.getenv("DBPORT"),
        user=os.getenv("DBUSER"),
        passwd=os.getenv("DBPASSWD"),
        database=os.getenv("DBDATABASE")
    )
    cursor = db.cursor(dictionary=True)
    yield cursor
    cursor.close()
    db.close()
