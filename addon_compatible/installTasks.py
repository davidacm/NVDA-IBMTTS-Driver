# -*- coding: UTF-8 -*-
#Copyright (C) 2009 - 2019 David CM, released under the GPL.
# Author: David CM <dhf360@gmail.com> and others.

# note: this file doesn't get settings from the base profile to avoid issues when updating from older versions.

from logHandler import log

import config, globalVars, gui, os, shutil, sys, wx, addonHandler

addonDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "globalPlugins"))
sys.path.append(addonDir)
from _ibmttsUtils import showDonationsDialog
sys.path.remove(sys.path[-1])

addonHandler.initTranslation()


DONATE_METHODS = (
	{
		'label': _('Using Paypal'),
		'url': 'https://paypal.me/davicm'
	},
	{
		'label': _('using Co-fi'),
		'url': 'https://ko-fi.com/davidacm'
	},
	{
		'label': _('See more methods on my github Page'),
		'url': 'https://davidacm.github.io/donations/'
	}
)

def buildAddonAbsPath(addonName):
	return os.path.abspath(os.path.join(globalVars.appArgs.configPath, "addons", addonName))


def preserveFiles(addonName, folder):
	"""
	addonName: the unique identifier of the add-on
	folder: a path for a folder inside the addonName directory where the files must be preserved.
	"""
	print(os.path.dirname(__file__))
	absFolderPath = os.path.join(buildAddonAbsPath(addonName), folder)
	tempFolder = os.path.join(buildAddonAbsPath(addonName) + addonHandler.ADDON_PENDINGINSTALL_SUFFIX, folder)
	if os.path.isdir(absFolderPath):
		if os.path.isdir(tempFolder):
			shutil.rmtree(tempFolder)
		os.rename(absFolderPath, tempFolder)


try:
	TTSPath = config.conf['ibmeci']['TTSPath']
	dllName = config.conf['ibmeci']['dllName']
except:
	TTSPath = "ibmtts"
	dllName = "eci.dll"


def onInstall():
	gui.mainFrame.prePopup()
	wx.CallAfter(showDonationsDialog, gui.mainFrame, "IBMTTS", DONATE_METHODS)
	gui.mainFrame.postPopup()
	try:
		preserveFiles("ibmtts", r"synthDrivers\ibmtts")
	except:
		log.warning("error backing data", exc_info=True)

	if not os.path.exists(os.path.join(os.path.dirname(__file__), 'synthDrivers', TTSPath, dllName)):
		# Translators: the message  shown if the driver can't find libraries during installation.
		msg = _("""The synthesizer won't be available until you set   IBMTTS files. NVDA won't show this synthesizer in teh synthesizers lists because you need to set the IBMTTS files location first.
	To do it open the NVDA settings dialog, select IBMTTS category and use the "Browse for  IBMTTS library" button to select the IBMTTS files folder.\n""")
		gui.messageBox(
			msg,
			# Translators: title of message box when user is installing NVDA
			_("IBMTTS driver for NVDA"), wx.OK
		)
