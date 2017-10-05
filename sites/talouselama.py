# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( class_ = 'sc-cJOK iSzzsB' )
	if article == None:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	processor.decompose_all( article.find_all( 'aside' ) )

	categories = processor.collect_categories( [article.find( class_ = 'sc-bGbJRg fjsUfa' )] )
	datetime_list = processor.collect_datetime( article.find( class_ = 'sc-likbZx fZfPtD' ) )
	title = processor.collect_text( article.find( 'h1' ) )
	ingress = processor.collect_text( article.find( 'h3' ) )
	text = processor.collect_text( article.find( class_ = 'sc-fyjhYU' ) )
	images = processor.collect_images( [article.find( 'img' )], 'src', '')
	captions = processor.collect_image_captions( article.find_all( 'figcaption' ) )

	return processor.create_dictionary('Talouselämä', url, r.status_code, categories, datetime_list, u'', title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.talouselama.fi/vaalit/vaalitebatti/murtuuko+suurten+puolueiden+valta++vaaliraati+vastaa/a2301513", file('talouselama.txt', 'w'))
