# uploads.py - Discourse only sends the real addresses of some embedded
# images in the 'cooked' HTML.  This module helps to extract them from
# there and turn them into real links in the Markdown.

import html.parser
import io

import commonmark
import commonmark_extensions.plaintext

class html_image_ripper(html.parser.HTMLParser):
	def __init__(self):
		super().__init__()
		self.images = []
	
	def handle_starttag(self, tag, attrs):
		if tag == "img" and ("class", "emoji") not in attrs:
			self.images.append(dict(attrs)["src"])

def replace_images(msg, addr):
	parser = commonmark.Parser()
	ast = parser.parse(msg["data"]["raw"])
	ripper = html_image_ripper()
	ripper.feed(msg["data"]["cooked"])
	for cur, entering in ast.walker():
		if cur.t == "image" and entering:
			cur.t = "link"
			dest = ripper.images.pop(0)
			if dest.startswith("/"):
				dest = addr + dest
			cur.destination = dest
	renderer = commonmark_extensions.plaintext.CommonMarkToCommonMarkRenderer()
	return renderer.render(ast)

