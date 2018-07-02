import json_lines
from gensim import corpora, models, similarities
import pandas as pd
from six import iteritems
import logging
import time
import psycopg2
import numpy as np
import time

#LabeledSentence = models.doc2vec.LabeledSentence

print("\nDESCRIPTION: 'word2vec.py' will create a Word2Vec model with word vectors of all words present in the corpus.\n\n\n")

aft = input("Which corpus to use?\n1-- ONLY article abstracts\n2-- Article abstracts and full text of articles(for all articles possible) (DEFAULT)\n\n")
while (aft !=1 and aft!=2):
	aft = input("\nEnter valid response (1/2):	")

hyper = raw_input("\n\nWhich hyper parameter(s) do you want to change?\n1-- Minimum count of word occurrences (default = 4)\n2-- Dimensionality of feature vector (default = 400)\n3--Minimum distance between the current and predicted word in a sentence (default = 6)\n4-- Number of worker threads to train the model (default = 4)\n5-- Use skip-gram/CBOW model? (0/1) (default = 0)\n0-- Use default values\n\nResponse (Add multiple by separating them with a comma without spaces):	")

hyper = hyper.split(',')
l1 = len(hyper)
min_freq,dimen,wind,work,sg1=4,400,6,4,0
if not('0' in hyper):
	for i in range(l1):
		if (hyper[i]=='1'):	min_freq = input("\n"+str(i+1)+") Minimum count of word occurrences (default = 4)?:		")
		elif (hyper[i]=='2'):	dimen = input("\n"+str(i+1)+") Dimensionality of feature vector (default = 400)?:		")
		elif (hyper[i]=='3'):	wind = input("\n"+str(i+1)+") Minimum distance between the current and predicted word in a sentence (default = 6)?:		")
		elif (hyper[i]=='4'):	work = input("\n"+str(i+1)+") Number of worker threads to train the model on(default = 4)?:		")
		elif (hyper[i]=='5'):	sg1 = input("\n"+str(i+1)+") Use skip-gram/CBOW model? (0/1) (default = 0)?:		")

if aft==1:	name,name1 = "sentences","ednode"
else:	name,name1="sentences1","ednode1"

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MyCorpus(object):
	def __iter__(self):
		conn = psycopg2.connect("dbname=edu_learning user=aabhaschauhan password=eval2017!")
		cur = conn.cursor()
		cur.execute("SELECT pos_tags, lemmas FROM "+name)# UNION ALL SELECT doc_id, sentence_index, lemmas FROM sentences1")
		row = cur.fetchone()
		stoplist = set('for a of the and to in where there i I ; who also am were here if was be being then that this as at what how it can we is with on you or there appear , \' they likely took take not more are their `` been become make made an from has have than between % about -lrb- -rrb- will them vary find must will them sb rb'.split())
		strictlist = ['0','/','1','2','3','4','5','6','7','8','9','%','&','$','+',',','=','.',"'",'--','\\']
		pos_list = ['NN','NNS','RB','RBR','VB','VBD','VBG','VBN','VBP','VBZ','JJ','JJR','JJS']
		while row is not None:
			(b,d,) = row
			temp = [d[at].lower() for at in range(len(b)) if not(d[at].lower() in stoplist) and (b[at] in pos_list)]
			t1 = []				
			for abc in temp:
				if any([True for abc1 in strictlist if (abc1 in abc)]):	continue
				else:	t1 += [abc]
			yield t1
			row = cur.fetchone()

corpus_memory_friendly = MyCorpus()
print(corpus_memory_friendly)  # load one vector into memory at a time
model = models.Word2Vec(corpus_memory_friendly, min_count = min_freq, size = dimen,workers = work, window = wind, sg = sg1, hs = 1, negative = 8) #Train the 
model.save('/media/aabhaschauhan/Data/ERIC/tmp/'+name1)

#model = models.Word2Vec.load('tmp/ednode')
#print model.doesnt_match("increase decrease enhance promote stimulate".split())
#print model.similarity('increase','decrease')
'''
		with open('/media/aabhaschauhan/Data/Edu/input/eric/articles1.jsonl', 'rb') as f:
			for item in json_lines.reader(f):
				if item['content'] != '':	
					try:	temp = coreout(str(item['content']))
					except Exception:	continue
					try:	i = len(temp['sentences'])
					except Exception:	continue
					for k in range(i):
						pp=[]
						j = len(temp['sentences'][k]['tokens'])
						if j < 5:	continue
						else:
							for k1 in range(j):
								z1 = str(temp['sentences'][k]['tokens'][k1]['lemma']).lower()
								if not(z1 in stoplist):	pp += [z1]
							yield pp
'''
