import time
import random
from urllib import request

def assert_page_content(content: bytes):
	str = content.decode('utf-8')
	if 'captcha-show' in str:
		print('Suspicios page content: %s' % str)
		raise Exception('DDoS protection page found, please adjust your settings and wait some time')

def download_book_page(link):
	print('Start download page from "%s"' % link)
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}
	req = request.Request(link, headers = headers)
	r = request.urlopen(req)
	with r as data:
		content: bytes = data.read()
		assert_page_content(content)
		print('Page downloaded.')
		return content

def wait_for_delay(delay):
	print("Waiting %s sec..." % delay)
	time.sleep(delay)

# Page loader to download book pages to cache
class PageLoader:
	def __init__(this, cache, min_delay, max_delay):
		this.cache = cache
		this.min_delay = min_delay
		this.max_delay = max_delay

	def try_download_book_page(this, book):
		full_link = "https://livelib.ru/book/" + book.id
		print('Downloading book with id = "%s" from "%s"' % (book.id, full_link))
		if this.cache.is_cached(book.id):
			print('Already in cache, skipping.')
			return False
		else:
			page = download_book_page(full_link)
			this.cache.save(book.id, page)
			return True

	def download(this, books):
		count = 1
		total = len(books)
		for book in books:
			print('%s/%s' % (count, total))
			count += 1
			if this.try_download_book_page(book):
				delay = random.randint(this.min_delay, this.max_delay)
				wait_for_delay(delay)
			print()
