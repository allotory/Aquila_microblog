import sqlite3

conn = sqlite3.connect("E:\Python\Aquila_microblog\db\microblog.db")
cur = conn.cursor()
cur.execute("select * from post")
print cur.fetchall()
