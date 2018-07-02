import ast
import pandas as pd
import json
import itertools as it
import numpy as np

print("\nDESCRIPTION: 'json_graph.py' will create JSON files which will be used as input for the front end of the network.\n\n\n")

file_map={"['0','1','2','3']":'influence_ednode.json',"['0','1','2']":'directandinf_ednode.json',"['0']":'big_ednode.json',"['0','1','3','4','5']":'neutral_ednode.json', "['0','1','2','4','5']":'directional_ednode.json'}

def mapped_word(l2):
	mp = []
	for a1 in list(l2):
		temp = []
		for a2 in ast.literal_eval(a1):	temp += [a2[0]]
		mp += [temp]
	return mp

dd = np.load('/media/aabhaschauhan/Data/ERIC/Results/node_lemma_to_token_V1.2_AC.npy').item()
pp = pd.read_csv('/media/aabhaschauhan/Data/ERIC/mapping_node_edge1_V2.2_AC.csv')
a = list(pp['a'])
b = list(pp['b'])
c = list(pp['c'])
triplet = list(pp['triplet'])
rel_buck = [max(ast.literal_eval(a1)) for a1 in list(pp['relation_bucket'])]
incs = list(pp['incs'])
inf = list(pp['inf'])
key_match = [ast.literal_eval(b1)[1] for b1 in list(pp['confidence_value'])]
mapa = mapped_word(pp['mapped word A'])
mapb = mapped_word(pp['mapped word B'])
l1 = len(a)

for k in file_map.keys():
	combo = []
	for i in range(l1):
		a1,a2,r = mapa[i],mapb[i],rel_buck[i]
		if not(r in ast.literal_eval(k)) and (not(incs[i]<0.1) or not(incs[i]>0.80 and inf[i]>95)):
			combo += [(dd[abc[0]].title(),r,dd[abc[1]].title()) for abc in it.product(a1,a2)]
	nodes,links= [],[] 
	node1 = []; node2=[];
	d1,d2,d3 = dict(),dict(),dict();
	for c11 in combo:
		d3[c11[0]+'_'+c11[2]],d3[c11[2]+'_'+c11[0]]=0,0
		node1 += [c11[0]]
		node2 += [c11[2]]
	for abc in list(set(node1+node2)):	d1[abc] = 0
	for abc in combo:
		if ((abc[0] != abc[2]) and (d3[abc[0]+'_'+abc[2]]!=1) and (d3[abc[2]+'_'+abc[0]]!=1)):
			d3[abc[0]+'_'+abc[2]],d3[abc[2]+'_'+abc[0]]=1,1
			d1[abc[0]] += 1
			d1[abc[2]] += 1
		if abc in d2 or (abc[2],abc[1],abc[0]) in d2:	
			try:	d2[abc] += 1
			except Exception:	d2[(abc[2],abc[1],abc[0])] += 1
		else:	d2[abc] = 1
	for abc in d1.keys():	nodes += [{"id":abc,"group":d1[abc]}]
	for abc in d2.keys():	links += [{"source":abc[0],"target":abc[2],"rb":abc[1],"freq":d2[abc]}]
	d3= {'nodes':nodes, 'links':links}
	with open('/home/aabhaschauhan/Ednode_Front/Ednode/Data/'+file_map[k],'w') as f:	f.write(json.dumps(d3))
	if file_map[k] == 'big_ednode.json':
		t=[]
		for a11 in links:	t+=[[a11['source'],a11['rb'],a11['target'],a11['freq']]]
		pd.DataFrame(t,columns=['source_node','relation_bucket','target_node','frequency']).to_csv('/media/aabhaschauhan/Data/ERIC/Results/Front_End_Output/mapped_front_end_V2.0.csv')
	
		
	

