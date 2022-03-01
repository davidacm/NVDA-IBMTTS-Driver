# -*- coding: UTF-8 -*-
#Copyright (C) 2009 - 2019 David CM, released under the GPL.
# Author: David CM <dhf360@gmail.com> and others.
#globalPlugins/ibmtts.py

import os, wx, winUser
from os import path
from ctypes import windll
import config, globalVars, gui, globalPluginHandler, addonHandler
from synthDrivers import _settingsDB
from logHandler import log
from gui import SettingsPanel
addonHandler.initTranslation()

class IBMTTSSettingsPanel(SettingsPanel):
	# Translators: This is the label for the IBMTTS settings category in NVDA Settings screen.
	title = _("IBMTTS")

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
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
		self._setValues()

	def _setValues(self):
		self._ttsPath.SetValue(config.conf.profiles[0]['ibmeci']['TTSPath'])
		self._dllName.SetValue(config.conf.profiles[0]['ibmeci']['dllName'])

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
				# Translators: The message displayed when the IBMTTS files folder and library name have  been set.
				gui.messageBox(_('The IBMTTS files location has been set. If you want  to use it with a portable version of NVDA, please use the "Copy IBMTTS files into driver add-on" button'),
					# Translators: The title displayed when the IBMTTS files folder and library name have been set.
					_("Success"),wx.OK|wx.ICON_INFORMATION,self)
				break
			except:
				# Translators: The message displayed in the dialog that inform you the specified library is invalid.
				if gui.messageBox(_("The specified dll file seems to be an incorrect IBMTTS library. Would you like to select another library?"),
				_("Error loading library"),
				style=wx.YES | wx.NO | wx.CENTER | wx.ICON_ERROR) == wx.NO: break

	def _onSetLocalClick(self, evt):
		# Translators: The message displayed when the current source path is relative.
		if  not path.isabs(self._ttsPath.GetValue()):
			# Translators: The message displayed when the current source path is relative.
			gui.messageBox(_("Relative paths are not allowed."), _("Error"), wx.OK|wx.ICON_ERROR, self)
			return
		# Translators: A message to ask the user to copy IBMTTS files to Add-on folder.
		if gui.messageBox(_('''Are you sure to copy IBMTTS files to local NVDA installation and register a new add-on called "eciLibraries" to store the libraries? It may not work in some IBMTTS distributions.
		Note: after it, if you want to uninstall this add-on, you'll need to uninstall two add-ons in order to  delete IBMTTS files completelly from NVDA. This one and "eciLibraries"'''),
			# Translators: The title of the Asking dialog displayed when trying to copy IBMTTS files.
			_("Copy IBMTTS files"),
			wx.YES|wx.NO|wx.ICON_QUESTION, self) == wx.YES:
			progressDialog = gui.IndeterminateProgressDialog(gui.mainFrame,
				# Translators: The title of the dialog presented while IBMTTS files  are being copied.
				_("Copying files"),
				# Translators: The message displayed while IBMTTS files are being copied.
				_("Please wait while IBMTTS files  are copied into add-on."))
			while True:
				try:
					gui.ExecAndPump(self.copyTtsFiles)
					res = True
					break
				except Exception:
					# Translators: a message dialog asking to retry or cancel when copying IBMTTS files.
					message=_("Unable to copy a file. Perhaps it is currently being used by another process or you have run out of disc space on the drive you are copying to.")
					# Translators: the title of a retry cancel dialog when copying IBMTTS files.
					title=_("Error Copying")
					if winUser.MessageBox(None,message,title,winUser.MB_RETRYCANCEL) != winUser.IDRETRY:
						res=False
						log.debugWarning("Error when copying IBMTTS files into Add-on",exc_info=True)
						break
			progressDialog.done()
			del progressDialog
			if res:
				self._ttsPath.SetValue(r"..\..\eciLibraries")
				# this parameter is saved even if the user doesn't click accept button.
				config.conf.profiles[0]['ibmeci']['TTSPath'] = self._ttsPath.GetValue()
				# Translators: The message displayed when copying IBMTTS files to Add-on was successful.
				gui.messageBox(_("Successfully copied IBMTTS files. The local copy will be used after restart NVDA."),
					# Translators: The title  displayed when copying IBMTTS files to Add-on was successful.
					_("Success"),wx.OK|wx.ICON_INFORMATION,self)
			else:
				# Translators: The message displayed when errors were found while trying to copy IBMTTS files to Add-on.
				gui.messageBox(_("Error copying IBMTTS files"), _("Error"), wx.OK|wx.ICON_ERROR, self)

	def copyTtsFiles(self):
		import installer
		fp = self._ttsPath.GetValue()
		tp = path.abspath(path.join(path.abspath(path.dirname(__file__)), r"..\..\eciLibraries"))
		for curSourceDir,subDirs,files in os.walk(fp):
			if curSourceDir == fp: curDestDir=tp
			else:
				curDestDir=path.join(tp,path.relpath(curSourceDir,fp))
			if not path.isdir(curDestDir): os.makedirs(curDestDir)
			for f in files:
				sourceFilePath=path.join(curSourceDir,f)
				destFilePath=path.join(curDestDir,f)
				installer.tryCopyFile(sourceFilePath,destFilePath)
		# Create a manifest, so NVDA recognizes the folder as an add-on
		with open(path.join(tp, "manifest.ini"), "w") as f:
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
		config.conf.profiles[0]['ibmeci']['dllName'] = self._dllName.GetValue()
		config.conf.profiles[0]['ibmeci']['TTSPath'] = self._ttsPath.GetValue()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		if not globalVars.appArgs.secure:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(IBMTTSSettingsPanel)

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		if not globalVars.appArgs.secure:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(IBMTTSSettingsPanel)
