# Matterbabble
# Copyright 2019 Declan Hoare
# application.py - starts and loops service conn.s

import asyncio
import json

import aiohttp
import bidict

from . import consts
from .discourse import discourse
from .matterbridge import matterbridge

# That's Right.  It's Object Oriented.
class application:
	def __init__(self, discourse_cfg, matterbridge_cfg, connections):
		self.connections = bidict.bidict(connections)
		self.discourse = discourse(self, **discourse_cfg)
		self.matterbridge = matterbridge(self, **matterbridge_cfg)
		self.services = [self.discourse, self.matterbridge]
		self.running = False
	
	async def loop(self, service):
		while self.running:
			await service.watch()
	
	async def run(self):
		self.running = True
		async with aiohttp.ClientSession(headers = {"User-Agent": consts.user_agent}) as session:
			self.session = session
			await asyncio.wait(map(self.loop, self.services))
	
	def shutdown(self):
		self.running = False
	
	async def jsonlines(self, req):
		async for raw in req.content: # iterate over lines
			line = raw.decode()
			if line.strip() == "|": # placed between objects by Discourse
				continue
			yield json.loads(line)

