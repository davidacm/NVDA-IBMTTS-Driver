# -*- coding: UTF-8 -*-
#Copyright (C) 2009 - 2019 David CM, released under the GPL.
# Author: David CM <dhf360@gmail.com> and others.
#synthDrivers/settingsDB.py

import config
# Add-on config database
confspec = {
	"dllName": "string(default='eci.dll')",
	"TTSPath": "string(default='ibmtts')"
}
config.conf.spec["ibmeci"]=confspec

def setConfig():
	d=config.conf['ibmeci'].dict()
	if 'ibmeci' not in config.conf.profiles[0]: config.conf.profiles[0]['ibmeci'] = d
	if 'TTSPath' not in config.conf.profiles[0]['ibmeci']: config.conf.profiles[0]['ibmeci']['TTSPath'] = d['TTSPath']
	if 'dllName' not in config.conf.profiles[0]['ibmeci']: config.conf.profiles[0]['ibmeci']['dllName'] = d['dllName']
setConfig()
