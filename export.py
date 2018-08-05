from book import Book
from read_parser import ReadParser
from csv_writer import CsvWriter
from details_parser import DetailsParser
from cache_manager import CacheManager
from page_loader import PageLoader

# settings
input_file_name = 'read.html'
cache_dir_name = 'cache'
out_file_name = 'out.csv'
min_delay = 90
max_delay = 120

print('Load books from file: "%s"' % input_file_name)
read_parser = ReadParser()
if read_parser.load_from_file(input_file_name) is False:
	exit(1)
print('Books loaded.')

print('Parse books from summary.')
books = read_parser.parse_books()
print('Books parsed: %s.' % len(books))

print('Start download detailed book pages.')
cache = CacheManager(cache_dir_name)
loader = PageLoader(cache, min_delay, max_delay)
loader.download(books)
print('Detailed book pages downloaded.')

print('Prepare books for export.')
details_parser = DetailsParser(cache)
ready_books = details_parser.parse(books)
print('Books ready to export: %s.' % len(ready_books))

writer = CsvWriter()
writer.save(ready_books, out_file_name)
print('Books saved to "%s"' % out_file_name)