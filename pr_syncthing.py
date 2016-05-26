#!/bin/python

import requests
import os
import json

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
		 request_data = requests.get( \
			"http://{}/rest/system/config".format(args.url))
	else:
		request_data = requests.get( \
			"http://{}/rest/system/config".format(args.url), \
			verify=False, \
			headers={'X-API-Key': args.apikey})
	print(request_data)
	syncthing = request_data.json()

	# ask for any parameters that weren't given
	if args.folder is None:
		folder = input("project directory: ")
	else:
		folder = args.folder
	folder = folder.strip()

	project_name = folder.split('/')[-1].strip()
	
	if args.devices is None:
		print("Enter devices to share with (comma separated)")
		devices_display = ''
		for device in syncthing['devices']:
			devices_display = "{}, {}".format(devices_display, device['name'])
		print devices_display.strip(', ')
		devices_input = input("devices: ").split(',')
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
	
		shared_devices = []
		# get device IDs
		for device_name in devices:
			for avail_device in syncthing['devices']:
				if avail_device['name'] == device_name:
					shared_devices.append({'deviceID': avail_device['deviceID']})
				
		new_folder['devices'] = shared_devices

		syncthing['folders'].append(new_folder)
	
		
	# send new config to syncthing
	
	# TODO: remove option to not have api key, cause I don't think it works
	if args.apikey is None:
		 response = requests.post( \
			"http://{}/rest/system/config".format(args.url), 
			data = json.dumps(syncthing))
	else:
		response = requests.post( \
			"http://{}/rest/system/config".format(args.url), \
			verify=False, \
			headers={'X-API-Key': args.apikey}, \
			data = json.dumps(syncthing))
		
	print response
	print response.text
	
	
	
	
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()

	subparsers = parser.add_subparsers()

	add_p = subparsers.add_parser('add')
	add_p.add_argument('-f', '--folder')
	add_p.add_argument('-d', '--devices', nargs='+')
	add_p.add_argument('-k', '--apikey')
	add_p.add_argument('-u', '--url', default='localhost:8384', nargs='?') 
	add_p.set_defaults(func=add_project)

	args = parser.parse_args()
	args.func(args)
