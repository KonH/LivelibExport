import time
import random
import json
import http
from urllib import request

from book import Book
from cache_manager import CacheManager

def assert_page_content(content: bytes):
	str = content.decode('utf-8')
	if 'captcha-show' in str:
		print('Suspicios page content: %s' % str)
		raise Exception('DDoS protection page found, please adjust your settings and wait some time')

def download_book_page_direct(link: str):
	print('Start direct download page from "%s"' % link)
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}
	req = request.Request(link, headers = headers)
	r = request.urlopen(req)
	with r as data:
		content: bytes = data.read()
		assert_page_content(content)
		print('Page downloaded.')
		return content

def create_proxy_session(proxy_host: str):
	print('Create proxy session for "%s"' % proxy_host)
	endpoint = proxy_host + '/v1'
	print('Proxy endpoint: "%s"' % endpoint)
	req_data = {
		'cmd': 'sessions.create',
		'session': 'single_livelib_session'
	}
	req_json = json.dumps(req_data)
	print('Proxy create session request data: "%s"' % req_json)
	req_json_bytes = req_json.encode()
	headers = { 'Content-Type': 'application/json' }
	req = request.Request(endpoint, data=req_json_bytes, method='POST', headers = headers)
	r: http.client.HTTPResponse = request.urlopen(req)
	with r as data:
		full_content: bytes = data.read()
		full_content_str = full_content.decode('utf-8')
		full_content_obj: dict = json.loads(full_content_str)
		status = full_content_obj['status']
		if status == 'ok':
			print('Proxy session successfully created')
		else:
			raise Exception('Unexpected create session status: ' + status)

def destroy_proxy_session(proxy_host: str):
	print('Destroy proxy session for "%s"' % proxy_host)
	endpoint = proxy_host + '/v1'
	print('Proxy endpoint: "%s"' % endpoint)
	req_data = {
		'cmd': 'sessions.destroy',
		'session': 'single_livelib_session'
	}
	req_json = json.dumps(req_data)
	print('Proxy destroy session request data: "%s"' % req_json)
	req_json_bytes = req_json.encode()
	headers = { 'Content-Type': 'application/json' }
	req = request.Request(endpoint, data=req_json_bytes, method='POST', headers = headers)
	r: http.client.HTTPResponse = request.urlopen(req)
	with r as data:
		full_content: bytes = data.read()
		full_content_str = full_content.decode('utf-8')
		full_content_obj: dict = json.loads(full_content_str)
		status = full_content_obj['status']
		if status == 'ok':
			print('Proxy session successfully destroyed')
		else:
			print('Unexpected session destroy status (non-critical): ' + status)

def download_book_page_via_proxy(link: str, proxy_host: str):
	print('Start download page from "%s" using proxy "%s"' % (link, proxy_host))
	endpoint = proxy_host + '/v1'
	print('Proxy endpoint: "%s"' % endpoint)
	req_data = {
		'cmd': 'request.get',
		'url': link,
		'session': 'single_livelib_session',
		'maxTimeout': 60000
	}
	req_json = json.dumps(req_data)
	print('Proxy request data: "%s"' % req_json)
	req_json_bytes = req_json.encode()
	headers = { 'Content-Type': 'application/json' }
	req = request.Request(endpoint, data=req_json_bytes, method='POST', headers = headers)
	r: http.client.HTTPResponse = request.urlopen(req)
	with r as data:
		full_content: bytes = data.read()
		full_content_str = full_content.decode('utf-8')
		full_content_obj: dict = json.loads(full_content_str)
		status = full_content_obj['status']
		if status != 'ok':
			raise Exception('Unexpected status: ' + status)
		solution: dict = full_content_obj['solution']
		response: str = solution['response']
		content = response.encode('utf-8')
		assert_page_content(content)
		print('Page downloaded.')
		return content

def download_book_page(link: str, proxy_host: str):
	if proxy_host:
		return download_book_page_via_proxy(link, proxy_host)
	else:
		return download_book_page_direct(link)

def wait_for_delay(delay: int):
	print("Waiting %s sec..." % delay)
	time.sleep(delay)

# Page loader to download book pages to cache
class PageLoader:
	def __init__(this, cache: CacheManager, min_delay: int, max_delay: int, proxy_host: str):
		this.cache = cache
		this.min_delay = min_delay
		this.max_delay = max_delay
		this.proxy_host = proxy_host

	def try_download_book_page(this, book: Book):
		full_link = "https://livelib.ru/book/" + book.id
		print('Downloading book with id = "%s" from "%s"' % (book.id, full_link))
		if this.cache.is_cached(book.id):
			print('Already in cache, skipping.')
			return False
		else:
			page = download_book_page(full_link, this.proxy_host)
			this.cache.save(book.id, page)
			return True

	def download(this, books: list[Book]):
		count = 1
		total = len(books)
		if this.proxy_host:
			create_proxy_session(this.proxy_host)
		for book in books:
			print('%s/%s' % (count, total))
			count += 1
			if this.try_download_book_page(book):
				delay = random.randint(this.min_delay, this.max_delay)
				wait_for_delay(delay)
			print()
		if this.proxy_host:
			destroy_proxy_session(this.proxy_host)
