import os
from book import Book

def str_or_empty(str):
	if str is None:
		return ''
	else:
		return str

def joined_list_or_empty(list):
	if list is None:
		return ''
	else:
		return ", ".join(list)

def rating_or_empty(rating):
	return rating if rating != -1 else ''

def format_book(book: Book):
	return "%s; %s; %s; %s; %s; %s\n" % (book.id, joined_list_or_empty(book.authors), str_or_empty(book.name), str_or_empty(book.ISBN), rating_or_empty(book.rating), book.date)

# Write books content to csv file
class CsvWriter():
	def save(this, books: list[Book], file_name: str):
		with open(file_name, 'w', encoding="utf-8") as file:
			file.write('ID; Author; Title; ISBN; My Rating; Date Added\n')
			for book in books:
				file.write(format_book(book))