# -*- coding: UTF-8 -*-
#Copyright (C) 2009 - 2019 David CM, released under the GPL.
#synthDrivers/_ibmeci.py

import os, wx, winUser
from os import path
from ctypes import windll
import config, gui, globalPluginHandler, addonHandler
from synthDrivers import settingsDB
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
		self._setLocalButton = sHelper.addItem (wx.Button (self, label = _("&Copy IBMTTS files into driver add-on (may not work for some IBMTTS distributions)")))
		self._setLocalButton.Bind(wx.EVT_BUTTON, self._onSetLocalClick)
		self._setValues()

	def _setValues(self):
		self._ttsPath.SetValue(config.conf['ibmeci']['TTSPath'])
		self._dllName.SetValue(config.conf['ibmeci']['dllName'])

	def _onBrowseClick(self, evt):
		# Translators: The message displayed in the dialog that allows you to look for the IBMTTS library.
		fd = wx.FileDialog(self, message=_("Select the IBMTTS library (dll)"),
		# Translators: the label for the dynamic link library extension (dll) file type
		wildcard=(_("dynamic link library (*.{ext})")+"|*.{ext}").format(ext="dll"),
		defaultDir="c:", style=wx.FD_OPEN)
		if fd.ShowModal() == wx.ID_OK:
			p = fd.GetPath()
			try:
				windll.LoadLibrary(p).eciVersion
				self._ttsPath.SetValue(path.dirname(p))
				self._dllName.SetValue(path.basename(p))
			except:
				# Translators: The message displayed in the dialog that inform you the specified library is invalid.
				gui.messageBox(_("The specified dll file seems to be an incorrect IBMTTS library"),
				_("Error loading library"),
				style=wx.OK | wx.CENTER | wx.ICON_ERROR)

	def _onSetLocalClick(self, evt):
		# Translators: The message displayed when the current source path is relative.
		if  not path.isabs(self._ttsPath.GetValue()):
			# Translators: The message displayed when the current source path is relative.
			gui.messageBox(_("Relative paths are not allowed."), _("Error"), wx.OK|wx.ICON_ERROR, self)
			return
		# Translators: A message to ask the user to copy IBMTTS fails to Add-on folder.
		if gui.messageBox(_("Are you sure to copy IBMTTS files to local NVDA driver Add-on? It may not work in some IBMTTS distributions."),
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
					# Translators: a message dialog asking to retry or cancel when copying IBMTTS fails.
					message=_("Unable to copy a file. Perhaps it is currently being used by another process or you have run out of disc space on the drive you are copying to.")
					# Translators: the title of a retry cancel dialog when copying IBMTTS fails
					title=_("Error Copying")
					if winUser.MessageBox(None,message,title,winUser.MB_RETRYCANCEL) != winUser.IDRETRY:
						res=False
						log.debugWarning("Error when copying IBMTTS files into Add-on",exc_info=True)
						break
			progressDialog.done()
			del progressDialog
			if res:
				self._ttsPath.SetValue("ibmtts")
				# this parameter is saved even if the user doesn't click accept button.
				config.conf['ibmeci']['TTSPath'] = self._ttsPath.GetValue()
				# Translators: The message displayed when copying IBMTTS fails to Add-on was successful.
				gui.messageBox(_("Successfully copied IBMTTS fails. The local copy will be used after restart NVDA."),
					# Translators: The title  displayed when copying IBMTTS fails to Add-on was successful.
					_("Success"),wx.OK|wx.ICON_INFORMATION,self)
			else:
				# Translators: The message displayed when errors were found while trying to copy IBMTTS files to Add-on.
				gui.messageBox(_("Error copying IBMTTS fails"), _("Error"), wx.OK|wx.ICON_ERROR, self)

	def copyTtsFiles(self):
		import installer
		fp = self._ttsPath.GetValue()
		tp = path.join(path.abspath(path.join(path.dirname(path.abspath(__file__)), "..")), r"synthDrivers\ibmtts")
		for curSourceDir,subDirs,files in os.walk(fp):
			if curSourceDir == fp: curDestDir=tp
			else:
				curDestDir=path.join(tp,path.relpath(curSourceDir,fp))
			if not path.isdir(curDestDir): os.makedirs(curDestDir)
			for f in files:
				sourceFilePath=path.join(curSourceDir,f)
				destFilePath=path.join(curDestDir,f)
				installer.tryCopyFile(sourceFilePath,destFilePath)

	def onSave(self):
		config.conf['ibmeci']['dllName'] = self._dllName.GetValue()
		config.conf['ibmeci']['TTSPath'] = self._ttsPath.GetValue()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(IBMTTSSettingsPanel)
