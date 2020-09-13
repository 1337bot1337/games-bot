import environ
import psycopg2


env = environ.Env()
config_db = env.db("CORE_DATABASE_URL")

conn = psycopg2.connect(
    "dbname='{NAME}' user='{USER}' host='{HOST}' password='{PASSWORD}' connect_timeout=5".format(**config_db)
)
conn.close()
