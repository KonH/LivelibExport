import re
from collections import defaultdict
from lxml import html
from lxml import etree
from book import Book

def get_rating_from_title(rating_title):
	try:
		parts = rating_title.split()
		return int(parts[-3])
	except ValueError:
		# Case for 'нет рейтинга' string
		return None
	except Exception as ex:
		print('get_rating_from_title("%s"): %s' % (rating_title, ex))
		return None

def get_max_rating_from_title(rating_title):
	try:
		parts = rating_title.split()
		return int(parts[-1])
	except ValueError:
		# Case for 'нет рейтинга' string
		return None
	except Exception as ex:
		print('get_max_rating_from_title("%s"): %s' % (rating_title, ex))
		return None

def try_get_link(link):
	if "/book/" in link:
		return link
	return None

def parse_book(row, last_date):
	link = None
	rating = None
	max_rating = None

	for cell in row.iter():
		if rating is None:
			spans = cell.xpath('.//span')
			if len(spans) == 2:
				rating_title = spans[1].get('title')
				rating = get_rating_from_title(rating_title)
				max_rating = get_max_rating_from_title(rating_title)
		if link is None:
			hrefs = cell.xpath('.//a')
			for href in hrefs:
				link = try_get_link(hrefs[0].get('href'))

	if link is not None and rating is not None:
		return Book(link, rating, max_rating, last_date)
	if link is not None or rating is not None:
		if link is None:
			print('Parsing error (link is not parsed):')
		if rating is None:
			print('Parsing error (rating is not parsed):')
		print(etree.tostring(row))
		print('')
	return None

def try_parse_month(raw_month):
	dict = defaultdict(lambda: '01', {
		'Январь': '01',
		'Февраль': '02',
		'Март': '03',
		'Апрель': '04',
		'Май': '05',
		'Июнь': '06',
		'Июль': '07',
		'Август': '08',
		'Сентябрь': '09',
		'Октябрь': '10',
		'Ноябрь': '11',
		'Декабрь': '12'
	})
	return dict[raw_month]

def try_parse_date(row):
	headers = row.xpath('.//td/h2')
	for header in headers:
		raw_text = header.text
		if raw_text is not None:
			m = re.search('\d{4} г.', raw_text)
			if m is not None:
				year = m.group(0).split(' ')[0]
				raw_month = raw_text.split(' ')[0]
				month = try_parse_month(raw_month)
				return '%s-%s-01' % (year, month)
	return None

# ReadParser - parse read list in html format
class ReadParser:
	def load_from_file(this, file_name):
		try:
			with open(file_name, 'r', encoding="utf-8") as file:
				this.content = file.read()
				return True
		except Exception as ex:
			print('load_from_file("%s"): %s' % (file_name, ex))
			this.content = None
			return False

	def parse_books(this):
		books = []
		books_html = html.fromstring(this.content)
		rows = books_html.xpath('//tr')
		last_date = None
		for row in rows:
			result = parse_book(row, last_date)
			if result is not None:
				books.append(result)
			else:
				date = try_parse_date(row)
				if date is not None:
					last_date = date
		return books
