from scrapy.selector import Selector
import re
import string

#filename="14d9010d785bd789.eml"
#A sample of Dice emails about mid-way through the database history
rootpath="C:\\Users\\Jake\\Documents\\Cont. Ed\\gyb\\gyb-0.47-windows\\gyb\\GYB-GMail-Backup-jacobbumpus@gmail.com\\";
filenames=['2016\\4\\24\\1544828cdcf8c6df.eml']#,'2016\\4\\23\\154430353dfb512c.eml','2016\\4\\22\\1543dc1cd369eee6.eml','2016\\4\\21\\15438b3dea8f5afc.eml','2016\\4\\20\\1543389ff9a7c0ef.eml','2016\\4\\19\\1542e6ab338790a4.eml','2016\\4\\18\\154293efa9a145e3.eml','2016\\4\\17\\1542416db1684692.eml','2016\\4\\16\\1541ed951a82e219.eml','2016\\4\\15\\15419cc7978d06cf.eml','2016\\4\\14\\15414a2510222ba0.eml','2016\\4\\13\\1540f7e5d115b250.eml','2016\\4\\12\\1540a577c03e1eb3.eml','2016\\4\\10\\153ffefc04e0c4aa.eml','2016\\4\\9\\153faca27324dab1.eml','2016\\4\\8\\153f5ad5412b014a.eml','2016\\4\\7\\153f07def0dbf967.eml','2016\\4\\6\\153eb57378691597.eml','2016\\4\\5\\153e64ec64c54b2f.eml','2016\\4\\4\\153e12767a62868c.eml','2016\\4\\3\\153dc023c4f15b11.eml','2016\\4\\2\\153d6d9e81ff4480.eml','2016\\4\\1\\153d196abfc2f328.eml','2016\\3\\31\\153cc8aa18af4824.eml','2016\\3\\30\\153c76adbf3bcc19.eml','2016\\3\\29\\153c23b09293bec2.eml','2016\\3\\28\\153bd0c9029f26a2.eml','2016\\3\\26\\153b2c8b90a96bae.eml','2016\\3\\25\\153ad998f0483d8d.eml','2016\\3\\9\\1535b7d3c4ff0205.eml','2016\\3\\8\\1535657a1f704053.eml','2016\\3\\7\\153513461aada424.eml','2016\\3\\5\\15346db577113605.eml','2016\\3\\4\\15341a514769efe8.eml','2016\\3\\3\\1533c76b5d28ab67.eml','2016\\3\\2\\15337766b77ec8ec.eml','2016\\3\\1\\1533241c3f05f132.eml','2016\\2\\29\\1532d1fa39ff58e6.eml','2016\\2\\28\\15327e260bd21da1.eml','2016\\2\\27\\15322ce69e9e882c.eml','2016\\2\\26\\1531d946df25fe1e.eml','2016\\2\\25\\15318eb11e926cde.eml','2016\\2\\24\\15313456ad91f92c.eml','2016\\2\\22\\15308f856cfa4b1c.eml','2016\\2\\21\\15303f05d2147efc.eml','2016\\2\\20\\152fec6cc2666f9a.eml','2016\\2\\19\\152f99e2cd3cd4c7.eml','2016\\2\\18\\152f47fd3f773a35.eml','2016\\2\\17\\152ef6712fd0264c.eml','2016\\2\\16\\152ea28b7a8f7a1d.eml','2016\\2\\15\\152e4e8d5fb97ecd.eml','2016\\2\\14\\152dfc3eee854c21.eml','2016\\2\\13\\152dad9a3dc77942.eml','2016\\2\\12\\152d591c3f264e0a.eml','2016\\2\\11\\152d076b00747470.eml','2016\\2\\10\\152cb5512f655628.eml','2016\\2\\9\\152c628879f084e3.eml','2016\\2\\8\\152c0f612ca8da52.eml','2016\\2\\7\\152bbb8c06772063.eml']

for file in filenames:
	f = open(rootpath+file, 'r')
	body = f.read()
	body=string.replace(body,"=\n","")
	print file
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
			print "JobTitle: "+JobTitles[i]
			print "PostingURL: "+PostingURLs[i][3:-2]
			jobInfoTD=JobInfoTDs[i]
			CoSplit=jobInfoTD.split(" | ")
			print "PostingCompany: "+ CoSplit[0].strip()	
			locSplit=CoSplit[1].split(", ")
			print "City: "+string.capwords(locSplit[0].strip().split("/")[0])
			print "State: "+string.capwords(locSplit[1].strip().split("/")[0])
	except IndexError:
		print "IndexError in JobTitles, PostingURLs or JobInfoTDs"