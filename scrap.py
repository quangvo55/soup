import requests
import re
from bs4 import BeautifulSoup

def getData(url):
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)

	for trow in soup.find_all('tr', {'class':'datarow'}):
		children = trow.findChildren()
		f.write('\n')
		strrow = '';
		for i in range(len(children)):
			if (i == 2 or i ==4):
				continue
			child = children[i]
			value = str(child.text).replace('\n', ',').replace('\r', '')
			value = " ".join(value.split())
			strrow += value
		strrow = re.sub(r',\s|\s,', ',', strrow).replace(',,', ',')
		strrow = re.sub(r'^,', '', strrow)
		strrow = re.sub(r'(L|W)\s', r'\1,', strrow)
		strrow = re.sub(r'(O|U)\s', r'\1,', strrow)
		f.write(strrow)
	return

f = open('test', 'w')
f.write('Date,Team,Outcome,Score,Gametype,Spread Outcome,Spread,OU OutCome,OU')
years = ['2013-2014', '2012-2013', '2011-2012', '2010-2011', '2009-2010', '2008-2009', '2007-2008', '2006-2007', '2005-2006', '2004-2005']
for i in range(len(years)):
	url = 'http://www.covers.com/pageLoader/pageLoader.aspx?page=/data/nba/teams/pastresults/' + years[i] +'/team404169.html'
	getData(url)
f.close()