import sqlite3

conn = sqlite3.connect("E:\Python\Aquila_microblog\db\microblog.db")
cur = conn.cursor()
cur.execute("select username, password from user where username='c' and password='c'")
print cur.fetchall()
