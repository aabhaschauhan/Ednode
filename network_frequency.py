import pandas as pd
import numpy as np

pp = pd.read_csv('/media/aabhaschauhan/Data/ERIC/mapping.csv')
a=[abc.split("'")[1] for abc in pp['mapped word A']]
b=[abc.split("'")[1] for abc in pp['mapped word B']]
c = list(set(a+b))
l = len(a)
d= dict()
for i in range(l):
	t1,t2 = pp['mapped word A'][i].split("'")[1],pp['mapped word B'][i].split("'")[1]
	if not(t1 in d):	d[t1] = [[t2,1]]
	else:
		temp1 = [abc[0] for abc in d[t1]]
		if t2 in temp1:	d[t1][temp1.index(t2)][1] += 1
		else:	d[t1] += [[t2,1]]
	if not(t2 in d):	d[t2] = [[t1,1]]
	else:
		temp2 = [abc[0] for abc in d[t2]]
		if t1 in temp2:	d[t2][temp2.index(t1)][1] += 1
		else:	d[t2] += [[t1,1]]

