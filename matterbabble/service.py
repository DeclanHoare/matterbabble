# Matterbabble
# Copyright 2019 Declan Hoare
# service.py - a few things redundant between Discourse and MB conn.s

import logging

from . import consts

class service:
	def __init__(self, app, address, token = None, *args, **kwargs):
		self.app = app
		self.addr = address.rstrip("/")
		self.token = token
		self.logger = logging.getLogger(f"{consts.product_name}/{type(self).__name__}")
		self.init(*args, **kwargs)
	
	def init(self):
		"""Optional extra constructor"""
	
	async def send(self, msg):
		"""Send msg (Matterbridge formatted dict) to the platform."""
		raise NotImplementedError()
	
	async def watch(self):
		"""Connect to the platform and listen for messages.  This is looped forever."""
		raise NotImplementedError()

