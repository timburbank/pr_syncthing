#!/bin/python

import requests

def input(prompt=''):
	from sys import version_info

	py3 = version_info[0] > 2
	if py3:
		content = input(prompt)
	else:
		content = raw_input(prompt)
	return(content)



# Adds in, out, and rnd directories for the project to syncthing
# and shares them with the specified devices
#
# Params:
# dir, string filepath of project (relative to pr/?)
# devices, list of device names
def add_project(args):

	# get config data
	if args.apikey is None:
		 syncthing_config = requests.get( \
			"http://{}/rest/system/config".format(args.url))
	else:
		syncthing_config = requests.get( \
			"http://{}/rest/system/config".format(args.url), \
			verify=False, \
			headers={'X-API-Key': args.apikey})

	print syncthing_config

	if args.folder is None:
		folder = input("project directory: ")
	else:
		folder = args.folder

	if args.devices is None:
		print("Enter devices to share with (comma separated)")
		devices_input = input("devices: ").split(',')
		# Assuming device names don't start or end with whitespace
		# If device names do start or end with whitespace then fuck you
		devices = [device_name.strip() for device_name in devices_input]
	else:
		devices = list(args.devices)
		
	project_name = folder.split('/')[-1].strip()
	print project_name
	print folder
	print devices[0]




if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()

	subparsers = parser.add_subparsers()

	add_p = subparsers.add_parser('add')
	add_p.add_argument('-f', '--folder')
	add_p.add_argument('-d', '--devices', nargs='+')
	add_p.add_argument('-k', '--apikey')
	add_p.add_argument('-u', '--url', default='localhost:8080', nargs='?') 
	add_p.set_defaults(func=add_project)

	args = parser.parse_args()
	args.func(args)
