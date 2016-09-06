from scrapy.selector import Selector
import re
import string

#filename="14d9010d785bd789.eml"
#A sample of ziprecruiter emails
rootpath="C:\\Users\\Jake\\Documents\\Cont. Ed\\gyb\\gyb-0.47-windows\\gyb\\GYB-GMail-Backup-jacobbumpus@gmail.com\\";
filenames=['2016\\6\\13\\1554924c574b6a76.eml']#,'2016\\4\\9\\153fa922a5f9bdbf.eml','2016\\4\\9\\153fa92177338d3e.eml','2016\\4\\9\\153fa920a121b3fc.eml','2016\\4\\9\\153fa91fb9f3897c.eml','2016\\4\\9\\153fa91ed925f0ba.eml','2016\\4\\9\\153fa91db35c0ea0.eml','2016\\4\\8\\153f5872a3b3fbb7.eml','2016\\4\\8\\153f5870b603087b.eml','2016\\4\\8\\153f586fbbb971d9.eml','2016\\4\\8\\153f586e611d24a3.eml','2016\\4\\8\\153f586d6ae4bca4.eml','2016\\4\\8\\153f586d3ea2a9fd.eml','2016\\4\\7\\153f066fb836459b.eml','2016\\4\\7\\153f066e4954f1c9.eml','2016\\4\\7\\153f066d391e80ca.eml','2016\\4\\7\\153f066be36a3d72.eml','2016\\4\\7\\153f066ab9a9c28e.eml','2016\\4\\7\\153f066995af1203.eml','2016\\4\\6\\153eb8acb14b1a1c.eml','2016\\4\\6\\153eb8ab1b5d8ade.eml','2016\\4\\6\\153eb8a946906a32.eml','2016\\4\\6\\153eb8a815280fbf.eml','2016\\4\\6\\153eb8a736c6ead6.eml','2016\\4\\6\\153eb8a5f792222c.eml','2016\\4\\5\\153e631e77d54f9d.eml','2016\\4\\5\\153e631d458ceedf.eml','2016\\4\\5\\153e631c1fd6e58f.eml','2016\\4\\5\\153e631ada92b691.eml','2016\\4\\5\\153e6319cc67f4b7.eml','2016\\4\\5\\153e6318ed3d2176.eml','2016\\4\\4\\153e0ee0ed4c968c.eml','2016\\4\\4\\153e0ee01e2be4c7.eml','2016\\4\\4\\153e0ede6d9da693.eml','2016\\4\\4\\153e0edd32587826.eml','2016\\4\\4\\153e0edc3e120e63.eml','2016\\4\\4\\153e0edaffec67ac.eml','2016\\4\\3\\153dbb555ee3428d.eml','2016\\4\\3\\153dbb53d3e695aa.eml','2016\\4\\3\\153dbb52690b2fa9.eml','2016\\4\\3\\153dbb508c49b644.eml','2016\\4\\3\\153dbb4f9c50e7a2.eml','2016\\4\\3\\153dbb4e8d88ef79.eml','2016\\4\\2\\153d6d98d73e13c1.eml','2016\\4\\2\\153d6d97e01c994c.eml','2016\\4\\2\\153d6d96d9460a6d.eml','2016\\4\\2\\153d6d95b46b16af.eml','2016\\4\\2\\153d6d94eb2cb985.eml','2016\\4\\2\\153d6d940163e468.eml','2016\\4\\1\\153d18168899af28.eml','2016\\4\\1\\153d18158872e302.eml','2016\\4\\1\\153d181424289187.eml','2016\\4\\1\\153d18131aeca3ed.eml','2016\\4\\1\\153d1811e308d503.eml','2016\\4\\1\\153d1810dc7cac7c.eml','2016\\3\\31\\153cc09e3c838cbc.eml']

for file in filenames:
	f = open(rootpath+file, 'r')
	body1 = f.read()
	body = string.replace(body1,"=\n","")
	body = string.replace(body,"color: ","color:")
	try:
		JobTitles=Selector(text=body).xpath("//a/span[@style='3D\"font-size:16px;color:#12C;line-height:1.8em;text-decoration:underline;\"']/text()").extract()
		#print JobTitles
		PostingCompanies=Selector(text=body).xpath("//a/span[@style='3D\"color:#444;font-weight:600;line-height:1.6em;\"']/text()").extract()
		# print PostingCompanies
		a_divs=Selector(text=body).xpath("//td[@width='3D\"97%\"']/a/text()").extract()
		Cities=[]
		States=[]
		PostingSiteNames=[]
		for a_text in a_divs:
			#print a_text,str(string.find(a_text," in ")>-1),str(string.find(a_text, ", ")>-1)
			if string.find(a_text," in ")>-1: 
				if string.find(a_text, ", ")>-1:
					Cities.append(string.capwords(a_text.split(", ")[0].split("in ")[1]))
					if a_text.split(", ")[1]=="Connecticut":
						States.append("CT")
					else:
						States.append(a_text.split(", ")[1])
				else:
					Cities.append("empty")
					States.append("empty")
			elif string.find(a_text,"on ")>-1:
				PostingSiteNames.append(a_text.split("on ")[1].split("(")[0].strip())
		#print Cities
		#print States
		#print PostingSiteNames
		links=Selector(text=body).xpath("//td/a/@href").extract()
		PostingURLsRaw = [URL for URL in links if string.find(URL,"https://www.ziprecruiter.com/clk/")>-1];
		PostingURLs=[URL[3:-1] for URL in PostingURLsRaw]
		#print PostingSiteNames

	except:
		print "Job title, Posting Company & URL : Selector failed"
		pause = raw_input()
		pause = raw_input()
	try:
		for i in range(0, len(JobTitles)):
			print "JobTitle: "+JobTitles[i]
			print "PostingSiteName: "+PostingSiteNames[i]
			print "PostingURL: "+PostingURLs[i]
			print "PostingCompany: "+ PostingCompanies[i]
			print "City: "+Cities[i]
			print "State: "+States[i]
			pause = raw_input()
	except:
		print "Error in JobTitles, PostingURLs or JobInfoTDs"
		pause = raw_input()
		pause = raw_input()
	pause = raw_input()