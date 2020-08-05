# -*- coding: UTF-8 -*-
#Copyright (C) 2009 - 2019 David CM, released under the GPL.
# Author: David CM <dhf360@gmail.com> and others.
# note: this file doesn't get settings from the base profile to avoid issues when updating from older versions.

from synthDrivers import _settingsDB
import config, gui, os, wx, addonHandler
addonHandler.initTranslation()

msg=""
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'synthDrivers', config.conf['ibmeci']['TTSPath'], config.conf['ibmeci']['dllName'])):
	# Translators: the message  shown if the driver can't find libraries during installation.
	msg = _("""The synthesizer won't be available until you set   IBMTTS files. NVDA won't show this synthesizer in teh synthesizers lists because you need to set the IBMTTS files location first.
	To do it open the NVDA settings dialog, select IBMTTS category and use the "Browse for  IBMTTS library" button to select the IBMTTS files folder.\n""")

# Translators: message box when user is installing the addon in NVDA. 
#msg += _("""if you are using another copy of IBMTTS or similar with a different name, you should not load this driver in the same NVDA session. If you do it, NVDA will fail.
#To resolve it switch to another synthesizer (E.G espeak) then restart NVDA. Afther that, you can use this new driver.""")

def onInstall():
	if msg!="":
		gui.messageBox(msg,
			# Translators: title of message box when user is installing NVDA
			_("IBMTTS driver for NVDA"), wx.OK)
