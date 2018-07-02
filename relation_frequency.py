import pandas as pd
import numpy as np
import psycopg2 as psy
from fuzzywuzzy import fuzz,process
import time

conn = psy.connect("dbname=edu_learning user=aabhaschauhan password=eval2017!")
cur = conn.cursor()
cur.execute("SELECT f_l FROM node_edge1")# UNION ALL SELECT doc_id, sentence_index, lemmas FROM sentences1")
row = cur.fetchone()
print cur.rowcount
temp_dict = dict()
stoplist = set('for a of the and to in where there i I ; who also am were here if was be being then that this as at what how it can we is with on you or there appear , \' they likely took take not more are their `` been become make made an from has have than between % about -lrb- -rrb- will them vary find must will them sb rb'.split())
strictlist = ['0','/','1','2','3','4','5','6','7','8','9','%','&','$','+',',','=','.',"'",'--','\\']

while row is not None:
	(rel,) = row
	temp = [a for a in rel.split() if not(a in stoplist) and not(any([True for b in strictlist if b in a]))]
	for abc  in temp:
		if not(abc in temp_dict):	temp_dict[abc] = 1
		else:	temp_dict[abc] += 1
	row= cur.fetchone()

print "Number of relation words possible:	", len(temp_dict)
k1 = [[a,b] for (a,b) in sorted(temp_dict.iteritems(), key=lambda (k,v):(v,k), reverse= True)]
pd.DataFrame(k1,columns=['relation_word','frequency']).to_csv('/media/aabhaschauhan/Data/ERIC/Results/relation_words_frequency_V2.0_AC.csv',encoding='utf-8')

	

