import sqlite3
import os
import re
import string
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
		
#An array of 4-tuples to hold the Senders table records
listFiles=[]

#An array of 16-tuples to hold the Jobs table records
#	NOTE: Many of these columns will be empty on the first pass through the emails.
#		  After extracting the PostingURL's, we can try to scrape data for some of the empty columns 
JobPostings=[]

#traverse root directory, and list directories as dirs and files as files
#for root, dirs, files in os.walk("C:\\Users\\Jake\\Documents\\Cont. Ed\\gyb\\gyb-0.47-windows\\gyb\\test"):
#	path = root.split('\\')
#^Can't os.walk the whole set for time being since only DICE selectors are determined/included
#So instead, just look at the Dice emails
root="C:\\Users\\Jake\\Documents\\Cont. Ed\\gyb\\gyb-0.47-windows\\gyb\\GYB-GMail-Backup-jacobbumpus@gmail.com"
files=RunSQL("SELECT messages.message_filename FROM Senders JOIN messages ON messages.message_num=senders.message_num WHERE senders.sendername like '%Dice%';")
files=[str(f[0]) for f in files]
print "files:\r"+str(files)
for file in files:
	f = open(root+"\\"+file, 'r')
	body = f.read()
	body=string.replace(body,"=\n","")
	#msgFilename = path[-3]+"\\"+path[-2]+"\\"+path[-1]+"\\"+file
	# #pull each of the slots for the senders table: Message_Num, SenderName, SenderEmail, SenderIP
	# Message_Num, SenderName, SenderEmail, SenderIP = 0,"","",""
	# #get the message_num
	Message_Num=RunSQL("SELECT message_num FROM messages WHERE message_filename LIKE "+"'"+file+"'"+";")[0][0]
	print "file : "+file
	print "Message_Num : "+str(Message_Num)
	# #get the sender name; if none listed, assign it as null
	# try:
		# SenderName=re.findall("(?<=From: )[^\r\n]+", body)[0]
	# except IndexError:
		# SenderName=""
	# #get the sender's email address; if none listed, assign it as null
	# try:
		# SenderEmail=re.findall("(?<=Received: from )\S+", body)[0]
	# except IndexError:
		# SenderEmail=""
	# #get the sender's IP address; if none listed, assign it as null
	# try:
		# SenderIP=re.findall("(?<=Received: from )[^\r\n]+", body)[0]
		# SenderIP=re.findall("([0-9]+.[0-9]+.[0-9]+.[0-9]+)",SenderIP)[0]
	# except IndexError:
		# SenderIP=""
	# print "SenderName : "+SenderName
	# print "SenderEmail : "+SenderEmail
	# print "SenderIP : "+SenderIP
	# listFiles.append((Message_Num,SenderName,SenderEmail,SenderIP))
	#pull each of the slots for the jobs table:
	#	JobID, Message_Num, PostingURL, PostingDate, PostingCompany, CompanyJobID, Industry, JobTitle, YearsExperience, ExperienceLevel, Skills, Salary, City, State, ZipCode
	
	#NOTE: added PostingSiteName column to Jobs table after this was run the first time
	#TODO: add a selector for PostingSiteName (if possible in Dice emails)
	
	#JobTitle & PostingURL
	try:		
		JobTitles=Selector(text=body).xpath("//td[@class='3D\"job-title\"']/a/text()").extract()
		PostingURLs=Selector(text=body).xpath("//td[@class='3D\"job-title\"']/a/@href").extract()
	except:
		print "Job title & URL : Selector failed"
	#JobInfo (should include "Company | City, State")
	try:
		JobInfoTDs=Selector(text=body).xpath("//td[@class='3D\"job-info\"']/text()").extract()
	except:
		print "Error selecting JobInfoTDs"
	try:
		for i in range(0, len(JobTitles)):
			JobTitle=JobTitles[i]
			print "JobTitle: "+JobTitle
			PostingURL=PostingURLs[i][3:-2]
			print "PostingURL: "+PostingURL
			jobInfoTD=JobInfoTDs[i]
			CoSplit=jobInfoTD.split(" | ")
			PostingCompany=CoSplit[0].strip()
			print "PostingCompany: "+PostingCompany
			locSplit=CoSplit[1].split(", ")
			City=string.capwords(locSplit[0].strip().split("/")[0])
			State=string.capwords(locSplit[1].strip().split("/")[0])
			print "City: "+City
			print "State: "+State
			#each record: (JobID,Message_Num,PostingURL,PostingDate,PostingCompany,WebsiteJobID,CompanyJobID,Industry,JobTitle,YearsExperience,ExperienceLevel,Skills,Salary,City,State,ZipCode)
			JobPostings.append((None,Message_Num,PostingURL,None,PostingCompany,None,None,None,JobTitle,None,None,None,None,City,State,None))
	except IndexError:
		print "IndexError in JobTitles, PostingURLs or JobInfoTDs"
		
#RunSQLMany('INSERT INTO senders VALUES (?,?,?,?);', listFiles)
RunSQLMany('INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);', JobPostings)

		
#loop through the filenames
	#open each file
	#pull each of the slots for the jobs table
		#JobID, Message_Num, PostingURL, PostingDate, PostingCompany, CompanyJobID, Industry, JobTitle, YearsExperience, ExperienceLevel, Skills, Salary, City, State, ZipCode


con.close()