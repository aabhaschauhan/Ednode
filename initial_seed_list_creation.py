import numpy as np
import pandas as pd
from gensim.models import Word2Vec as ww
from fuzzywuzzy import fuzz, process

print("\nDESCRIPTION: 'initial_seed_list_creation.py' will create a dictionary of seed words that will be used to create the seed tree in the next step.\n\n")
filename = raw_input("Enter Input File Address\n\n<0>-- DEFAULT: 'Final_word_list_V1.2.csv'\nStore it at '/media/aabhaschauhan/Data/ERIC/Results'\nHeaders: 'Lemma_Keywords' and 'Label'\nNOTE:Multi-words should be joined using underscore('_')\n\nRESPONSE:	")

if filename=='0':	filename = 'Final_word_list_V1.2.csv'
mm=ww.load('/media/aabhaschauhan/Data/ERIC/tmp/ednode1')
#nn=np.load('/media/aabhaschauhan/Data/ERIC/Results/node_matrix.npy')
mainlist = [abc for abc in mm.wv.vocab]
keyword = list(pd.read_csv('/media/aabhaschauhan/Data/ERIC/Results/'+filename)["Lemma_Keywords"])
label = list(pd.read_csv('/media/aabhaschauhan/Data/ERIC/Results/'+filename)["Label"])
keyword=[keyword[i] for i in range(len(label)) if label[i]=='1']

#All words that do not entirely exist in the Word2Vec vocabulary are filtered out

t=[]
for i,abc in enumerate(keyword):
	k1 = [abc1 for abc1 in abc.split('_') if (abc1 in mainlist)]
	if len(k1) != len(abc.split('_')):	t += [[i,abc]]

for i in t:
	zz = keyword.index(i[1])	
	del keyword[zz]
	del label[zz]
#---------------------------------------------------------------------------------

#Creating a similarity matrix for all keywords
nn = np.zeros([len(keyword),len(keyword)])
for i in range(len(keyword)-1):
	k1 = keyword[i].split('_')
	for j in range(i+1,len(keyword)):
		k2 = keyword[j].split('_')
		nn[i,j]=mm.wv.n_similarity(k1,k2)
		nn[j,i]=nn[i,j]

np.save('/media/aabhaschauhan/Data/ERIC/Results/node_matrix.npy',nn)
print "The node matrix of initial seed list is saved as: '/media/aabhaschauhan/Data/ERIC/Results/node_matrix.npy'"
#-----------------------------------------------------------------------------------
d1 = dict()
for word in keyword:	d1[word]=word
pd.DataFrame(keyword,columns=["Node"]).to_csv('/media/aabhaschauhan/Data/ERIC/Results/initial_seed_list.csv',encoding='utf-8')
np.save('/media/aabhaschauhan/Data/ERIC/Results/node_dict.npy',d1)
print "The dictonary of initial seed list is saved as: '/media/aabhaschauhan/Data/ERIC/Results/node_dict.npy'\n"
print "The initial seed list is saved as: '/media/aabhaschauhan/Data/ERIC/Results/initial_seed_list.csv'\n"

#--------------------------------------------------------------------------------------------------

'''
def change_or_not(dd,word,tt,t1):
	if t1 == 0:	
		try:	t1 = mm.wv.n_similarity(tt.split('_'),word.split('_'))
		except Exception:	return dd
	if not(tt in dd) and t1>=0.30:	dd[tt] = word
	elif (tt in dd):
		if mm.wv.n_similarity(tt.split('_'),dd[tt].split('_')) < t1:	dd[tt] = word
	return dd

#collapsing the initial seed list

d1 = dict()
for j,word in enumerate(keyword):
	d1[word] = word
	for i,abc in enumerate(nn[j,:]):
		temp = fuzz.token_set_ratio(" ".join(word.split('_'))," ".join(keyword[i].split('_')))
		if temp>90 and i!=j and not(keyword[i] in keykey):	
			d1 = change_or_not(d1,word,keyword[i],0)
		elif ((temp<60 and abc>0.75) or (60<=temp<=90 and abc>0.80)) and not(keyword[i] in keykey) and len(word.split('_'))<2:
			if keyword[i] in d1:	
				if (nn[i,keyword.index(d1[keyword[i]])] < nn[i,keyword.index(word)]):
					d1 = change_or_not(d1,word,keyword[i],0)
			else:	
				d1[keyword[i]] = word
#------------------------------------------------------------------------------------------------------------------------------------------

#If A is mapped to B, all words mapped to A are automatically mapped to B
for word in keykey:
	if word in d1.keys():
		if d1[word]!=word:
			for k in range(len(d1.keys())):
				if d1.values()[k] == word:	d1[d1.keys()[k]] = d1[word]
#--------------------------------------------------------------------------------------------------------------------------------------------
'''

'''
k2 = [(i,word) for (i,word) in k1 if len(word.split('_'))<=1] 
k3 = [(i,word) for (i,word) in k1 if len(word.split('_'))>=2] 
for (j,word) in k2:
	for (i,word1) in enumerate(keyword):
		temp = fuzz.token_set_ratio(word,word1)
		if temp > 90 and word!=word1 and not(word1 in d1.values()):	d1[word1] = word
'''
