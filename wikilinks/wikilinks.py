from runners import page_parser
from celery import Celery

app = Celery('wikilinks',
             include=['wikilinks.runners'])

def main():
	app.worker_main(argv=['worker', '-A', 'runners', '-l', 'info'])

	# page_parser.delay('http://en.wikipedia.org/wiki/P-wave')


if __name__ == '__main__':
	main()