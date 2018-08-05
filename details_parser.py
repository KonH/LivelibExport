from lxml import html
from lxml import etree
from book import Book

def parse_isbn_str(isbn_str):
	raw_isbn_str = isbn_str
	isbn = raw_isbn_str.split(',')[:1][0].split(' ')[0]
	return isbn

def normalize_isbn(isbn):
	return isbn.replace('-', '').replace('.', '')

def first_text_or_none(items):
	if len(items) > 0:
		return items[0].text
	else:
		return None

def try_extract_name_from_span(book_html):
	name_spans = book_html.xpath('//span[@itemprop="name"]')
	return first_text_or_none(name_spans)

def try_extract_name_from_header(book_html):
	headers = book_html.xpath('//h1[@id=\"book-title\"]')
	return first_text_or_none(headers)

def try_extract_name(book_html, book):
	name = try_extract_name_from_span(book_html)
	if name is not None:
		book.add_name(name)
		return
	name = try_extract_name_from_header(book_html)
	if name is not None:
		book.add_name(name)
		return
	print('try_extract_name(%s): can\'t find name.' % book.id)	

def parse_downloaded_book(book_content, book):
	if book_content is not None:
		book_html = html.fromstring(book_content)
		try_extract_name(book_html, book)
		isbn_spans = book_html.xpath('//span[@itemprop="isbn"]')
		if len(isbn_spans) > 0:
			raw_isbn = isbn_spans[0].text
			isbn = normalize_isbn(parse_isbn_str(raw_isbn))
			book.add_isbn(isbn)
		else:
			print('parse_downloaded_book(%s): can\'t find ISBN.' % book.id)
		return book

# Parse detail pages to update Book entries
class DetailsParser:
	def __init__(this, cache):
		this.cache = cache

	def parse(this, books):
		ready_books = []
		for book in books:
			book_content = this.cache.load(book.id)
			ready_book = parse_downloaded_book(book_content, book)
			if ready_book is not None:
				ready_books.append(ready_book)
		return ready_books
	