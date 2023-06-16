import mysql.connector
import os
import pytest
from dotenv import load_dotenv

if 'ENV_FILE' in os.environ:
    load_dotenv(os.environ['ENV_FILE'])
else:
    load_dotenv()


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
