============
Matterbabble
============

Matterbabble is an API client for Discourse_ and Matterbridge_.  It
mirrors Discourse posts in a thread to Matterbridge messages on a
gateway, and vice versa.  It works well with the `Discourse Babble`_
plugin, which formats a thread as a chat room.

.. _Discourse: https://discourse.org/
.. _Matterbridge: https://github.com/42wim/matterbridge
.. _Discourse Babble: https://discourse-babble.com/

Installation and Usage
----------------------

To install, execute::

	pip install matterbabble

To run, execute::

	python -m matterbabble CONFIGPATH

providing the path to a Matterbabble configuration file as described
below.

Configuration
-------------

Matterbabble is configured with a ``configparser`` INI file.

Example::

	[discourse]
	address = https://forum.bitphoenixsoftware.com/
	username = matterbridge
	token = 0dwdmaddzludwvntpg7gss6dxdem7byemre3krw86k60n39vn1ni7wganakpzjd0
	fmt = {username}: {message}

	[matterbridge]
	address = http://127.0.0.1:4242/
	token = oTUaGHctYYve28nYNMzLZszJvT1RD3kXLlZwPLULEaTFMRrGyvFzdvOdpsuQYFEhD84qL9PP5FJvGFOsQINESs1keaLO8SnvQNHHM6wq41mwHVX0NNKaBXD5uDaDhZ4p

	[connections]
	lounge = /babble/topics/68

	[logging]
	level = INFO

discourse
~~~~~~~~~

The ``discourse`` section must contain an address and API key for a
Discourse forum, and the username of the user you want the client to run
as.  You can also change the format used for the messages going TO
Discourse (the ``fmt`` key is optional).

matterbridge
~~~~~~~~~~~~

The ``matterbridge`` section must contain the ``BindAddress`` of a
`Matterbridge API`_ instance.  If you added a ``Token`` to the API,
you must also include that here.

connections
~~~~~~~~~~~

The ``connections`` section maps Matterbridge gateways to Discourse
threads.  The ID of a thread is the last component of the URL after you
navigate to it on Discourse, and the correct format is ``/topics/{id}``.
You can find a Babble chat room's ID by clicking on it in the admin
chat manager.  The format for those is ``/babble/topics/{id}``.

logging
~~~~~~~

The optional ``logging`` section can contain ``basicConfig`` options
for ``logging`` in Matterbabble.  You can set ``level`` to ``INFO`` to
log raw objects sent through Matterbabble to ``stderr``.

.. _Matterbridge API: https://github.com/42wim/matterbridge/wiki/Api

Caveat Emptor
-------------

Inline images in the Discourse post are currently replaced with links
before being sent to the gateway because they generally aren't
supported by chat rooms.  Maybe there will be a better solution to this
problem in future.

Copyright
---------

Copyright 2019 Declan Hoare

Licensed under Apache License 2.0.
NO WARRANTY
