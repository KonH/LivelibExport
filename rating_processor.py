import math
from book import Book

# 10-star to 5-star rating converter
class RatingProcessor:
	def is_applicable(this, books: list[Book]):
		for book in books:
			if (book.max_rating is not None and book.max_rating > 5) or isinstance(book.rating, float):
				return True
		return False

	def change_rating(this, books: list[Book], ceil: bool):
		for book in books:
			if book.max_rating is not None:
				raw_rating = (book.rating / (book.max_rating / 5))
				if ceil:
					book.rating = math.ceil(raw_rating)
				else:
					book.rating = math.floor(raw_rating)
