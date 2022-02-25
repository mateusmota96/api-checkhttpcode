import mysql.connector

# URLS for INSERT into table
urls = [
    'http://www.sitedomotao.com.br',
    'http://www.localhost/'
]

conn = mysql.connector.connect(
    host="localhost",
    user="botmon",
    password="seila123",
)
c = conn.cursor()

# CREATE DB
c.execute("""CREATE DATABASE IF NOT EXISTS monitoring""")
conn.commit()

try:
    # CREATE TABLE
    c.execute("USE monitoring")
    conn.commit()
    c.execute("""CREATE TABLE monitor (
        id int auto_increment,
        client varchar(50),
        url varchar(100),
        http_code int,
        status varchar(50),                    
        error int,
        notify int,
        send_notify int,
        PRIMARY KEY (id)
        )""")
    conn.commit()
except:
    print("Error into DB creation")

# INSERT URLS INTO monitor
for url in urls:
    execute = "INSERT INTO monitor VALUES (null, 'SERRANO', '" + str(url) + "', 200, 'OK' , 0, 0, 0)"
    c.execute(execute)
    conn.commit()

conn.close()