import sqlite3
import os
import re
from scrapy.selector import Selector

con = sqlite3.connect("msg-db.sqlite")
con.isolation_level = None
cur = con.cursor()

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
	if sqlite3.complete_statement(sqlInsert):
		try:
			sqlInsert = sqlInsert.strip()
			cur.executemany(sqlInsert,paramIterable)
			if sqlInsert.lstrip().upper().startswith("SELECT"):
				return cur.fetchall()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]
		sqlInsert = ""
		
# get the message filenames (with full path)
# traverse root directory, and list directories as dirs and files as files
listFiles=[]

# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk("C:\\Users\\Jake\\Documents\\Cont. Ed\\gyb\\gyb-0.47-windows\\gyb\\GYB-GMail-Backup-jacobbumpus@gmail.com"):
	path = root.split('\\')
	for file in files:
		f = open(root+"\\"+file, 'r')
		body = f.read()
		msgFilename = path[-3]+"\\"+path[-2]+"\\"+path[-1]+"\\"+file
		# pull each of the slots for the senders table: Message_Num, SenderName, SenderEmail, SenderIP
		Message_Num, SenderName, SenderEmail, SenderIP = 0,"","",""
		# get the message_num
		Message_Num=RunSQL("SELECT message_num FROM messages WHERE message_filename LIKE "+"'"+msgFilename+"'"+";")[0][0]
		print "Message_Num : "+str(Message_Num)
		# get the sender name; if none listed, assign it as null
		try:
			SenderName=re.findall("(?<=From: )[^\r\n]+", body)[0]
		except IndexError:
			SenderName=""
		# get the sender's email address; if none listed, assign it as null
		try:
			SenderEmail=re.findall("(?<=Received: from )\S+", body)[0]
		except IndexError:
			SenderEmail=""
		# get the sender's IP address; if none listed, assign it as null
		try:
			SenderIP=re.findall("(?<=Received: from )[^\r\n]+", body)[0]
			SenderIP=re.findall("([0-9]+.[0-9]+.[0-9]+.[0-9]+)",SenderIP)[0]
		except IndexError:
			SenderIP=""
		print "SenderName : "+SenderName
		print "SenderEmail : "+SenderEmail
		print "SenderIP : "+SenderIP
		listFiles.append((Message_Num,SenderName,SenderEmail,SenderIP))

RunSQLMany('INSERT INTO senders VALUES (?,?,?,?);', listFiles)


		
# loop through the filenames
	# open each file
	# pull each of the slots for the jobs table
		# JobID, Message_Num, PostingURL, PostingDate, PostingCompany, CompanyJobID, Industry, JobTitle, YearsExperience, ExperienceLevel, Skills, Salary, City, State, ZipCode


con.close()