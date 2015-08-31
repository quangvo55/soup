import requests
import re
from bs4 import BeautifulSoup

def getData(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	name = soup.find_all('div', {'class':'teamname'})
	f.write(cleanString(name[0].text) + '\n')
	t = soup.find_all('table')
	#only get regular season data
	table = t[1] if len(t) == 3 else t[0]

	games = table.findChildren('tr')
	for i in range(1, len(games)):
		strrow = ''
		for gameData in games[i].findChildren('td'):
			value = cleanString(gameData.text)
			strrow += value + ', '
		strrow = re.sub(r'(L|W)\s', r'\1,', strrow) #separate game outcomes from score
		strrow = re.sub(r'(O|U)\s', r'\1,', strrow) #separate OU outcomes into two columns
		f.write(strrow)
		f.write('\n')
	f.write('\n')
	return

def cleanString(stringInput):
	s = str(re.sub('\s+',' ', stringInput))
	return " ".join(s.split())

f = open('nflspread', 'w')
f.write('Date,Opp,Outcome,Score,Week,SpreadOutcome,Spread,OU,OUNumber')
f.write('\n')
for i in range(1,33):
	url = 'http://www.covers.com/pageLoader/pageLoader.aspx?page=/data/nfl/teams/pastresults/2014-2015/team' + str(i) + '.html'
	getData(url)
f.close()