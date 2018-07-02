from gensim.models import Word2Vec as ww
import pandas as pd
import numpy as np
import psycopg2 as psy
from fuzzywuzzy import fuzz, process
from collections import Counter
import math

stoplist = list(set('article author study program approach strategy analysis method course suggestion concept idea student teacher child school view people effort example level sentence system importance factor impact service time recommendation type process element aspect guidelines perception definition scale sample problem group average barrier test aim area theory theories expectation impact intervention problem study author model step framework bloom likelihood observe inclusion basic benchmark project research adjustment demonstrate reinforcer symptom researcher potential connection inventory opinion use role history vary way find likely appear monitoring save datum editor criteria strong experience paper technique experiment effect frequency objective whether survey need imitation text definition sample scale probability observation advantage background test evidence attitude regain review power goal law color user cue stage condition perceive highest diagram significant similarity following difference majority effectiveness between about , -LRB- -RRB- -lrb- -rrb- \' \'\' `` - `'.split()))
stoplist1 = list(set('for a of the and to in where which while these there i I who also am ; were here if was be because try some by do when not seem may being then that : this as at what how it must can we is with on you or there they more are their been an from has have than between about -lrb- -rrb- will them'.split()))
stoplist2 = ['0','/','1','2','3','4','5','6','7','8','9','one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ninth', 'ten', 'eleven', 'twelve', 'twelfth', 'first', 'second', 'third','%','&','$','+',',','=','.',"'",'--','sb','rb','\\']
mm= ww.load('/media/aabhaschauhan/Data/ERIC/tmp/ednode2')
pp1 = pd.read_csv('/media/aabhaschauhan/Data/ERIC/Results/top_relation_words_AC_V1.1.csv')

conn = psy.connect("dbname=edu_learning user=aabhaschauhan password=eval2017!")
cur = conn.cursor()
cur.execute("SELECT DISTINCT(ft_le) FROM node_edge3")
row = cur.fetchone()
d1 = dict()#{'improve':1,'increase':2,'decrease':3,'
bigie,i,j = [],0,0
while row is not None:
	i+=1
	(b,)=row
	b1 = [abc.lower() for abc in b.split() if (not(abc.lower() in stoplist+stoplist1) and not(any([True for aac in stoplist2 if str(aac) in abc])))]
	if len(b1) == 0:
		j+=1
		row = cur.fetchone()
		continue
	bigie += b1
	row = cur.fetchone()

dd=Counter(bigie)
dd1 = sorted(dd.iteritems(), reverse = True, key = lambda (k,v):(v,k))
dd3=dict()
for i in range(len(pp1)):
	if pp1['sim_wo'][i]!='Done':
		try:
			t1 = math.isnan(pp1['sim_wo'][i])
			temp = [i]
		except Exception:
			temp = [int(a) for a in pp1['sim_wo'][i].split(', ')]+[i]
		dd3[len(dd3)] = temp


for i in dd3.keys():
	temp = []
	for j in dd3[i]:	temp += [pp1['word'][j]]
	dd3[i] = temp


dd2 = [i for (i,abc) in dd1 if 500>abc>80]
for i in dd2:
	for j in dd3.keys():
		if any([True for a in dd3[j] if mm.wv.n_similarity(i.split(),a.split())>0.45]):
			dd3[j]+=[i]
			break

abc = []
for j in dd3.values():	abc = abc + j


pd.DataFrame(abc,columns=['words']).to_csv('/media/aabhaschauhan/Data/ERIC/Results/all_top_relations.csv')
np.save('/media/aabhaschauhan/Data/ERIC/Results/rel_map.npy',dd3)
pd.DataFrame(sorted(dd3.iteritems()),columns=['index','list']).to_csv('/media/aabhaschauhan/Data/ERIC/Results/clubbed_relations.csv')
'''
	j+=1
	(b,) = row
	flag = 0
	if len(d1)>500: break
	b1 = [abc for abc in b.split() if not(abc in stoplist+stoplist1)]
	if len(b1) == 0:
		row = cur.fetchone()
		continue
	temp1 = '_'.join(b1)
	mapped_word = temp1
	for abc in d1.keys():	#Fuzzy Check
		if fuzz.token_set_ratio(abc,temp1) > 70:
			mapped_word = abc
			flag = 1			
			break
	if flag == 0 and not(temp1 in d1):	d1[temp1]= len(d1)+1 	#checking uniqueness
	bigie += [[b,mapped_word]]

	row=cur.fetchone()
print pd.DataFrame(bigie,columns=['relation','mapping'])
print j
'''
