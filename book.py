class Book:
	def __init__(this, link: str, rating: int, max_rating: int, date: str):
		this.link = link
		this.rating = rating
		this.max_rating = max_rating
		this.id : str = link[link.rfind("/")+1:]
		this.date = date
		this.authors = None
		this.name = None
		this.ISBN = None
	
	def __str__(this):
		return ('id="%s", link="%s", rating="%s", max_rating="%s", date="%s", authors="%s", name="%s", isbn="%s"'
				% (this.id, this.link, this.rating, this.max_rating, this.date, this.authors, this.name, this.ISBN))

	def add_isbn(this, isbn: str):
		this.ISBN = isbn

	def add_authors(this, authors: list):
		this.authors = authors

	def add_name(this, name: str):
		this.name = name
