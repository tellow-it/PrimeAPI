import psycopg2
from core.config import settings
import getpass
import datetime

from utils.hash_password import hashing_password


input_password = getpass.getpass("Input password for super user: ")

while len(input_password) < 5:
    input_password = getpass.getpass("Input password for super user: ")

hash_password = hashing_password(input_password)

name = "admin"
surname = "admin"
role = "admin"
password = hash_password
telephone = settings.ADMIN_TELEPHONE
created_at = datetime.datetime.now().isoformat()

try:
    conn = psycopg2.connect(settings.DATABASE_URL_R)
    curs = conn.cursor()
    query = f"INSERT INTO public.user (name, surname, role, password, telephone, created_at) " \
            f"values (%s,%s,%s,%s,%s,%s)"
    record_to_insert = (name, surname, role, password, telephone, created_at)
    curs.execute(query, record_to_insert)
    conn.commit()
    print("Success insert superuser")
except (Exception, psycopg2.DatabaseError) as err:
    print("ERROR: ", err)
finally:
    # closing database connection.
    if conn:
        curs.close()
        conn.close()
        print("Connection close")



