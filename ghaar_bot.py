import pymysql

conn = pymysql.connect(host='localhost', user='root',
                       passwd='Amirparsa96', db='Ghaar')

cur = conn.cursor()
cur.execute("SELECT * FROM group_users")

print(cur.description)
print()

for row in cur:
    print(row)

cur.close()
conn.close()
