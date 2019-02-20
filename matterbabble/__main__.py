# Matterbabble
# Copyright 2019 Declan Hoare

import argparse
import asyncio
import configparser
import logging

from . import consts
from .application import application

def main():
	arg = argparse.ArgumentParser(description = consts.product_description)
	config = configparser.ConfigParser()
	arg.add_argument("config_path", help = consts.config_path_help)
	args = arg.parse_args()
	config.read(args.config_path)
	if "logging" in config:
		logging.basicConfig(**config["logging"])
	instance = application(config["discourse"], config["matterbridge"], config["connections"])
	asyncio.run(instance.run())

if __name__ == "__main__":
	main()

