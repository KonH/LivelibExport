from lxml import html
from lxml import etree
from book import Book

def parse_isbn_str(isbn_str):
	raw_isbn_str = isbn_str
	isbn = raw_isbn_str.split(',')[:1][0]
	return isbn

def normalize_isbn(isbn):
	return isbn.replace('-', '')

def parse_downloaded_book(book_content, book):
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
	