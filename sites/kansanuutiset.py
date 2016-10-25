# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( 'article' )
	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose( article.find( 'footer' ) )
	processor.decompose_all( article.find_all( class_ = 'cb-module-title' ) )
	processor.decompose_all( article.find_all( 'blockquote' ) )

	categories = processor.collect_categories( article.find_all( class_ = 'cb-category' ) )
	datetime_list = processor.collect_datetime( article.find( class_ = 'cb-date' ), '' )
	author = processor.collect_text( article.find( class_ = 'cb-author' ) )
	title = processor.collect_text( article.find( class_ = 'entry-title' ) )

	ingress_tag = article.find( class_ = 'cb-entry-content' ).find( 'h4' )
	ingress = processor.collect_text( ingress_tag )
	ingress_tag.decompose()

	text = processor.collect_text( article.find( class_ = 'cb-entry-content' ) )
	images = processor.collect_images( article.find_all( 'img' ), '' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'caption' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.kansanuutiset.fi/kulttuuri/kirjat/3341821/lahi-idan-rajoja-vedetaan-uusiksi", file('kansanuutiset.txt', 'w'))
