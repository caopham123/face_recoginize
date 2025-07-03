import psycopg2

DB_NAME = "db_test"
USERNAME = "postgres"
PASSWORD = "postgres"
HOST_DB = "localhost"
PORT_DB = 5432
conn = psycopg2.connect(database = DB_NAME, 
                        user = USERNAME, 
                        host= HOST_DB,
                        password = PASSWORD,
                        port = PORT_DB)