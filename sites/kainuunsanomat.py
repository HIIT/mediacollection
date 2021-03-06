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

	article = soup.find( 'article' )
	if article == None:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose_all( article.find_all( class_ = 'attImage' ) )

	meta = article.find( 'time' )

	categories = processor.collect_categories( meta.find_all( 'b' ) )
	datetime_list = processor.collect_datetime( meta )

	author = processor.collect_text( article.find( class_ = 'Kirjoittaja' ), True )
	title = processor.collect_text( article.find( 'h1' ) )
	ingress = processor.collect_text( article.find( class_ = 'Alaotsikko' ) )
	text = processor.collect_text( article.find( class_ = 'Teksti' ) )
	images = processor.collect_images( article.find_all( 'img' ), 'src', '' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'featuredCaption' ) )

	return processor.create_dictionary('Kainuun sanomat', url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)


def parse_from_archive(url, content):

	article = BeautifulSoup( content, "html.parser" )

	if article == None:
		return processor.create_dictionary('Kainuun sanomat', url, 404, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	meta = article.find( class_ = 'hakutuloslahde' )

	datetime_list = processor.collect_datetime( meta )

	categories = [processor.collect_text( meta ).split(',')[1].strip()]

	author = processor.collect_text( article.find( class_ = 'signeeraus' ) )

	title = processor.collect_text( article.find( class_ = 'otsikko' ) )

	text_divs = article.find_all( class_ = 'artikkelip')
	text = ''
	for text_content in text_divs:
		text += processor.collect_text(text_content) + ' '
	text = text.strip()

	captions = processor.collect_image_captions( article.find_all( class_ = 'kuva') )

	return processor.create_dictionary('Kainuun sanomat', url, 200, categories, datetime_list, author, title, u'', text, [u''], captions)


if __name__ == '__main__':
	parse("http://www.kainuunsanomat.fi/kainuun-sanomat/kotimaa/lipponen-moitti-sipilan-puheita-ministerien-vahentamisesta/", file('kainuunsanomat.txt', 'w'))
