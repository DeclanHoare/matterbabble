# Matterbabble
# Copyright 2019 Declan Hoare
# matterbridge.py - Matterbridge event watch

from .service import service

class matterbridge(service):
	def request(self, method, url, *args, headers = None, **kwargs):
		if headers is None:
			headers = {}
		if self.token is not None:
			headers["Authorization"] = f"Bearer {self.token}"
		url = self.addr + url
		return self.app.session.request(method, url, *args, headers = headers, **kwargs)
	
	async def send(self, msg):
		return await self.request("POST", "/api/message", data = msg)
	
	async def watch(self):
		async with self.request("GET", "/api/stream") as req:
			async for msg in self.app.jsonlines(req):
				self.logger.info(msg)
				if not msg["event"]: # This is a user message not a system event
					await self.app.discourse.send(msg)

