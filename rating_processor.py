from book import Book

# 10-star to 5-star rating converter
class RatingProcessor:
	def is_applicable(this, books):
		for book in books:
			if book.max_rating is not None and book.max_rating > 5:
				return True
		return False

	def change_rating(this, books):
		for book in books:
			if book.max_rating is not None:
				book.rating = int(book.rating / (book.max_rating / 5))
