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