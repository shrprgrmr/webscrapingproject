import sqlite3

con = sqlite3.connect("msg-db.sqlite")
con.isolation_level = None
cur = con.cursor()

sql="SELECT message_num FROM messages WHERE message_filename LIKE "+"'2015\\10\\14\\15066de37d5bacd8.eml'"+";"

purchases = [(111111,'Example.com <noreply@example.com>', 'example2@example.com', '11.11.11.11'),
			 (121212,'Example.com <noreply@example.com>', 'example2@example.com', '12.12.12.12')
            ]


def RunSQL(sql):
	if sqlite3.complete_statement(sql):
		try:
			sql = sql.strip()
			cur.execute(sql)
			if sql.lstrip().upper().startswith("SELECT"):
				return cur.fetchall()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]
		sql = ""
		
def RunSQLMany(sqlInsert,paramIterable):
	if sqlite3.complete_statement(sql):
		try:
			sqlInsert = sqlInsert.strip()
			cur.executemany(sqlInsert,paramIterable)
			if sqlInsert.lstrip().upper().startswith("SELECT"):
				return cur.fetchall()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]
		sqlInsert = ""
		
res=RunSQL(sql)
print res[0][0]

RunSQLMany('INSERT INTO senders VALUES (?,?,?,?);', purchases)

