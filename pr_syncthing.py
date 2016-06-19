#!/bin/python

import requests
import os
import json

# awkward system to get config parser for python 2 or 3
from sys import version_info
py3 = version_info[0] > 2
if py3:
	import configparser
else:
	import ConfigParser as configparser 

	
def terminal_input(prompt=''):
	from sys import version_info

	py3 = version_info[0] > 2
	if py3:
		content = input(prompt)
	else:
		content = raw_input(prompt)
	return(content)

# Read config file
def get_config(section, option):
	# TODO: Handles specific exceptions, so we can tell the difference
	#       between incorrect config file and no config file
	config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.ini')
	
	parser = configparser.SafeConfigParser()
	parser.read(config_file)	
	result = parser.get(section, option)
	
	return(result)

# Adds in, out, and rnd directories for the project to syncthing
# and shares them with the specified devices
#
# Params:
# dir, string filepath of project (relative to pr/?)
# devices, list of device names
def add_project(args):

	# get url and api key, either from command line, config, or ask
	config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.ini')
	
	if args.url is not None:
		url = args.url
	else:
		try:
			url = get_config('connection', 'url')
		except:
			url = terminal_input('url: ')
		
	if args.apikey is not None:
		api_key = args.apikey
	else:
		try:
			api_key = get_config('connection', 'api_key')
		except:
			api_key = terminal_input('api key: ')

	# get config data
	request_data = requests.get( \
		"http://{}/rest/system/config".format(url), \
		verify=False, \
		headers={'X-API-Key': api_key})
	print(request_data)
	syncthing = request_data.json()

	# ask for any parameters that weren't given
	if args.folder is None:
		folder = os.getcwd()
	else:
		folder = args.folder
	folder = folder.strip()
	project_name = os.path.basename(folder)
	
	if args.devices is None:
		print("Enter devices to share with (comma separated)")
		devices_display = ''
		for device in syncthing['devices']:
			devices_display = "{}, {}".format(devices_display, device['name'])
		print(devices_display.strip(', '))
		devices_input = terminal_input("devices: ").split(',')
		# Assuming device names don't start or end with whitespace
		# If device names do start or end with whitespace then fuck you
		devices = [device_name.strip() for device_name in devices_input]
	else:
		devices = list(args.devices)
		
			
	# generic folder configs
	generic_folder = {
		'pullers': 0,
		'hashers': 0,
		'scanProgressIntervalS': 0,
		'disableSparseFiles': False,
		'rescanIntervalS': 60,
		'copiers': 0,
		'order': 'random',
		'minDiskFreePct': 1,
		'pullerPauseS': 0,
		'readOnly': False,
		'ignoreDelete': False,
		'invalid': '',
		'maxConflicts': -1,
		'pullerSleepS': 0,
		'autoNormalize': True,
		'ignorePerms': False,
		'versioning': {'params': {}, 'type': ''}
	}

	# create folder (project directory needs to already exist)
	# if we want it to not have to <http://stackoverflow.com/a/18503387>
	
	directorys = ['in', 'out', 'rnd']
	
	for directory in directorys:
	
		filepath = os.path.join(folder, directory)
		if not os.path.exists(filepath):
			os.mkdir(filepath)
	
		new_folder = generic_folder.copy()
		new_folder['path'] = filepath
		new_folder['id'] = '{}-{}'.format(project_name, directory)
		print(new_folder['id'])
	
		shared_devices = []
		# get device IDs
		for device_name in devices:
			for avail_device in syncthing['devices']:
				if avail_device['name'] == device_name:
					shared_devices.append({'deviceID': avail_device['deviceID']})
				
		new_folder['devices'] = shared_devices

		syncthing['folders'].append(new_folder)
	
		
	# send new config to syncthing
	print("send new config to syncthing")
	# TODO: remove option to not have api key, cause I don't think it works
	response = requests.post( \
		"http://{}/rest/system/config".format(url), \
		verify=False, \
		headers={'X-API-Key': api_key}, \
		data = json.dumps(syncthing))

	print(response)
	print(response.text)
	
	
	
	
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()

	subparsers = parser.add_subparsers()

	add_p = subparsers.add_parser('add')
	add_p.add_argument('-f', '--folder')
	add_p.add_argument('-d', '--devices', nargs='+')
	add_p.add_argument('-k', '--apikey', nargs='?')
	add_p.add_argument('-u', '--url', nargs='?') 
	add_p.set_defaults(func=add_project)

	args = parser.parse_args()
	args.func(args)
