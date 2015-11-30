from HTMLParser import HTMLParser

import re


class WLParser(HTMLParser):
	is_href = False
	is_body = False
	is_bodyContent = False

	links = set()
	def handle_starttag(self, tag, attrs):
		# print 'start tag: ', tag
		if tag == 'body':
			self.is_body = True
		if self.is_body:
			for attr in attrs:
				if attr[1] == 'bodyContent':
					self.is_bodyContent = True
					
				if (attr[0] == 'href') or (self.is_bodyContent):
					self.is_href = True
					link = attr[1]
					m = re.search('\A/wiki/[^\A(Wikipedia:|Special:|Help:|Category:|Talk:|Portal:|File:|Main_Page)]', link)

					if m:
						self.links.add(link.replace('/wiki/', '', 1))
						pass

	def handle_endtag(self, tag):
		if tag == 'body':
			# print 'End of body'
			# print self.links
			self.is_body = False

		if self.is_bodyContent:
			self.is_bodyContent = False

		if self.is_href:
			# print 'tag ended: ', tag
			self.is_href = False
