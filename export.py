from book import Book
from read_parser import ReadParser
from csv_writer import CsvWriter
from details_parser import DetailsParser
from cache_manager import CacheManager
from page_loader import PageLoader
from rating_processor import RatingProcessor

import sys, getopt

# settings
input_file_name = 'read.html'
cache_dir_name = 'cache'
out_file_name = 'out.csv'
min_delay = 90
max_delay = 120

try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["convert-10-star-rating="])
except getopt.GetoptError:
	print('You can specify custom rating behaviour (defaults below):')
	print('test.py --convert-10-star-rating=True')

convert_10_star_rating = True
for opt, arg in opts:
	if opt == "--convert-10-star-rating":
		convert_10_star_rating = arg == "True"
print('Convert 10-star rating (defaults: True): %s' % convert_10_star_rating)

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

rating_processor = RatingProcessor()
should_convert_rating = convert_10_star_rating and rating_processor.is_applicable(ready_books)
if should_convert_rating:
	print('Change rating from 10-star to 5-star format with accuracy loss')
	rating_processor.change_rating(ready_books)

writer = CsvWriter()
writer.save(ready_books, out_file_name)
print('Books saved to "%s"' % out_file_name)