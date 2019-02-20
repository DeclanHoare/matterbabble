from setuptools import setup

with open("README.rst", "r") as f:
	long_description = f.read()

setup(name = "matterbabble",
	packages = ["matterbabble"],
	entry_points = {"console_scripts": ["matterbabble = matterbabble.__main__:main"]},
	version = "1.0.0",
	description = "Connect Discourse threads to Matterbridge.",
	long_description = long_description,
	author = "Declan Hoare",
	author_email = "declanhoare@exemail.com.au",
	url = "https://github.com/DeclanHoare/matterbabble",
	classifiers = ("Programming Language :: Python :: 3",
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: OS Independent"))

