from gensim.models import Word2Vec as ww
import pandas as pd
import numpy as np
import psycopg2 as psy
from fuzzywuzzy import fuzz,process
import time

print("\nDESCRIPTION: 'triplet_mapping.py' will create a mapped node or relation for each of the (subject, relation, object) of a triplet.\n\n\n")

aft = input("Which corpus to use?\n1-- ONLY article abstracts (DEFAULT)\n2-- Article abstracts and full text of articles(for all articles possible)\n\n")
while (aft !=1 and aft!=2):
	aft = input("\nEnter a valid response (1/2):	")
if aft==1: name,name1 = "node_edge","ednode1"
else:	name,name1 = "node_edge1","ednode1"

mm = ww.load('/media/aabhaschauhan/Data/ERIC/tmp/'+name1)
mainlist = [abc for abc in mm.wv.vocab]
stoplist = list(set('% = , -LRB- -RRB- -lrb- -rrb- \''.split())) 
d2 = np.load('/media/aabhaschauhan/Data/ERIC/Results/synonym_dict_aka_idea(with parent_synonym)_AC_V2.6.npy').item()
d3 = np.load('/media/aabhaschauhan/Data/ERIC/Results/rel_map.npy').item()
d4 = [abc for abc in d2 if len(abc.split('_'))>1]
d5 = dict()

def key1(abc):
	[a,b] = abc
	return b
def simi(a,c):
	temp1=[]
	for c1 in c:
		temp = [abc for abc in c1.split('_') if abc in mainlist]
		if len(temp) == 0:	temp1+=[[c1,-100]]
		else:	temp1 += [[c1,mm.wv.n_similarity(a,temp)]]		
	ab = sorted(temp1, key = key1, reverse=True)	
	return ab[0]
def check_dict_multi(d,t):
	temp = t.split()
	for i in range(2,7):	#maximum number of words in a dictionary entry = 6
		for j in range(len(temp)-i+1):
			temp1 = "_".join(temp[j:j+i])
			if temp1 in d:	temp = temp[:j] + [temp1] + temp[j+i:]
	return " ".join(temp)
def create_sim_tuples(d,a,a1):
	t=[]
	for abc in a:
		if (abc in d):
			temp1 = simi(a1,d[abc])
			if temp1[1] >= 0:	t += [temp1]
	return t
	
conn = psy.connect("dbname=edu_learning user=aabhaschauhan password=eval2017!")
cur = conn.cursor()
cur.execute("SELECT p1_id,p1_name, feature, p2_name, p1_l, f_l, p2_l, con_value, keywords FROM "+name)# UNION ALL SELECT doc_id, sentence_index, lemmas FROM sentences1")
row = cur.fetchone()
bigie,i,total,j,ddd = [],0,cur.rowcount,0,dict()
t1 = time.time()
while row is not None:
	j += 1
	if j%1000 == 0:	
		print "TRIPLET No.:	", j
		print time.time()- t1
		t1= time.time()
	(p1,a2,b2,c2,a,b,c,value,keywords) = row
	key = '_'.join(p1.split('_')[0:2])
	#if i>500: break
	if j % int(total/5) == 0: print str((j*100)/float(total)) + "% COMPLETE"
	if key in ddd:
		if key == bigie[len(bigie)-1][0]:	del bigie[len(bigie)-1]
		row = cur.fetchone()
		continue
	else:
		ddd[key] = 1
	#print "Starting Step 1: joining multiple words with _ --   ", time.time()-t1
	temp = check_dict_multi(d4,a + " ..... " + c)
	[aa,cc] = temp.split(" ..... ")
	#t1 = time.time()
	a1,b1,c1 = [abc for abc in aa.split() if not(abc in stoplist)],b.split(),[abc for abc in cc.split() if not(abc in stoplist)]
	a11,c11 = [abc for abc in ' '.join(a1).replace('_',' ').split() if abc in mainlist], [abc for abc in ' '.join(c1).replace('_',' ').split() if abc in mainlist]
	if min(len(a11),len(a1),len(c11),len(c1))==0:
		row = cur.fetchone()
		continue
	#print "Step 2: Similarity Values --  ", time.time()-t1
	tt1,tt2,tt3 = create_sim_tuples(d2,a1,a11),[],create_sim_tuples(d2,c1,c11)
	for abc in b1:	
		if abc in d3:	tt2 += d3[abc]
	if min(len(tt1),len(tt2),len(tt3)) == 0:
		row = cur.fetchone()			
		continue
	#t1 = time.time()
	tt1a,tt2a,tt3a = sorted(tt1,reverse=True,key = key1)[:min(3,len(tt1))],tt2,sorted(tt3,reverse=True,key = key1)[:min(3,len(tt3))]
	tttt1 = mm.wv.n_similarity(a11,c11)	#inter- node similarity
	tttt2 = fuzz.token_set_ratio(' '.join(a11),' '.join(c11))	#fuzzy match b/w nodes
	#print "Step 3: Inter-node Similarity Values --  ", time.time()-t1
	#t1 = time.time()
	value1 = 0
	#print "Step 4: Keyword Matching --  ", time.time()-t1
	try: 
		if any([True for abc in keywords if abc in a2 + " " + a]):	value1 += 0.5	# keyword match
		if any([True for abc in keywords if abc in c2 + " " + c]):	value1 += 0.5 
	except Exception: pass
	#t1 = time.time()
	#print "Step 5: Frequency --  ", time.time()-t1
	(a1,b1) = tt1a[0]
	(a3,b3) = tt3a[0]
	if not((a1,a3) in d5) and not((a3,a1) in d5):		#frequency of tuple check
		d5[(a1,a3)] = 1
	else:	
		try:	d5[(a1,a3)] += 1
		except Exception:	d5[(a3,a1)] += 1
	#t1 = time.time()
	bigie += [[key,a,b,c,(a2,b2,c2),tt1a,tt2a,tt3a,(value,value1),tttt1,tttt2]]
	i += 1
	row = cur.fetchone()

for k,abc in enumerate(bigie):
	(t11,t12) = abc[5][0]
	(t21,t22) = abc[7][0]
	try:	temp0 = d5[(t11,t21)]
	except Exception:	temp0 = d5[(t21,t11)]
	bigie[k] = abc + [temp0]
print i,j
df1 = pd.DataFrame(bigie,columns=['key','a','b','c','triplet','mapped word A','relation_bucket','mapped word B','confidence_value','incs','inf', 'frequency'])
df1.to_csv('/media/aabhaschauhan/Data/ERIC/mapping_'+name+'_V2.0_AC.csv')
print "File saved as: '/media/aabhaschauhan/Data/ERIC/mapping_"+name+"_V2.0_AC.csv'"


'''
study program approach strategy analysis method course suggestion concept idea view example level sentence importance factor impact service time recommendation type process element aspect guidelines perception paper definition scale skill help sample group average aim document area change expectation problem model step framework likelihood observe % = inclusion basic introduction category purpose train benchmark project adjustment percent demonstrate reinforcer symptom potential connection comparison opinion use role history vary way find likely appear monitoring save datum editor criteria strong experience experiment frequency objective work survey result need text definition sample scale observation advantage background evidence regain law user cue stage condition perceive highest diagram significant similarity following difference majority effectiveness effective between about
'''
