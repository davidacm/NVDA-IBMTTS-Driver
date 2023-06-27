# -*- coding: UTF-8 -*-
#Copyright (C) 2009 - 2019 David CM, released under the GPL.
# Author: David CM <dhf360@gmail.com> and others.
# note: this file doesn't get settings from the base profile to avoid issues when updating from older versions.
from logHandler import log
from synthDrivers._settingsDB import appConfig, DEFAULT_LIB_FOLDER
import globalVars, gui, os, shutil, wx, addonHandler
addonHandler.initTranslation()


def preserveFiles(addonName, folder):
	"""
	addonName: the name (identifier) of the addon
	folder: a path for a folder inside the addonName directory.
	"""
	absFolderPath = os.path.abspath(os.path.join(globalVars.appArgs.configPath, "addons", addonName, folder))
	tempFolder = os.path.abspath(os.path.join(globalVars.appArgs.configPath, "addons", addonName + addonHandler.ADDON_PENDINGINSTALL_SUFFIX, folder))
	if os.path.isdir(absFolderPath):
		if os.path.isdir(tempFolder):
			shutil.rmtree(tempFolder)
		os.rename(absFolderPath, tempFolder)

msg=""
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'synthDrivers', appConfig.TTSPath, appConfig.dllName)):
	# Translators: the message  shown if the driver can't find libraries during installation.
	msg = _("""The synthesizer won't be available until you set   IBMTTS files. NVDA won't show this synthesizer in teh synthesizers lists because you need to set the IBMTTS files location first.
	To do it open the NVDA settings dialog, select IBMTTS category and use the "Browse for  IBMTTS library" button to select the IBMTTS files folder.\n""")


def onInstall():
	try:
		preserveFiles("IBMTTS", fr"synthDrivers\{DEFAULT_LIB_FOLDER}")
	except:
		log.warning("error backing data", exc_info=True)
	if msg != "":
		gui.messageBox(msg,
			# Translators: title of message box when user is installing NVDA
			_("IBMTTS driver for NVDA"), wx.OK)
