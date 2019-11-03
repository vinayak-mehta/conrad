import csv
import datetime
import dateparser
import dateparser.search
import requests
from bs4 import BeautifulSoup

URL = 'https://www.papercall.io/events?open-cfps=true&page={page}'

def get(page):
	res = requests.get(URL.format(page=page))
	return BeautifulSoup(res.text, 'html.parser')


def maybe_int(s):
	try:
		return int(s)
	except ValueError:
		return 0


def num_pages():
	pagination = get(1).find(class_='pagination')
	return max(maybe_int(elm.string) for elm in pagination.find_all('a'))


def parse_page(root):
	for event in root.select('.event-list-detail'):
		title_line = event.select('.event__title a')[-1]
		title_parts = title_line.string.split(' - ', 1)
		if len(title_parts) == 1:
			title = title_parts[0]
			location = ''
		elif len(title_parts) == 2:
			title = title_parts[0]
			location = title_parts[1]
		try:
			url = event.select('.fa-external-link')[0]['title']
		except IndexError:
			url = ''
		cfp_close_label = event.find(lambda elm: elm.name == 'strong' and 'CFP closes at' in elm.string)
		if not cfp_close_label:
			# No real point.
			continue
		cfp_close = dateparser.parse(cfp_close_label.parent.find_next_sibling('td').string.strip())
		start_date = end_date = None
		dates = event.find(lambda elm: elm.name == 'strong' and 'Event Dates' in elm.string)
		if dates:
			dates = dates.next_sibling.string.strip()
		if dates:
			parsed_dates = [d for _, d in dateparser.search.search_dates(dates)]
			if parsed_dates:
				start_date = parsed_dates[0].date()
				end_date = parsed_dates[-1].date()
		tags = [t.string for t in event.select('a[href^="/events?keywords=tags"]')]		
		conrad = {}
		"""
		Conrad Format
		"""
		conrad["cfp_end_date"]= cfp_close.strftime("%Y-%m-%d")
		today = datetime.datetime.now().replace(tzinfo=None)
		if cfp_close > cfp_close:
			conrad["cfp_open"] = False
		else:
			conrad["cfp_open"] = True
		conrad["cfp_start_date"] = "2019-10-01"
		conrad["city"]= location.split(',')[0]
		conrad["country"] = location.split(',')[1]
		conrad["end_date"]=end_date.strftime("%Y-%m-%d")
		conrad["kind"]= "conference"
		conrad["name"]= title
		conrad["source"]= "http://papercall.io"
		conrad["start_date"] = start_date.strftime("%Y-%m-%d")
		conrad["state"]= ""
		conrad["tags"]= tags
		conrad["url"] = url

		yield conrad


def parse_all():
	count = num_pages()
	for n in range(count):
		yield from parse_page(get(n+1))


if __name__ == '__main__':
	import pprint
	"""
	Just Print out one conf to check the format
	"""
	count =0
	for event in parse_all():
		pprint.pprint(event)
		count+=1
		if count == 2:
			break
