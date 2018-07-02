import psycopg2
import pandas as pd

conn = psycopg2.connect("dbname=edu_learning user=aabhaschauhan password=eval2017!")
cur = conn.cursor()
cur.execute("SELECT tokens,lemmas FROM sentences")
row = cur.fetchone()

combo1,combo2=[],[]
d1 = dict()
print "TOTAL NUMBER OF ROWS: ", cur.rowcount
j=0
while row is not None:
	if j%100000 == 0: print j/100000
	a,b = row
	a,b = list(a),list(b)
	if len(a) == len(b):
		for i in range(len(a)):
			if not(a[i] in d1) and a[i]!=" " and a[i]!="":	
				d1[a[i]] = 0			
				combo1 += [a[i].lower()]
				combo2 += [b[i].lower()]
	row = cur.fetchone()
	j += 1	
df1 = pd.DataFrame(data=[[combo1[i],combo2[i]] for i in range(len(combo1))],columns=["token","lemma"])
df1.to_csv("/media/aabhaschauhan/Data/ERIC/Results/token_lemma.csv", sep='\t', encoding='utf-8')	


