import pandas as pd
import numpy as np

print("\nDESCRIPTION: 'relation_mapping.py' will create a dictionary of mapped relation words using '/media/aabhaschauhan/Data/ERIC/Results/all_top_relations.csv' as the input file with headers 'word' and 'tag'.\n\n\n")

aft = raw_input("Do you want to change the input file (y/n)?\n\nRESPONSE:	")
while (aft!='y' and aft!='n'):	aft = raw_input("Enter a valid response (y/n):	")
if aft=='y':	filename = raw_input("Enter csv input file name stored at '/media/aabhaschauhan/Data/ERIC/Results'\n<NOTE> For multi-tags of a word, separate them by a comma followed by a space. For example 3, 4.\n\nRESPONSE:	")
else:	filename = 'relation_bucket_tagging_V2.1_AC.csv'

pp1 = pd.read_csv('/media/aabhaschauhan/Data/ERIC/Results/' + filename)
l1 = len(pp1)
d1 = dict()
for i in range(l1):
	if pp1['tag'][i]!=0:	d1[pp1['word'][i]] = [pp1['tag'][i]]
	else:	continue

np.save('/media/aabhaschauhan/Data/ERIC/Results/rel_map_V2.0_AC.npy',d1)
print "\nDictionary saved as: '/media/aabhaschauhan/Data/ERIC/Results/rel_map_V2.0_AC.npy'"




