import sqlite3

conn = sqlite3.connect("E:\Python\Aquila_microblog\db\microblog.db")
cur = conn.cursor()
#cur.execute("delete from followers where followed_id=4")
#conn.commit()
cur.execute("select * from followers")
print cur.fetchall()
