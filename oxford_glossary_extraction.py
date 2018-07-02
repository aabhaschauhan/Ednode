import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
tt=[]
for i in range(1,12):
	print i
	page = requests.get("http://www.oxfordreference.com/view/10.1093/acref/9780199679393.001.0001/acref-9780199679393?btog=chap&hide=true&page="+str(i)+"&pageSize=100&skipEditions=true&sort=titlesort&source=%2F10.1093%2Facref%2F9780199679393.001.0001%2Facref-9780199679393")
	soup = bs(page.content, 'html.parser')
	for abc in soup.find_all('h2',class_='itemTitle'):
		tt += [abc.get_text().replace('\n','')]
df1 = pd.DataFrame(tt,columns=['Word'])
df1.to_csv('/media/aabhaschauhan/Data/ERIC/Results/ed_glossary.csv',sep='\t', encoding='utf-8')
