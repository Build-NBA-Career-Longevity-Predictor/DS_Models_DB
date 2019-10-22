import psycopg2
#from decouple import config

db_host = 'ec2-54-235-180-123.compute-1.amazonaws.com'
db_name = 'd9j38jtaim5u92'
db_user = 'ticqhtmsxabnow'
db_password = 'a3be20dbc652d427ca174fc64781b6bd33cd6bce42e3158ac3b2a9e642f0f383'

pg_conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
pg_cur = pg_conn.cursor()

# Query postgres db
show_tables = """
SELECT *
FROM player_stats
LIMIT 20;
"""

print(pg_cur.execute(show_tables))