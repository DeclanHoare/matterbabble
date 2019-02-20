# Matterbabble
# Copyright 2019 Declan Hoare
# discourse.py - Discourse event watch and type converter

import posixpath
import traceback
import uuid

from .images import replace_images
from .service import service

class discourse(service):
	def init(self, username, fmt = "{username}: {message}"):
		# The POST data lists which channels you want events on, and
		# the last message you got on each one.  -1 is used on start,
		# and replaced by the first event.  We only need to subscribe
		# to "posts".
		self.data = {posixpath.join(topic, "posts"): -1 for topic in self.app.connections.values()}
		
		# There is also this special key which numbers the requests
		# sequentially.
		self.data["__seq"] = 0
		
		# There needs to be a bus UUID shared among all the requests
		# from this instance but it's created on the client end.
		self.bus = f"/message-bus/{uuid.uuid4().hex}/poll"
		
		# I briefly had "uploads" here, but it doesn't send events
		# for what other people upload.
		self.handlers = {"posts": self.posts, "__status": self.status}
		
		self.fmt = fmt
		self.username = username
	
	def post(self, url, data):
		data["api_key"] = self.token
		data["api_username"] = self.username
		url = self.addr + url
		return self.app.session.post(url, data = data)
	
	async def messages(self, req):
		async for obj in self.app.jsonlines(req):
			for ev in obj:
				yield ev # can't use "yield from" and "async" together!
	
	# Handler for "posts" messages from Discourse
	async def posts(self, msg):
		if (msg["data"]["username"] == self.username # sent by the bot
				or "is_edit" in msg["data"]
				or "is_delete" in msg["data"]):
			return
		try:
			text = replace_images(msg, self.addr)
		except:
			self.logger.warning(traceback.format_exc())
			text = msg["data"]["raw"]
		await self.app.matterbridge.send({"text": text,
			"username": msg["data"]["username"],
			"userid": str(msg["data"]["user_id"]),
			"avatar": self.addr + msg["data"]["avatar_template"].format(size = 128),
			"gateway": self.app.connections.inverse[posixpath.dirname(msg["channel"])]})

	# Handler for "__status" messages from Discourse, which update
	# the state of the other subscribed channels
	async def status(self, msg):
		self.data.update(msg["data"])
	
	async def send(self, msg):
		raw = self.fmt.format(username = msg["username"], message = msg["text"])
		async with self.post(posixpath.join(self.app.connections[msg["gateway"]],
				"posts"), {"raw": raw}) as req:
			if req.status >= 400:
				self.logger.error(f"{req.status}\n{await req.text()}")
	
	async def watch(self):
		self.data["__seq"] += 1
		async with self.post(self.bus, self.data) as req:
			async for msg in self.messages(req):
				self.logger.info(msg)
				self.data[msg["channel"]] = msg["message_id"] # update last message
				kind = posixpath.basename(msg["channel"])
				if kind in self.handlers:
					await self.handlers[kind](msg)
				else:
					print(f"No handler for {kind}")

