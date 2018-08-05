import os
from os import path

# Operates with book pages cache
class CacheManager:
	def __init__(this, cache_dir):
		this.cache_dir = cache_dir
		this.ensure_cache_dir()

	def ensure_cache_dir(this):
		if not path.exists(this.cache_dir):
			os.mkdir(this.cache_dir)

	def get_path(this, id):
		return path.join(this.cache_dir, id + '.html')

	def is_cached(this, id):
		return path.exists(this.get_path(id))

	def save(this, id, content):
		file_name = this.get_path(id)
		with open(file_name, 'wb') as file:
			print('Save to cache: "%s"' % file_name)
			file.write(content)

	def load(this, id):
		file_name = this.get_path(id)
		try:
			with open(file_name, 'r') as file:
				return file.read()
		except Exception as ex:
			print('load_book_content_from_cache("%s"): %s' % (file_name, ex))
			return None

