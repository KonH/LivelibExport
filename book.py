class Book:
	def __init__(this, link, rating, max_rating, date):
		this.link = link
		this.rating = rating
		this.max_rating = max_rating
		this.id = link[link.rfind("/")+1:]
		this.date = date
		this.name = None
		this.ISBN = None
	
	def __str__(this):
		return 'id="%s", link="%s", rating="%s", max_rating="%s", name="%s", isbn="%s"' % (this.id, this.link, this.rating, this.max_rating, this.date, this.name, this.ISBN)

	def add_isbn(this, isbn):
		this.ISBN = isbn

	def add_name(this, name):
		this.name = name
