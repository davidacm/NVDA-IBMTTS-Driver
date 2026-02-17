# -*- coding: UTF-8 -*-
#Copyright (C) 2009 - 2019 David CM, released under the GPL.
# Author: David CM <dhf360@gmail.com> and others.
#synthDrivers/settingsDB.py

try:
	import addonHandler
	addonHandler.initTranslation()
except ImportError:
	pass  # addonHandler may not be available in synthDriverHost32

from ._configHelper64 import configSpec, registerConfig, boolValidator

# Add-on config database
@configSpec("ibmeci")
class _AppConfig:
	dllName = ("string(default='eci.dll')", True)
	TTSPath = ("string(default='ibmtts')", True)  # Default to 'ibmtts' like backup
	autoUpdate  = ('boolean(default=True)', True, boolValidator)
appConfig = registerConfig(_AppConfig)

@configSpec("speech")
class _SpeechConfig:
	ibmtts = ""
	outputDevice = ""
speechConfig = _SpeechConfig()
