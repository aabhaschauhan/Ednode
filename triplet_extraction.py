import os
import sys
import fileinput
from subprocess import call
import psycopg2

print("\nDESCRIPTION: 'triplet_extraction.py' will create triplets of (subject, relation, object) using JSONL file created in previous step.\n\n\n")
aft = input("Triplet extraction to be run on which database?\n1-- ONLY article abstracts (DEFAULT)\n2-- Article abstracts and full text of articles(for all articles possible)\n\nResponse:	")

def replace_some(filename,value, totalset):
	t11 = filename.rfind(".")
	filename1 = filename[:t11]+"_temp"+filename[t11:]
	os.rename(filename,filename1)
	o = open(filename,"a")
	for line in open(filename1):
		for i in range(value):	line = line.replace(totalset[2*i],totalset[(2*i)+1])	
		o.write(line)
	o.close()
	call(['sudo','rm',filename1])

def compile_some(name):
	tt = raw_input("\nCompile "+name+"? (y/n)\n\nResponse:   ")
	while (tt!='y' and tt!='n'):
		tt = raw_input("\nEnter valid response (y/n):	")
	if tt.lower()=='y':	call(["/home/aabhaschauhan/local/bin/deepdive","redo",name])

conn = psycopg2.connect("dbname=edu_learning user=aabhaschauhan password=eval2017!")
cur = conn.cursor()

os.chdir('/media/aabhaschauhan/Data/Edu')
if (aft == 1):
	replace_some('/media/aabhaschauhan/Data/Edu/app.ddlog',3,["articles1","articles","sentences1","sentences","node_edge1","node_edge"])	
	call(["/home/aabhaschauhan/local/bin/deepdive","corenlp","start"])
	call(["/home/aabhaschauhan/local/bin/deepdive","compile"])
	compile_some("articles")
	replace_some('/media/aabhaschauhan/Data/Edu/run/process/ext_sentences_by_nlp_markup/run.sh',1,['& /media/aabhaschauhan/Data/Edu/udf/nlp_markup.sh','& bash /media/aabhaschauhan/Data/Edu/udf/nlp_markup.sh'])
	compile_some("sentences")
	replace_some('/media/aabhaschauhan/Data/Edu/run/process/ext_node_edge_by_map_triplet/run.sh',1,['& /media/aabhaschauhan/Data/Edu/udf/map_factor_mention1_old.py','& python /media/aabhaschauhan/Data/Edu/udf/map_factor_mention1_old.py'])
	compile_some("node_edge")
	call(["/home/aabhaschauhan/local/bin/deepdive","corenlp","stop"])
	o = open('/media/aabhaschauhan/Data/ERIC/Results/triplets_from_abstracts.csv','w')
	cur.copy_to(o,'node_edge',sep=',')
	print "\n\n FILE CREATED: 'triplets_from_abstracts.csv' SAVED AT '/media/aabhaschauhan/Data/ERIC/Results'\n\n"
else:
	replace_some('/media/aabhaschauhan/Data/Edu/app.ddlog',3,["articles","articles1","sentences","sentences1","node_edge","node_edge1"])
	call(["/home/aabhaschauhan/local/bin/deepdive","corenlp","start"])
	call(["/home/aabhaschauhan/local/bin/deepdive","compile"])
	compile_some("articles1")
	replace_some('/media/aabhaschauhan/Data/Edu/run/process/ext_sentences1_by_nlp_markup/run.sh',1,['& /media/aabhaschauhan/Data/Edu/udf/nlp_markup.sh','& bash /media/aabhaschauhan/Data/Edu/udf/nlp_markup.sh'])
	replace_some('/media/aabhaschauhan/Data/Edu/run/process/ext_node_edge1_by_map_triplet/run.sh',1,['& /media/aabhaschauhan/Data/Edu/udf/map_factor_mention1_old.py','& python /media/aabhaschauhan/Data/Edu/udf/map_factor_mention1_old.py'])
	compile_some("sentences1")
	compile_some("node_edge1")
	call(["/home/aabhaschauhan/local/bin/deepdive","corenlp","stop"])
	o = open('/media/aabhaschauhan/Data/ERIC/Results/triplets_from_fulltext.csv','w')
	cur.copy_to(o,'node_edge1',sep=',')
	print "\n\n FILE CREATED: 'triplets_from_fulltext.csv' SAVED AT '/media/aabhaschauhan/Data/ERIC/Results'\n\n"

