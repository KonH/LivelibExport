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
		this.name = None
		this.ISBN = None
	
	def __str__(this):
		return 'id="%s", link="%s", rating="%s", name="%s", isbn="%s"' % (this.id, this.link, this.rating, this.name, this.ISBN)

	def add_isbn(this, isbn):
		this.ISBN = isbn

	def add_name(this, name):
		this.name = name

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

def get_path_in_cache(cache_dir, id):
	return path.join(cache_dir, id + '.html')

def try_download_book_page(book, cache_dir):
	print('Downloading book with id = "%s" from "%s"' % (book.id, book.full_link))
	cache_file_name = get_path_in_cache(cache_dir, book.id)
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

def parse_books(content):
	books = []
	books_html = html.fromstring(content)
	rows = books_html.xpath('//tr')
	for row in rows:
		result = parseBook(row)
		if result is not None:
			books.append(result)
	return books

def load_book_content_from_cache(cache_dir, id):
	file_name = get_path_in_cache(cache_dir, id)
	try:
		with open(file_name, 'r') as file:
			return file.read()
	except Exception as ex:
		print('load_book_content_from_cache("%s"): %s' % (file_name, ex))
		return None

def parse_isbn_str(isbn_str):
	raw_isbn_str = isbn_str
	isbn = raw_isbn_str.split(',')[:1][0]
	return isbn

def normalize_isbn(isbn):
	return isbn.replace('-', '')

def parse_downloaded_book(cache_dir, book):
	book_content = load_book_content_from_cache(cache_dir, book.id)
	if book_content is not None:
		book_html = html.fromstring(book_content)
		name_spans = book_html.xpath('//span[@itemprop="name"]')
		if len(name_spans) > 0:
			name = name_spans[0].text
			book.add_name(name)
		else:
			print('parse_downloaded_book(%s): can\'t find name.' % book.id) 
		isbn_spans = book_html.xpath('//span[@itemprop="isbn"]')
		if len(isbn_spans) > 0:
			raw_isbn = isbn_spans[0].text
			isbn = normalize_isbn(parse_isbn_str(raw_isbn))
			book.add_isbn(isbn)
		else:
			print('parse_downloaded_book(%s): can\'t find ISBN.' % book.id)
		return book

def parse_downloaded_books(cache_dir, books):
	ready_books = []
	for book in books:
		ready_book = parse_downloaded_book(cache_dir, book)
		if ready_book is not None:
			ready_books.append(ready_book)
	return ready_books

def str_or_empty(str):
	if str is None:
		return ''
	else:
		return str

def format_book(book):
	return "%s; %s; %s; %s\n" % (book.id, str_or_empty(book.name), str_or_empty(book.ISBN), book.rating)

def save_books(books, file_name):
	with open(file_name, 'w') as file:
		file.write('ID; Title; ISBN; My Rating\n')
		for book in books:
			file.write(format_book(book))

# settings
input_file_name = 'read.html'
cache_dir_name = 'cache'
out_file_name = 'out.csv'

print('Load books from file: "%s"' % input_file_name)
books_content = load_books(input_file_name)
if books_content is None:
	exit(1)
print('Books loaded.')

print('Parse books from summary.')
books = parse_books(books_content)
print('Books parsed: %s.' % len(books))

print('Start download detailed book pages.')
download_book_pages(books, cache_dir_name, min_delay=90, max_delay=120)
print('Detailed book pages downloaded.')

print('Prepare books for export.')
ready_books = parse_downloaded_books(cache_dir_name, books)
print('Books ready to export: %s.' % len(ready_books))

save_books(ready_books, out_file_name)
print('Books saved to "%s"' % out_file_name)