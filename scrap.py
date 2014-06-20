import requests
import re
from bs4 import BeautifulSoup
teams = [{"team":"Atlanta","id":"404085"},{"team":"Boston","id":"404169"},{"team":"Brooklyn","id":"404117"},{"team":"Charlotte","id":"664421"},{"team":"Chicago","id":"404198"},{"team":"Cleveland","id":"404213"},{"team":"Dallas","id":"404047"},{"team":"Denver","id":"404065"},{"team":"Detroit","id":"404153"},{"team":"Golden State","id":"404119"},{"team":"Houston","id":"404137"},{"team":"Indiana","id":"404155"},{"team":"L.A. Clippers","id":"404135"},{"team":"L.A. Lakers","id":"403977"},{"team":"Memphis","id":"404049"},{"team":"Miami","id":"404171"},{"team":"Milwaukee","id":"404011"},{"team":"Minnesota","id":"403995"},{"team":"New Orleans","id":"404101"},{"team":"New York","id":"404288"},{"team":"Oklahoma City","id":"404316"},{"team":"Orlando","id":"404013"},{"team":"Philadelphia","id":"404083"},{"team":"Phoenix","id":"404029"},{"team":"Portland","id":"403993"},{"team":"Sacramento","id":"403975"},{"team":"San Antonio","id":"404302"},{"team":"Toronto","id":"404330"},{"team":"Utah","id":"404031"},{"team":"Washington","id":"404067"}];

def getData(url,team):
	r = requests.get(url)
	soup = BeautifulSoup(r.text)

	for trow in soup.find_all('tr', {'class':'datarow'}):
		children = trow.findChildren()
		f.write('\n')
		strrow = team
		for i in range(len(children)):
			if (i == 2 or i == 4): #skip duplicate values
				continue
			child = children[i]
			value = str(child.text).replace('\n', ',').replace('\r', '')
			value = " ".join(value.split()) ## remove multiple duplicate whitespaces
			strrow += value
		#clean and transform data to desire format for csv file
		strrow = re.sub(r',\s|\s,', ',', strrow).replace(',,', ',') #remove whitespaces
		strrow = re.sub(r'^,', '', strrow) 
		strrow = re.sub(r'(L|W)\s', r'\1,', strrow) #seprate game outcomes from score
		strrow = re.sub(r'(O|U)\s', r'\1,', strrow) #seperate OU outcomes into two columns
		f.write(strrow)
	return

for i in range(len(teams)):
	team = teams[i]['team']
	tId = teams[i]['id']
	f = open(team, 'w')
	f.write('Team,Date,Opp,Outcome,Score,Gametype,Spread Outcome,Spread,OU OutCome,OU')
	years = ['2013-2014', '2012-2013', '2011-2012', '2010-2011', '2009-2010', '2008-2009', '2007-2008', '2006-2007', '2005-2006', '2004-2005']
	for i in range(len(years)):
		url = 'http://www.covers.com/pageLoader/pageLoader.aspx?page=/data/nba/teams/pastresults/' + years[i] +'/team' +tId + '.html'
		getData(url, team)
	f.close()
