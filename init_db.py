import psycopg2

connection = psycopg2.connect(database="rms",
                              host="localhost",
                              user="oliver",
                              password="test",
                              port="5432")

with open("schema.sql") as file:
    sql = file.read()

cursor = connection.cursor()

cursor.execute(sql)

connection.commit()
connection.close()
