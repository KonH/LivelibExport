import time
import random
from urllib import request

def download_book_page(link):
	print('Start download page from "%s"' % link)
	with request.urlopen(link) as data:
		content = data.read()
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
		print('Downloading book with id = "%s" from "%s"' % (book.id, book.full_link))
		if this.cache.is_cached(book.id):
			print('Already in cache, skipping.')
			return False
		else:
			page = download_book_page(book.full_link)
			cache.save(book.id, page)
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