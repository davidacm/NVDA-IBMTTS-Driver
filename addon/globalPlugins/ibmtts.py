# -*- coding: UTF-8 -*-
#Copyright (C) 2009 - 2023 David CM, released under the GPL.
# Author: David CM <dhf360@gmail.com> and others.
#globalPlugins/ibmtts.py

import wx, winUser
from os import path, startfile
from ctypes import windll

import globalVars, gui, globalPluginHandler, addonHandler
from logHandler import log
from gui.settingsDialogs import SettingsPanel
from synthDrivers._settingsDB import appConfig
from ._ibmttsUtils import UpdateHandler, GithubService, guiCopiFiles, showDonationsDialog
addonHandler.initTranslation()

ADDON_NAME = "IBMTTS"
# github repo
USER = 'davidacm'
REPO = 'NVDA-IBMTTS-Driver'
updateHandler = UpdateHandler(ADDON_NAME, GithubService(USER, REPO))

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


class IBMTTSSettingsPanel(SettingsPanel):
	# Translators: This is the label for the IBMTTS settings category in NVDA Settings screen.
	title = _("IBMTTS")

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: label used to toggle the auto check update.
		self._autoCheck = sHelper.addItem(wx.CheckBox(
			self,
			label=_("&Automatically check for updates for IBMTTS")
		))
		# Translators: This is the button to check for new updates of the add-on.
		self.updateButton = sHelper.addItem (wx.Button (self, label = _("&Check for update")))
		self.updateButton.Bind(wx.EVT_BUTTON, self._onUpdateClick)
		# Translators: This is the label for the IBMTTS folder address.
		self._ttsPath  = sHelper.addLabeledControl(_("IBMTTS folder address"), wx.TextCtrl)
		# Translators: This is the label for the IBMTTS library name.
		self._dllName  = sHelper.addLabeledControl(_("IBMTTS library name (dll)"), wx.TextCtrl)
		# Translators: This is the button to explore and find for an IBMTTS library and files.
		self._browseButton = sHelper.addItem (wx.Button (self, label = _("&Browse for  IBMTTS library...")))
		self._browseButton.Bind(wx.EVT_BUTTON, self._onBrowseClick)
		# Translators: This is the button to copy external IBMTTS files into synth driver Add-on.
		self._setLocalButton = sHelper.addItem (wx.Button (self, label = _("&Copy IBMTTS files in an  add-on (may not work for some IBMTTS distributions)")))
		self._setLocalButton.Bind(wx.EVT_BUTTON, self._onSetLocalClick)
		self.donateButton = sHelper.addItem (wx.Button (self, label = _("&Support IBMTTS add-on")))
		self.donateButton.Bind(wx.EVT_BUTTON, lambda e: showDonationsDialog(self, ADDON_NAME, DONATE_METHODS))
		self._setValues()

	def _setValues(self):
		self._autoCheck.SetValue(appConfig.autoUpdate)
		self._ttsPath.SetValue(appConfig.TTSPath)
		self._dllName.SetValue(appConfig.dllName)

	def _onUpdateClick(self, evt):
		updateHandler.checkUpdate(True)

	def _onBrowseClick(self, evt):
		# Translators: The message displayed in the dialog that allows you to look for the IBMTTS library.
		p= 'c:'
		while True:
			fd = wx.FileDialog(self, message=_("Select the IBMTTS library (dll)"),
			# Translators: the label for the dynamic link library extension (dll) file type
			wildcard=(_("dynamic link library (*.{ext})")+"|*.{ext}").format(ext="dll"),
			defaultDir=path.dirname(p), style=wx.FD_OPEN)
			if not fd.ShowModal() == wx.ID_OK: break
			p = fd.GetPath()
			try:
				windll.LoadLibrary(p).eciVersion
				self._ttsPath.SetValue(path.dirname(p))
				self._dllName.SetValue(path.basename(p))
				gui.messageBox(
					# Translators: The message displayed when the IBMTTS files folder and library name have  been set.
					_('The IBMTTS files location has been set. If you want  to use it with a portable version of NVDA, please use the "Copy IBMTTS files into driver add-on" button'),
					# Translators: The title displayed when the IBMTTS files folder and library name have been set.
					_("Success"),wx.OK|wx.ICON_INFORMATION,self
				)
				break
			except:
				log.info("Error loading the IBMTTS library", exc_info=True)
				if gui.messageBox(
					# Translators: The message displayed in the dialog that inform you the specified library is invalid.
					_("The specified dll file seems to be an incorrect IBMTTS library. Would you like to select another library?"),
					_("Error loading library"),
					style=wx.YES | wx.NO | wx.CENTER | wx.ICON_ERROR
				) == wx.NO:
					break

	def _onSetLocalClick(self, evt):
		# Translators: A message to ask the user to copy IBMTTS files to Add-on folder.
		if gui.messageBox(
			_('''Are you sure to copy IBMTTS files to local NVDA installation and register a new add-on called "eciLibraries" to store the libraries? It may not work in some IBMTTS distributions.
		Note: after it, if you want to uninstall this add-on, you'll need to uninstall two add-ons in order to  delete IBMTTS files completelly from NVDA. This one and "eciLibraries"'''),
			# Translators: The title of the Asking dialog displayed when trying to copy IBMTTS files.
			_("Copy IBMTTS files"),
			wx.YES|wx.NO|wx.ICON_QUESTION, self
		) == wx.YES:
			src = self._ttsPath.GetValue()
			if src == "ibmtts":
				src = r"..\synthDrivers\ibmtts"
			if not path.isabs(src):
				src = path.abspath(path.join(path.abspath(path.dirname(__file__)), src))
			dest = path.abspath(path.join(path.abspath(path.dirname(__file__)), r"..\..\eciLibraries"))
			if src == dest:
				# Translators: The message displayed when copying IBMTTS files and the paths are the same.
				gui.messageBox(
					_("Unable to copy the files because the source and destination paths are the same."),
					# Translators: The title  displayed when copying IBMTTS files to Add-on was successful.
					_("Error"),
					wx.OK | wx.ICON_ERROR,
					self
				)
				return
			if guiCopiFiles(
				src,
				dest,
				# Translators: The title of the dialog presented while IBMTTS files  are being copied.
				_("Copying files"),
				# Translators: The message displayed while IBMTTS files are being copied.
				_("Please wait while IBMTTS files  are copied into add-on.")
			):
				self.createLibrariesManifest(dest)
				# this parameter is saved even if the user doesn't click accept button.
				appConfig.TTSPath = r"..\..\eciLibraries"
				self._ttsPath.SetValue(appConfig.TTSPath)
				# Translators: The message displayed when copying IBMTTS files to Add-on was successful.
				gui.messageBox(
					# Translators: The message displayed when copying IBMTTS files to Add-on was successful.
					_("Successfully copied IBMTTS files. The local copy will be used after restart NVDA."),
					# Translators: The title  displayed when copying IBMTTS files to Add-on was successful.
					_("Success"),
					wx.OK|wx.ICON_INFORMATION,
					self
				)
			else:
				# Translators: The message displayed when errors were found while trying to copy IBMTTS files to Add-on.
				gui.messageBox(_("Error copying IBMTTS files"), _("Error"), wx.OK|wx.ICON_ERROR, self)

	def createLibrariesManifest(self, dest):
		with open(path.join(dest, "manifest.ini"), "w") as f:
			f.write('''name = eciLibraries
summary = IBMTTS libraries
description = """You can put the libraries for IBMTTS driver here."""
author = NVDA User
version = 0.1
url = None
minimumNVDAVersion = 2012.1.1
lastTestedNVDAVersion = 2030.1.1
updateChannel = None''')

	def onSave(self):
		appConfig.autoUpdate = self._autoCheck.GetValue()
		updateHandler.isAutoUpdate = self._autoCheck.GetValue()
		appConfig.dllName = self._dllName.GetValue()
		appConfig.TTSPath = self._ttsPath.GetValue()
		updateHandler.updateTimer()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		if not globalVars.appArgs.secure:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(IBMTTSSettingsPanel)
			updateHandler.isAutoUpdate = appConfig.autoUpdate
			updateHandler.updateTimer()

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		if not globalVars.appArgs.secure:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(IBMTTSSettingsPanel)
