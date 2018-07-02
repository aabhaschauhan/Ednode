import psycopg2
import numpy as np
import time
import json
import os.path
from gensim import models
import pandas as pd
from itertools import combinations_with_replacement
		
stoplist1 = set('for a of the and to in where there i am were here if was be being then that this as at what how it can we is with on you or save demonstrate observe regain there appear , \' they likely more are their been an from has have than between about -lrb- -rrb- will them vary find perceive highest'.split())
stoplist = set('article author study program approach strategy analysis method course suggestion concept idea view people effort example level sentence system importance factor impact service time recommendation type process element aspect guidelines child perception definition scale sample problem group average barrier test aim area theory theories expectation impact intervention problem study author model step framework bloom likelihood observe inclusion basic benchmark project research adjustment demonstrate reinforcer symptom researcher potential connection inventory opinion use role history vary way find likely appear monitoring save datum editor criteria strong experience paper technique experiment effect frequency objective survey need imitation text definition sample scale probability observation advantage background test evidence attitude regain review power goal law color user cue stage condition perceive highest diagram significant similarity following difference majority effectiveness between about , -LRB- -RRB- -lrb- -rrb- \''.split())
model = models.Word2Vec.load('/media/aabhaschauhan/Data/ERIC/tmp/ednode')

def errorcheck1(b,param):
	t11 = [a2 for a2 in b.split() if not(a2 in stoplist1)] 
	try:	temp = model.wv.n_similarity(t11,['increase','decrease'])
	except Exception:	return [True,0]
	if temp < param:	return [True,0]
	else:	return [False,temp]

def errorcheck2(a,c,param):
	if (a in stoplist or c in stoplist):	return [True,0]
	a1 = [at for at in a.split() if not(at in stoplist1) and len(a.split())<5]
	a2 = [at for at in c.split() if not(at in stoplist1) and len(c.split())<5]	 
	try:	temp = model.wv.n_similarity(a1,a2)
	except Exception:	return [True,0]
	if temp < param:	return [True,0]
	else:	return [False,temp]

def sortit(pool,p1,p2):
	a1,a2,a3=[],[],[]
	for [(a,c),b] in pool:
		if b>=p1: a1 += [[(a,c),b]]
		elif p1>b>=p2:	a2 += [[(a,c),b]]
		else:	a3 += [[(a,c),b]]
	return a1,a2,a3

def getkey1(abc):
	[(a,c),b] = abc	
	return b

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

#------------------------------------------------------------------------------------

conn = psycopg2.connect("dbname=edu_learning user=aabhaschauhan password=eval2017!")
cur = conn.cursor()
cur.execute("SELECT p1_name, feature, p2_name, p1_le, ft_le, p2_le FROM node_edge2")
row = cur.fetchone()
#------------------------------------------------------------------------------------

def common(w1,w2,f1):
	f2 = [ww for (ww,www) in f1]
	if not(w1 in f2): f2 += [w1] 	 
	com1 = [a for (a,b) in d1[w1] if not(a in f2)]
	com2 = [a for (a,b) in d1[w2]]
	temp = list(set(com1).intersection(com2))
	if len(temp)>0:	
		temp1=[]
		for a in temp:
			temp1 += [f2+[a,w2]]
		return True,temp1
	else: return False,0

def words(j,w,p2,f1):
	if j == 1: 
		if w==p2:	return False,0
		else:	return common(w,p2,f1)	
	flag = 0	
	for i,(a,b) in enumerate(f1):
		if b==j:	
			flag = 1			
			f1 = f1[:i] + [(w,j)]
			break
	if flag==0: f1 += [(w,j)]
	f2 = [a for (a,b) in f1]
	if len(d1[w])>0:
		temp = []
		for (w1,r) in d1[w]:
			if w1 in f2: continue
			a1,a2 = words(j-1,w1,p2,f1)
			if a1:	temp += a2
		return True,temp
	else: return False,0
'''	
print "TOTAL NUMBER OF ROWS: ", cur.rowcount


d2,d3,links = dict(),dict(),[]
while row is not None:
	(a3,b3,c3,a,b,c) = row
	[va1,val1] = errorcheck1(b,0.04)
	[va2,val2] = errorcheck2(a,c,0.15)
	if va1 or va2:
		row = cur.fetchone()
		continue
	if not((a,c) in d3 or (c,a) in d3):
		d3[(a,c)] = 0
		if a in d2: d2[a] += [(c,b)]
		else:	d2[a] = [(c,b)]
		if c in d2: d2[c] += [(a,b)]
		else:	d2[c] = [(a,b)]
	else:
		row = cur.fetchone()
		continue
	row = cur.fetchone()
np.save("/media/aabhaschauhan/Data/ERIC/tmp/analysis1.npy",d2)'''
d1 = np.load("/media/aabhaschauhan/Data/ERIC/tmp/analysis1.npy").item()
p1,p2,dd = 'student','teacher',2
compil = []
for i in range(dd):
	cc,temp = words(i+1,p1,p2,[(p1,i+1)])	
	for abc in temp:
		compil += [[i+1,abc]]
		print i+1, abc
 	print i+1, len(temp)

#df = pd.DataFrame(data=compil,columns=['no. of intermediate nodes','path'])
#df.to_csv('/media/aabhaschauhan/Data/ERIC/Results/analysis1.csv')
nodes,links=[{"id":p1,"group":2},{"id":p2,"group":2}],[]
for abc1,abc2 in compil:
	d2,d3,d4=dict(),dict(),dict()
	d2["id"]=abc2[1]
	d2["group"]=1
	d3["source"],d3["target"],d3["value"]=p1,abc2[1],1	
	d4["source"],d4["target"],d4["value"]=abc2[1],p2,1
	nodes += [d2]
	links += [d3] + [d4]	
d5 = dict()
d5["nodes"]=nodes
d5["links"]=links
filename = '/home/aabhaschauhan/Ednode_Front/analysis1.json'
with open(filename, 'w') as outfile:
	json.dump(d5, outfile)

	
