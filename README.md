2jtl0-BvMCIgmpeaew1qY2ajiC3fKoZv

 r = requests.get("https://localhost:8080/rest/system/config", verify=False, headers={'X-API-Key': '2jtl0-BvMCIgmpeaew1qY2ajiC3fKoZv'})

r.status_code should = 200
r.json()

folders = list of dictionaries of:
u'pullers'
u'hashers'
u'scanProgressIntervalS'
u'disableSparseFiles'
u'rescanIntervalS'
u'copiers'
u'devices'
u'order'
u'minDiskFreePct'
u'pullerPauseS'
u'readOnly'
u'ignoreDelete'
u'invalid'
u'maxConflicts'
u'pullerSleepS'
u'path'
u'autoNormalize'
u'ignorePerms'
u'id'
u'versioning'


{
	"pullers": 0, 
	"hashers": 0, 
	"scanProgressIntervalS": 0, 
	"disableSparseFiles": false, 
	"rescanIntervalS": 60, "
	copiers": 0, 
	"devices": [
		{
			"deviceID": "KGKQKNT-3PAEO3H-R3F2EP3-64RJAWG-XTZXVVC-FZNVBZL-7KVCE4O-WCP3ZAO"
		},
		{
			"deviceID": "KH3MVFK-4WIX4EZ-QQNPSZT-VPEB2LJ-277JBVA-3OJVIU2-M5BAJFP-N2IX3QU"
		}, 
		{
			"deviceID": "3AHYUIG-GPYLPIG-IEFOJYW-WRVLOJG-KQK7AQP-W26VORW-WWBWBIA-CIPW2AJ"
		}
	], 
	"order": "random", 
	"minDiskFreePct": 1, 
	"pullerPauseS": 0, 
	"readOnly": false, 
	"ignoreDelete": false, 
	"invalid": "", 
	"maxConflicts": -1, 
	"pullerSleepS": 0, 
	"path": "/home/tim/pr/angel2015/media/", 
	"autoNormalize": true, 
	"ignorePerms": false, 
	"id": "angel2015-media", 
	"versioning": {
		"params": {}, 
		"type": ""
	}
}


We want to: 
Version 0, works just with local syncthing
Run script locally on each machine

* ask for project directory

* parse directory path into name + everything else

* Get config from server

* get available device names

* ask for device names to share (comma separated)

* create a library for the new folder

* append the library to the folders list

* create folder if it doesn't exist

* POST to localhost

Note: apparently POSTing doesn't work without the api key


<https://docs.syncthing.net/dev/rest.html>

<https://docs.python.org/3/library/json.html>

<http://docs.python-requests.org/en/master/user/quickstart/>

## pr_init

more comprehensive version of script, would include
- syncthing
- owncloud
- git/hg

Run locally on each workstation, providing relative or absolute directory

When creating a project:
- add project directory to nimloth if doesn't exist (ask version control if need be)
- clone project directory from nimloth
- add syncthing folders if they don't exist
- if they do, add current machine to nimloth, and share with other machines
- add out/ to owncloud if it doesn't exist
- sync out/ with owncloud

