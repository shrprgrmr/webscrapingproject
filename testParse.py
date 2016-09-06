from scrapy.selector import Selector
import re

filename="14adb067e316f79e.eml"

f = open(filename, 'r')
body = f.read()
print "file : " + filename.split(".")[0]
#print "Job title example : "+ Selector(text=body).xpath("//div/a[@class='3D\"jobtitle']/text()").extract()[0]
print "Sender name : " + re.findall("(?<=From: )[^\r\n]+", body)[0]
try:
	print "Sender address : " + re.findall("(?<=Received: from )\S+", body)[0]
except IndexError:
	print "Assign null instead"
try:
	match=re.findall("(?<=Received: from )[^\r\n]+", body)[0]
	match=re.findall("([0-9]+.[0-9]+.[0-9]+.[0-9]+)",match)[0]
	print "Sender IP : " + match
except IndexError:
	print "Assign null instead"