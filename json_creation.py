import xml.etree.ElementTree as ET
import subprocess
import json
import os
from os.path import isfile, join, getsize, exists
#from TextRank import get_best_sentence, get_senteces_ranks
import pandas as pd

print("\nDESCRIPTION: 'json_creation.py' will create a JSONL file of all the peer-reviewed research articles downloaded from the ERIC database\n\n\n")
ch = input ("choose\n1-- use existing database\n2-- use a new database\n\nResponse:")
while (ch!=1 and ch!=2):
	ch = input("\n Enter a valid response (1/2):")
if (ch==1):
	mypath = "/media/aabhaschauhan/Data/ERIC/Completed_Databases" 
	mypath1 = "/media/aabhaschauhan/Data/ERIC/Database"
else:
	mypath = raw_input("enter  filepath ")
aft = input("What will the database include?\n1-- ONLY article abstracts\n2-- article abstracts and full text of articles(for all articles possible)\n\nResponse:	")
while (aft!=1 and aft!=2 ):
	aft = input("\nEnter a valid response (1/2):	")
ns= {'ab1':'http://www.eric.ed.gov' ,'ab2':'http://purl.org/dc/elements/1.1/' ,'ab3':'http://purl.org/dc/terms/'}

f1 = [mypath + "/" + f for f in os.listdir(mypath) if isfile(join(mypath, f))] 
f2 = [mypath1 + "/" + f for f in os.listdir(mypath1) if isfile(join(mypath1, f))]

l1 = len(f1)
onlyfiles = f1 + f2
d2=dict()
i=1
j=1
tmp123=[]

for m123,doc1 in enumerate(onlyfiles):
	tree = ET.parse(doc1)
	root = tree.getroot()
	print m123, doc1[doc1.rfind('/')+1:]
	k=0
	l=0
	for record in root.findall('record'):
		for metadata in record.findall('metadata'):
			ident = metadata.find('ab2:identifier',ns).text
			print j, ident			
			titl = metadata.find('ab2:title',ns).text
			cont = metadata.find('ab2:description',ns).text
			peerrev = metadata.find('ab1:peer_reviewed',ns).text			
			if (cont != None) and (peerrev=='T'):
				i += 1
				print i, doc1[-12:], ident	
				source = metadata.find('ab2:source',ns).text 	
				key = []
				for keys in metadata.findall('ab2:subject',ns):
					key = key + [keys.text]
				d2["id"]= ident
				d2["source"] = source
				d2["title"] = titl
				d2["keywords"] = key	
				d2["publisher"] = metadata.find('ab2:publisher',ns).text
				d2["peerrev"] = peerrev
				d2["doc"] = doc1[doc1.rfind('/')+1:]
				
				if exists('/media/aabhaschauhan/Data/ERIC/Articles/'+ident+'.pdf') and (aft==2):
					subprocess.call(['pdftotext','/media/aabhaschauhan/Data/ERIC/Articles/'+ident+'.pdf','/media/aabhaschauhan/Data/ERIC/temp1.txt'])
					try:
						with open('/media/aabhaschauhan/Data/ERIC/temp1.txt', 'r') as f1:
							abc = f1.read().replace("\n"," ")
							f1.close()
					except Exception:	abc = cont
					subprocess.call(['rm','/media/aabhaschauhan/Data/ERIC/temp1.txt'])
				else:	abc = cont
				d2["content"] = abc

				with open('/media/aabhaschauhan/Data/Edu/input/eric/temp.jsonl', 'a') as fp:
					json.dump(d2, fp, encoding="utf-8")
					fp.write(os.linesep)
			j += 1
			k +=1

if (aft==1):
	os.rename('/media/aabhaschauhan/Data/Edu/input/eric/temp.jsonl','/media/aabhaschauhan/Data/Edu/input/eric/articles.jsonl')
	print("File saved to: "+'/media/aabhaschauhan/Data/Edu/input/eric/articles.jsonl')
else:
	os.rename('/media/aabhaschauhan/Data/Edu/input/eric/temp.jsonl','/media/aabhaschauhan/Data/Edu/input/eric/articles1.jsonl')
	print("File saved to: "+'/media/aabhaschauhan/Data/Edu/input/eric/articles1.jsonl')
	
#--------------------------------------------------------------------------------------------------------------------------------------------

				#sub_dict = get_senteces_ranks(metadata.find('ab2:description',ns).text)
				#d2["content"] = get_best_sentence(metadata.find('ab2:description',ns).text, sub_dict, 4) #3 best sentences
				#d2["content"] = cont
				#with open('/media/aabhaschauhan/Data/Edu/input/eric/articles_main1.jsonl', 'a') as fp:
				#	json.dump(d2, fp)
				#	fp.write(os.linesep)
#	tmp123 += [(doc1[-12:],k,l)]
#print pd.DataFrame(tmp123,columns=["File","Total_Count", "Selected_Count"])
'''
				subprocess.call(['pdftotext','/media/aabhaschauhan/Data/ERIC/Articles/'+ident+'.pdf','/media/aabhaschauhan/Data/ERIC/temp1.txt'])
				try:
					with open('/media/aabhaschauhan/Data/ERIC/temp1.txt', 'r') as f1:
						try:	abc = f1.read()
						except Exception:	continue
						d2["content"] = abc
						f1.close()
				except Exception:	continue
				subprocess.call(['rm','/media/aabhaschauhan/Data/ERIC/temp1.txt'])
				with open('/media/aabhaschauhan/Data/Edu/input/eric/articles_huge.jsonl', 'a') as fp:
					json.dump(d2, fp)
					fp.write(os.linesep)
				i+=1
				l+=1
			elif exists('/media/aabhaschauhan/Data/ERIC/Articles/'+ident+'.pdf'):
				subprocess.call(['rm','/media/aabhaschauhan/Data/ERIC/Articles/'+ident+'.pdf'])
'''
