import requests

from bs4 import BeautifulSoup

def parse( url , out ):

	r = requests.get( url )
	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "lxml" )

	for teksti in soup.find_all( class_='post-content span8' ):
		for p in teksti.find_all( 'p' ):

			for string in p.stripped_strings:
	        		out.write( string.encode('utf8') + ' ' )

if __name__ == '__main__':
	parse("https://www.suomenuutiset.fi/perussuomalaiset-hurjassa-nosteessa-puoluesihteeri-ei-yllattynyt/", file('suomenuutiset.txt', 'w'))
