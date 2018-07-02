from nltk.corpus import wordnet
from gensim.models import Word2Vec as ww
from pycorenlp import StanfordCoreNLP
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz, process

stoplist = list(set('for a of the and to in where there i I ; who also am were here if was be being then that this as at what how it can we is with on you or save demonstrate observe regain there appear , \' they likely took take not more are their `` been become make made an from has have than between % about -lrb- -rrb- will them vary find must will them'.split()))
strictlist = ['0','/','1','2','3','4','5','6','7','8','9','one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ninth', 'ten', 'eleven', 'twelve', 'twelfth', 'first', 'second', 'third','%','&','$','+',',','=','.',"'",'--','sb','rb','\\'] + list(set('article author percent number review study model theor participant finding section objective sampl statement research'.split()))
relation = list(set(pd.read_csv('/media/aabhaschauhan/Data/ERIC/Results/all_top_relations.csv')['word']))

print("\nDESCRIPTION: 'seed_tree.py' will create a list of possible nodes of the network and a corresponding synonym dictionary which will be used to map the triplets produced using 'triplet_extraction.py'.\n\n")
cutoff = input("Enter Node Cosine Similarity Cutoff for the first layer (DEFAULT = 0.47)\n\nRESPONSE:	")
if (cutoff<0 or cutoff>1):	cutoff = input("Enter valid value between 0 and 1: ")
fuzzycutoff = input("Enter Fuzzy Cutoff for first layer (DEFAULT = 90)\n\nRESPONSE:	")
if (fuzzycutoff<0 or fuzzycutoff>100):	fuzzycutoff = input("Enter valid value between 0 and 100: ")
mm = ww.load('/media/aabhaschauhan/Data/ERIC/tmp/ednode1')
mainlist = [abc for abc in mm.wv.vocab]

d2 = np.load('/media/aabhaschauhan/Data/ERIC/Results/node_dict.npy').item()
seed = list(set(d2.values()))
d1,total,j = dict(),len(seed),1
#mm2 = ww.load('/media/aabhaschauhan/Data/ERIC/tmp/ednode1')
#seed = list(set(pd.read_csv('/media/aabhaschauhan/Data/ERIC/Results/node_seed_list.csv')['nodes']))

def key1(word):
	(a,b) = word
	return b

def map_syn(dd,seed1):
	t,seed1 = [],list(set(seed1))
	for abc in seed1:
		if abc in dd:
			if dd[abc]!=abc:
				for i in range(len(dd.values())):
					if dd[dd.keys()[i]]==abc:
						dd[dd.keys()[i]] = dd[abc]
				if dd[abc] in seed1:	t += [abc]
				else:	seed1[seed1.index(abc)] = dd[abc]
				
	for a in list(set(t)):	del seed1[seed1.index(a)]	
	return dd,seed1
	
def rem_syn(dd1,dd2,seed1):
	seed1 = map_syn(dd2,seed1)
	i,l1 = 0,1
	while (i<l1):
		if not(dd1.keys()[i] in dd2.keys()):	dd1.values()[i] = map_syn(dd2,dd1.values()[i])
		else:
			word = dd2[dd1.keys()[i]]
			dd1[word] = list(set(dd1[word] + dd1.values()[i]))
			dd1[word] = map_syn(dd2,dd1[word])
			del dd1[dd1.keys()[i]]
			i -= 1
		i += 1
		l1 = len(dd1.keys())
	return seed1,dd1

def change_or_not(dd,word,tt,t1):
	if t1 == 0:	t1 = mm.wv.n_similarity(tt.split('_'),word.split('_'))
	if not(tt in dd) and t1>=0.30:	dd[tt] = word
	elif tt in dd:
		if mm.wv.n_similarity(tt.split('_'),dd[tt].split('_')) < t1:	dd[tt] = word
	return dd

for i,word in enumerate(seed):
	if i==total:
		j += 1
		cutoff += 0.05
		total = len(seed)
	if j>2:	break	
	if i%500==0: print len(seed)
	d1[word] = []
	for abc in wordnet.synsets(word,pos='n'):
		for l in abc.lemmas():
			if l.name() != word and not(l.name() in seed) and not(l.name() in d2):	d2[l.name()] = word
	temp = [abc for abc in word.split('_') if not(abc in stoplist) and (abc in mainlist)]
	if len(temp)==len(word.split('_')):	mm1 = mm.wv.most_similar(temp)
	else:	continue
	for (t1,t2) in mm1:
		temp1,temp2,t3,t4 = False,False,t1.replace('-','_'),t1.replace('-','')
		try:	
			temp1 = wordnet.synsets(t3)[0].wup_similarity(wordnet.synsets(word)[0])>0.70
			temp2 = wordnet.synsets(t4)[0].wup_similarity(wordnet.synsets(word)[0])>0.70	
		except Exception: pass
		if t2>=cutoff and not(t1 in relation) and not(any([True for abc in strictlist if str(abc) in t1])): #and nouncheck(t3)
			level = 0
			for word1 in seed:
				if (fuzz.token_set_ratio(' '.join(word1.split('_')),t1)>=fuzzycutoff):
					if len(t1)<len(word1):	d2 = change_or_not(d2,t1,word1,0)
					else:	d2 = change_or_not(d2,word1,t1,0)	
					level = 1					
			if level == 1:	continue
			if temp1:
				d2 = change_or_not(d2,word,t3,0.75)
				continue
			if temp2:
				d2 = change_or_not(d2,word,t4,0.75)
				continue			
			if t3 in seed and t1!=t3:
				d2 = change_or_not(d2,t3,t1,0)
				continue
			if t4 in seed and t1!=t4:
				d2 = change_or_not(d2,t4,t1,0)
				continue
			if not(t1 in seed) and t2>=cutoff+0.05:	seed += [t1]

d2, seed = map_syn(d2,seed)
#seed,d1 = rem_syn(d1,d2,seed)
for abc1 in seed:	d2[abc1] = abc1

print "\n\n\n\n"
print len(seed)
print "\n\n\n\n",len(d2)
np.save('/media/aabhaschauhan/Data/ERIC/Results/parent_child.npy',d1)
np.save('/media/aabhaschauhan/Data/ERIC/Results/parent_synonyms.npy',d2)
df1 = pd.DataFrame(seed,columns=['nodes'])
df1.to_csv('/media/aabhaschauhan/Data/ERIC/Results/node_list.csv',encoding='utf-8')
print "File saved as: '/media/aabhaschauhan/Data/ERIC/Results/node_list.csv'"
