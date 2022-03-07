import mysql.connector

# URLS for INSERT into table
urls = [
    'http://www.example.com',
    'http://www.example2.com'
]

conn = mysql.connector.connect(
    host="{db_host}",
    user="{db_user}",
    password="{db_passwd}",
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
