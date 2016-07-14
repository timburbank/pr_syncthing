pr_syncthing
============

Script I use for automatically setting up [Synchting](https://syncthing.net/) folders for projects.

`config.ini` sets the directories to create, as well as the Syncthing URL and API key for the machine. Copy `config.ini.example` as `config.ini` and make appropriate changes.

Runs on Python 2 or 3, with Windows or *nix systems.

Use
---

From project directory, run `python pr_syncthing.py add`

### Optional Paramenters

`-f``--folder` Base directory instead of using current working directory
`-d``--devices` Devices to share with,\ instead of prompting you for them
`-k``--apikey` API key instead of using `config.ini`
`-u``--url` Provide Syncthing URL instead of using `config.ini`
