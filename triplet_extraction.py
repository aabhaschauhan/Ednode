#!/usr/bin/env python
from deepdive import *
import pandas
from fuzzywuzzy import fuzz, process

def combine_similar_relations(f1): 
	f2,indices=[],[]
	for i,temp1 in enumerate(f1):
		if not(i in indices) and temp1 != None:
			for j in xrange(i+1,len(f1)):
				if f1[j] != None:
					flag = 0
					(x11,r111,r112,y11,e11,e12,x12,r121,r122,y12) = temp1
					(x21,r211,r212,y21,e21,e22,x22,r221,r222,y22) = f1[j]
					b1, e1 = [x11,r111,r112,y11], [x12,r121,r122,y12]
					b2, e2 = [x21,r211,r212,y21], [x22,r221,r222,y22]
					r1, r2 = [e11,e12], [e21,e22]
					h1, h2 = list(set(r1))+[e1[0]], list(set(r2))+[e2[0]]
					if (b1==b2 and r1==r2) and (e1[0]==e2[0]):
						flag = 1
						if e2[3]>e1[3]:	temp1 = (b1[0],b1[1],b1[2],b1[3],r2[0],r2[1],e2[0],e2[1],e2[2],e2[3])
						else:	temp1 = (b1[0],b1[1],b1[2],b1[3],r2[0],r2[1],e1[0],e1[1],e1[2],e1[3])
					elif (b1==b2 and r1!=r2 and (h1 == list(set(xrange(r2[0],r2[1]+1)).intersection(h1)))):
						flag = 1
						temp1 = (b1[0],b1[1],b1[2],b1[3],r2[0],r2[1],e2[0],e2[1],e2[2],e2[3])
					elif (b1==b2 and r1!=r2 and (h2 == list(set(xrange(r1[0],r1[1]+1)).intersection(h2)))):
						flag = 1
						temp1 = (b1[0],b1[1],b1[2],b1[3],r1[0],r1[1],e1[0],e1[1],e1[2],e1[3])
					if flag == 1:
						indices += [j]
			f2 += [temp1]
	return f2

def potential_nodes(pos_tags):
	num_tokens = len(pos_tags)
	i=0
	flag = -1
	flag1 = 0
	nodes = []
	nouns, adjectives = ["NN","NNS"], ["JJ","JJR", "JJS"]
	while i < num_tokens:
		if (pos_tags[i] in nouns):
			if flag == -1:
				begin_index = i
				flag = 0
				flag1 = 1
			elif flag1 == 1 and flag == 1:
				flag = 0
			if i == num_tokens - 1:
				end_index = i
				flag = -1		
		elif (pos_tags[i] in adjectives) and i < num_tokens - 1 and (flag in [0,1] or flag1 == 0):
			if (pos_tags[i+1] in nouns) and flag == -1:
				begin_index = i
				flag = 1
				flag1 = 1
			elif i< num_tokens - 2:
				if ((pos_tags[i+1] in adjectives) and (pos_tags[i+2] in nouns)) and flag == -1:
					begin_index = i
					flag = 1
					flag1 = 1
		elif flag == 0:
			end_index = i-1
			flag = -1
		if flag == -1 and flag1 == 1:
			nodes += [(begin_index,0,0,end_index,0,5)] #(starting index, middle1,middle2, ending index, 0-no middle word/ 1 - middle word exists,5-default)
			flag1 = 0
		i += 1
	return nodes


def nodechecks(node,deptype,deptoken,pos,token): 	#add prepositions and identify 'and' b/w two nodes
	subord_conj = ["after","once","until","although","provided that","when","as","rather than","whenever","because","since","where","before","so that","whereas", "even if","than","wherever","even though","that","whether","if","though","while","in order that","unless","why","such"] #subordinating conjunctions to be excluded from POS "IN"
	stop_dt= ["these","this","such"]
	for i in xrange(len(node)-1):	
		flag = 0
#		with open("/media/aabhaschauhan/Data/Edu/tmpp1.txt",'a') as f:
#			f.write("length: " + str(len(node)) + "              --" + str(i) + " " + str(node[i]) + "\n" + str(i+1) + " " + str(node[i+1]) + "\n")
		(x1,r11,r12,y1,h1,t1) = node[i]
		(x2,r21,r22,y2,h2,t2) = node[i+1]
		for j in xrange(x2,y2+1):
			if not('between' in token[:j+1]) and (deptype[j] == 'conj:and' and x1+1 <= deptoken[j] <= y1+1) or (x2 - y1 == 2 and token[y1+1].lower() == 'and' and pos[x2] in ["JJ","JJR", "JJS","NN","NNS"]):
				flag, node[i],node[i+1] = 1,(x1,r11,r12,y1,h1,1),(x2,r21,r22,y2,h2,-1)
				break
		if flag == 0:	node[i],node[i+1] = (x1,r11,r12,y1,h1,0),(x2,r21,r22,y2,h2,0)		 
	i = 0
	while (i<len(node)-1):
		(x1,r11,r12,y1,h1,t1) = node[i]
		(x2,r21,r22,y2,h2,t2) = node[i+1]
		if (x2-y1 == 2 and pos[y1+1] == 'IN' and not(token[y1+1] in subord_conj)) or (x2-y1 == 3 and pos[y1+1] == 'IN' and not(token[y1+1] in subord_conj) and pos[y1+2] == 'DT' and not(token[y1+2] in stop_dt)):
			if h1 == 1:	node = 	node[:i] + [(x1,r11,r12,y2,1,t2)] + node[i+2:]
			else:	node = node[:i] + [(x1,0,0,y2,0,t2)] + node[i+2:]
			if t2 == 1:	
				(s1,r31,r32,s2,h3,t3) = node[i+1]
				if h3 == 0 and h1==0:	node[i+1] = (x1,y1+1,s1,s2,1,-1)
			if t1 == -1:
				(s1,r31,r32,s2,h3,t3) = node[i-1]
				if h3 == 0 and h2==0:	node[i-1] = (s1,s2,x2-1,y2,1,1)
		i += 1
	return node


def joining(abc,structure):
	(x1,r11,r12,y1,h1,t1) = abc
	if h1 == 0: return " ".join(structure[x1:y1+1])
	else:	return " ".join(structure[x1:r11+1]+structure[r12:y1+1])


def ranges(abc):
	(x1,r11,r12,y1,h1,t1) = abc
	if h1 == 0:	return xrange(x1,y1+1)
	else:	return list(xrange(x1,r11+1))+list(xrange(r12,y1+1))

		
def ranges1(abc):
	(x1,r11,r12,y1) = abc
	if r11 == 0 and r12 == 0:	return xrange(x1,y1+1)
	else:	return list(xrange(x1,r11+1))+list(xrange(r12,y1+1))


def negate(deptype,deptoken,i): # To check for negations and adjectives in edge labels
	flag1, flag2 = 0,0
	for j in range(i):
		if deptype[j] == 'neg' and deptoken[j] == i+1 and flag1 == 0:
			flag1 = j
		if deptype[j] == 'amod' and deptoken[j] == i+1 and flag2 == 0:
			flag2 = j
		if flag1!=0 and flag2!=0: break
	if flag1!=0 or flag2!=0:
		return min(flag1,flag2)
	else:
		return i


def relext(a1,a2,deptoken,deptype,pos,d): #To develop tuples of the form (x1,r11,r12,y1,e1,e2,x2,r21,r22,y2)
	(x1,r11,r12,y1,h1,t1) = a1
	(x2,r21,r22,y2,h2,t2) = a2
	flag1, flag15, flag2 = 0, 'aaa', 0
	for i in ranges(a1):
		if deptype[i] == 'nsubj' or deptype[i] == 'dobj':
			flag1, flag15, k1 = 1, deptype[i], i
	if flag1 == 1: 
		for i in ranges(a2):
			if deptype[i] == 'nsubj' or deptype[i] == 'dobj' and deptype[i]!=flag15:
				flag2, k2 = 1, i
				break
		if flag2 == 1:
			if k1 == k2:
				temp = deptoken[k1]-1
				e1 = negate(deptype,deptoken,temp)
				e2 = deptoken[k2]-1
				if (y1<e1<=e2<x2) and abs(e2-e1)<d and not(any([True for abc in pos[e1:e2+1] if abc in ['NN','NNS']])):#,'VBD','VBN']])): #Check 'not' and if noun exists in relation
					return (x1,r11,r12,y1,e1,e2,x2,r21,r22,y2)
			else:
				l11 = [deptoken[k1]-1,deptoken[k2]-1]
				token = [abc for abc in l11 if y1<abc<x2]
				if len(token)>0:		
					e1 = negate(deptype,deptoken,min(token))
					e2 = max(token)
					if e2-e1<d and not(any([True for abc in pos[e1:e2+1] if abc in ['NN','NNS']])):#,'VBD','VBN']])):
						return (x1,r11,r12,y1,e1,e2,x2,r21,r22,y2) 
		

def confidence(mt1,ft,mt2,token,keywords):
	temp = mt1 + " " + ft + " " + mt2
	value = fuzz.partial_ratio(temp," ".join(token).lower())/float(100)
	return value
'''
	if any([True for abc in mt1.split() if abc in keywords]):	value += 0.5
	if any([True for abc in mt2.split() if abc in keywords]):	value += 0.5 
'''	
	
def error_checking(ff,m1,m2):	#Returns true if no error
	status = True
	stoplist1 = list(set('for a of the and to in where there i I also much am were here if was be being then that this as at what how it can we is with on you or and there appear , \' they likely took take not more not are their `` been become make made an from has much have than between % about -lrb- -rrb- will them vary find must will them'.split()))
	strictlist = ['0','/','1','2','3','4','5','6','7','8','9','%','&','$','+',',','=','.',"'",'--','\\']
	# no self loops 
	if (m1 in ff) or (m2 in ff) or (ff in m1) or (ff in m2) or (m1 in m2) or (m2 in m1):	return False 
	m11 = any([True for abc in strictlist if (abc in m1)]) or (len([abc for abc in m1.split() if not(abc in stoplist1)])==0) #if node consists of any of the stopwords
	m12 = any([True for abc in strictlist if (abc in m2)]) or (len([abc for abc in m2.split() if not(abc in stoplist1)])==0)
	ff1 = any([True for abc in strictlist if (abc in ff)]) or (len([abc for abc in ff.split() if not(abc in stoplist1)])==0)
	if m11 or m12 or ff1:	return False		
	# edge label <> node label
	#if any([(abc in ff) or (ff in abc) for abc in set123]): return False
	return status
'''
	m11 = [abc for abc in m1.split() if not(abc in stoplist)]
	m12 = [abc for abc in m2.split() if not(abc in stoplist)]
	ff1 = [abc for abc in ff.split() if not(abc in stoplist)]
	if len(m11)>0 and len(m12)>0 and len(ff1)>0:
		try:	tempo1 = model.wv.n_similarity(m11,m12)		
		except Exception: return False
		try:  tempo2 = model.wv.n_similarity(ff1,['increase','decrease'])
		except Exception: return False
		if tempo1<0.1 or tempo2< 0.08:	return False
	else: return False
'''
	
# for python 3 compatibility
try:
    xrange
except NameError:
    xrange = range

@tsj_extractor
@returns(lambda
  doc_id      = "text",
  p1_id       = "text",
  r_id        = "text",
  p2_id       = "text",
  p1_name     = "text",
  feature     = "text",
  p2_name     = "text",
  p1_l        = "text",
  f_l	      = "text",
  p2_l	      = "text",
  con_value   = "float",
  keywords    = "text[]",
:[])
def extract(
	doc_id         = "text",
	sentence_index = "int",
	tokens         = "text[]",
	pos_tags       = "text[]",
	lemmas         = "text[]",
	dep_types      = "text[]",
	dep_tokens     = "int[]",
	keywords       = "text[]",
	  ):
		#factor_set = [ttt.lower() for ttt in list(pandas.read_csv("/media/aabhaschauhan/Data/ERIC/Results/updated_keywords1.3.csv")["Lemma_Keywords"])]
		#model = models.Word2Vec.load('/media/aabhaschauhan/Data/ERIC/tmp/ednode')
		keywords = [abc.lower() for abc in keywords]
		if len(tokens) > 4:
			nodes = potential_nodes(pos_tags) #identifies nodes
			nodes = nodechecks(nodes,dep_types,dep_tokens,pos_tags,tokens) #node checks for 'and' and prepositions
			d2, d1, f1 = 4, 7, []
			#Developing relationships
			for i in range(len(nodes)-1):
				(x1,r11,r12,y1,h1,t1) = nodes[i]
				q1 = joining(nodes[i],lemmas) #converts indices into lemma phrases
				for j in range(i+1,len(nodes)):		
					(x2,r21,r22,y2,h2,t2) = nodes[j]
					if (0>=x2-y1) or (x2-y1>d1):	break 	#d1 is distance between the two nodes
					q2 = joining(nodes[j],lemmas)
					if (q1 in q2) or (q2 in q1) or (x1 == x2) or (y1 == y2):	continue				
					else:	f1 += [relext(nodes[i],nodes[j],dep_tokens,dep_types,pos_tags,d2)]	#extracting relations
			f2 = combine_similar_relations(f1)
			for temp1 in f2:
				(b1,r11,r12,e1,r1,r2,b2,r21,r22,e2) = temp1
				mention_id_1 = "%s_%s_%d_%d" % (doc_id, str(sentence_index), b1, e1)
				mention_id_2 = "%s_%s_%d_%d" % (doc_id, str(sentence_index), b2, e2)
				feature_id = "%d_%d" % (r1, r2)
				feature_text = " ".join(map(lambda i: tokens[i].lower(), xrange(r1, r2 + 1)))
				mention_text_1 = " ".join(map(lambda i: tokens[i].lower(), ranges1((b1, r11,r12,e1))))
				mention_text_2 = " ".join(map(lambda i: tokens[i].lower(), ranges1((b2, r21,r22,e2))))
				feature_text_le = " ".join(map(lambda i: lemmas[i].lower(), xrange(r1, r2 + 1)))
				mention_text_1_le = " ".join(map(lambda i: lemmas[i].lower(), ranges1((b1, r11,r12,e1))))
				mention_text_2_le = " ".join(map(lambda i: lemmas[i].lower(), ranges1((b2, r21,r22,e2))))
				con_value = confidence(mention_text_1,feature_text,mention_text_2,tokens,keywords)
				if mention_text_1 != mention_text_2 and error_checking(feature_text_le,mention_text_1_le,mention_text_2_le):  
					yield 	[doc_id+"_"+str(sentence_index),mention_id_1,feature_id,mention_id_2,mention_text_1,feature_text,mention_text_2,mention_text_1_le,feature_text_le,mention_text_2_le,con_value,keywords]


'''
	relationlist= ['believe', 'cultivate', 'exploit', 'accomplish', 'imply', 'confirm', 'produce', 'obtain', 'endorse', 'generate', 'induce', 'embrace', 'fulfil', 'argue', 'grasp', 'nurture', 'reveal', 'propose', 'agree', 'elicit', 'fulfill', 'accommodate', 'indicate', 'recommend', 'accept', 'derive', 'exhibit', 'attain', 'suggest', 'advocate', 'yield', 'show', 'emphasize', 'satisfy', 'emerge', 'discover', 'give', 'present', 'serve', 'provide', 'offer', 'beneficial', 'able', 'assist', 'desire', 'go', 'helpful', 'hope', 'reluctant', 'interested', 'get', 'unable', 'empower', 'want', 'enable', 'help', 'permit', 'difficult', 'vital', 'aid', 'make', 'establish', 'prepare', 'construct', 'nurture', 'build', 'equip', 'develop', 'evolve', 'broaden', 'sustain', 'motivate', 'create', 'development', 'foster', 'expand', 'stimulate', 'design', 'cultivate', 'undermine', 'become', 'inspire', 'enrich', 'constrain', 'hinder', 'strengthen', 'comprise', 'consist', 'include', 'support', 'lower', 'acquire', 'lead', 'ensure', 'enrich', 'greater', 'facilitate', 'motivate', 'alter', 'encourage', 'constrain', 'enhance', 'gain', 'promote', 'increase', 'inhibit', 'less', 'maximize', 'insufficient', 'limit', 'benefit', 'guide', 'inadequate', 'shape', 'low', 'hinder', 'contribute', 'inform', 'improve', 'higher', 'decrease', 'possess', 'take', 'inadequate', 'require', 'enough', 'key', 'critical', 'lack', 'necessary', 'vital', 'sufficient', 'essential', 'crucial', 'insufficient', 'resolve', 'arise', 'identify', 'consider', 'raise', 'confront', 'depend', 'avoid', 'determine', 'remove', 'emphasize', 'rely', 'address', 'eliminate', 'overcome', 'minimize', 'characterize', 'infer', 'modify', 'clarify', 'adapt', 'activate', 'adjust', 'recognize', 'interact', 'alter', 'shape', 'affect', 'influence', 'chance', 'attempt', 'seek', 'begin', 'start', 'predict', 'receive', 'bring', 'employ', 'utilize', 'put', 'combine', 'introduce', 'transform', 'implement', 'integrate', 'deliver', 'incorporate', 'apply', 'adopt', 'change', 'move', 'shift', 'focus', 'reach', 'achieve', 'achieve', 'complete', 'continue', 'prevent', 'avoid', 'remove', 'minimize', 'overcome', 'reduce', 'eliminate', 'challenge', 'difficulty', 'successfully', 'effectively', 'important', 'success', 'relevant', 'successful', 'effective', 'useful', 'depend', 'depict', 'comprise', 'reflect', 'constitute', 'believe', 'agree', 'preserve', 'sustain', 'favor', 'prefer', 'decide', 'choose', 'choice', 'select', 'assign', 'fail', 'result', 'emerge', 'lead', 'finding', 'become', 'ask', 'resist', 'solve', 'decline', 'grow', 'surge', 'rise', 'ever-increasing', 'bolster', 'deteriorate', 'diminish', 'highest', 'fluctuate', 'lowest', 'accelerate']
'''

