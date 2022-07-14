class Book:
	def __init__(this, link, rating, date):
		this.link = link
		this.rating = rating
		this.id = link[link.rfind("/")+1:]
		this.date = date
		this.name = None
		this.ISBN = None
	
	def __str__(this):
		return 'id="%s", link="%s", rating="%s", name="%s", isbn="%s"' % (this.id, this.link, this.rating, this.date, this.name, this.ISBN)

	def add_isbn(this, isbn):
		this.ISBN = isbn

	def add_name(this, name):
		this.name = name
