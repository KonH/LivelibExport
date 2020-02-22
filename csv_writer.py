import os
from book import Book

def str_or_empty(str):
	if str is None:
		return ''
	else:
		return str

def format_book(book):
	return "%s; %s; %s; %s; %s\n" % (book.id, str_or_empty(book.name), str_or_empty(book.ISBN), book.rating, book.date)

# Write books content to csv file
class CsvWriter():
	def save(this, books, file_name):
		with open(file_name, 'w', encoding="utf-8") as file:
			file.write('ID; Title; ISBN; My Rating; Date Added\n')
			for book in books:
				file.write(format_book(book))