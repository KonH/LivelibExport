import os
from os import path
import time
import random
from lxml import html
from lxml import etree
from urllib import request

class Book:
	def __init__(this, link, rating):
		this.link = link
		this.rating = rating
		this.id = link[6:]
		this.full_link = 'https://www.livelib.ru' + link
	
	def __str__(this):
		return 'id="%s", link="%s", rating="%s"' % (this.id, this.link, this.rating)

def get_rating_from_class(rating_class):
	try:
		if rating_class[0] == 'r':
			return int(rating_class[1:2])
		return None
	except Exception as ex:
		print('get_rating_from_class("%s"): %s' % (rating_class, ex))
		return None

def load_books(file_name):
	try:
		with open(file_name, 'r') as file:
			return file.read()
	except Exception as ex:
		print('load_books("%s"): %s' % (file_name, ex))
		return None

def try_get_link(link):
	if link.startswith("/book/"):
		return link
	return None

def parseBook(row):
	link = None
	rating = None

	for cell in row.iter():
		if rating is None:
			spans = cell.xpath('.//span')
			if len(spans) == 2:
				rating_class = spans[1].get('class')
				rating = get_rating_from_class(rating_class)
		if link is None:
			hrefs = cell.xpath('.//a')
			for href in hrefs:
				link = try_get_link(hrefs[0].get('href'))

	if link is not None and rating is not None:
		return Book(link, rating)
	if link is not None:
		print('Parsing error (rating not parsed):')
		print(etree.tostring(row))
		print('')
	if rating is not None:
		print('Parsing error (link not parsed):')
		print(etree.tostring(row))
		print('')
	return None

def ensure_cache_dir(cache_dir):
	if not path.exists(cache_dir):
		os.mkdir(cache_dir)

def save_book_page_to_cache(file_name, content):
	with open(file_name, 'wb') as file:
		print('Save to cache: "%s"' % file_name)
		file.write(content)

def download_book_page(link):
	print('Start download page from "%s"' % link)
	with request.urlopen(link) as data:
		content = data.read()
		print('Page downloaded.')
		return content

def try_download_book_page(book, cache_dir):
	print('Downloading book with id = "%s" from "%s"' % (book.id, book.full_link))
	cache_file_name = path.join(cache_dir, book.id + '.html')
	if path.exists(cache_file_name):
		print('Already in cache, skipping.')
		return False
	else:
		page = download_book_page(book.full_link)
		save_book_page_to_cache(cache_file_name, page)
		return True

def wait_for_delay(delay):
	print("Waiting %s sec..." % delay)
	time.sleep(delay)

def download_book_pages(books, cache_dir, min_delay, max_delay):
	ensure_cache_dir(cache_dir)
	count = 1
	total = len(books)
	for book in books:
		print('%s/%s' % (count, total))
		count += 1
		if try_download_book_page(book, cache_dir):
			delay = random.randint(min_delay, max_delay)
			wait_for_delay(delay)
		print()

def parseBooks(content):
	books = []
	books_html = html.fromstring(content)
	rows = books_html.xpath('//tr')
	for row in rows:
		result = parseBook(row)
		if result is not None:
			books.append(result)
	return books

file_name = 'read.html'
print('Load books from file: "%s"' % file_name)
books_content = load_books(file_name)
if books_content is None:
	exit(1)
print('Books loaded.')

books = parseBooks(books_content)
print("Books parsed: %s" % len(books))

download_book_pages(books, 'cache', min_delay=90, max_delay=120)
