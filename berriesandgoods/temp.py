import psycopg2

hostname = 'localhost'
username = 'postgres'
password = ''
database = 'berry_db'

conn = psycopg2.connect(
    host=hostname, user=username, password=password, dbname=database)
conn.cursor().execute("CREATE TABLE temp")
breakpoint()
