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

	article = soup.find( class_ = 'article-body-container' )
	if article == None:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose_all( article.find_all( class_ = 'photographer' ) )
	processor.decompose( article.find( class_ = 'linked-articles' ) )
	processor.decompose_all( article.find_all( 'aside' ) )
	processor.decompose( article.find( class_ = 'pagehitcounter' ) )
	processor.decompose( article.find( class_ = 'article-paywall' ) )
	processor.decompose_all( article.find_all( class_ = 'article-ad-block' ) )

	categories = processor.collect_categories( article.find_all( class_ = 'section-name' ) )
	datetime_list = processor.collect_datetime_objects( article.find( class_ = 'article-metasection' ).find_all('time'), 'content' )
	author = processor.collect_text( article.find( class_ = 'author' ) )
	title = processor.collect_text( article.find( 'h1' ) )
	ingress = processor.collect_text( article.find( class_ = 'article-ingress' ) )

	images = processor.collect_images( article.find( class_ = 'article-main-image' ).find_all( 'img' ), 'src', 'http:' )
	images_filt = filter( lambda img: 'data:image' not in img, images )

	captions = processor.collect_image_captions( article.find_all( itemprop = 'caption' ), True )

	processor.decompose_all( article.find_all( class_ = 'embedded-image' ) )
	processor.decompose_all( article.find( class_ = 'body' ).find_all( class_ = 'print-url' ) )

	text = processor.collect_text( article.find( class_ = 'body' ), False )

	return processor.create_dictionary('Helsingin Sanomat', url, r.status_code, categories, datetime_list, author, title, ingress, text, images_filt, captions)

if __name__ == '__main__':

	parse("http://www.hs.fi/paakirjoitukset/a1428030701507", file('hs.txt', 'w'))
