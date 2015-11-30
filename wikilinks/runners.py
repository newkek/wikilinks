from celery import Celery
from parser import WLParser
from celery.task.sets import subtask

import requests

from celery.signals import celeryd_after_setup

app = Celery('runners', broker='amqp://guest@localhost//')

@app.task
def page_parser(url, depth=0):
	print 'Task {0} starts parsing : {1}'.format(depth, url)
	parser = WLParser()
	r = requests.get(url)
	page = r.text
	parser.feed(page)
	print 'Task {0}: {1} links found'.format(depth, len(parser.links))

	if (depth < 3):
		subtask(page_parser).delay(url, depth+1)

@celeryd_after_setup.connect
def start_first_task(sender, instance, **kwargs):
	print 'Received signal after setup'
	subtask(page_parser).delay('http://en.wikipedia.org/wiki/P-wave')