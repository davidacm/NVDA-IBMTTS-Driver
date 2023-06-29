# -*- coding: UTF-8 -*-
#Copyright (C) 2009 - 2023 David CM, released under the GPL.
# Author: David CM <dhf360@gmail.com> and others.
#globalPlugins/_ibmttsutils.py

import addonAPIVersion, config, json, os, pickle, ssl, time, winUser, wx, zipfile
from os import path
from ctypes import windll
from urllib.request import urlopen

import globalVars, gui, addonHandler
from core import callLater
from logHandler import log
from gui.addonGui import promptUserForRestart

addonHandler.initTranslation()


def loadPickle(fileName):
	with open(fileName, "rb") as f:
		return pickle.load(f)


def savePickle(fileName, obj):
	with open(fileName, "wb") as f:
		pickle.dump(obj, f, 4)


#: The download block size in bytes.
DOWNLOAD_BLOCK_SIZE = 2048 # 2kb
def downloadFile(url, dest, fnUpdate=None):
	"""
	@fnUpdate: an optional function to notify the progress of the download. if the function returns True, the download will be cancelled.
	this function must accept an integer between 0 and 100, where 100 means that the download finished.
	"""
	remote = urlopen(url, timeout=120)
	if remote.code != 200:
		raise RuntimeError("Download failed with code %d" % remote.code)
	size = int(remote.headers["content-length"])
	with open(dest, "wb") as local:
		read = 0
		chunk=DOWNLOAD_BLOCK_SIZE
		while True:
			if size -read < chunk:
				chunk = size -read
			block = remote.read(chunk)
			if not block:
				break
			read += len(block)
			local.write(block)
			if fnUpdate and fnUpdate(int(read / size * 100)):
				return
		if read < size:
			raise RuntimeError("Content too short")
		fnUpdate and fnUpdate(int(read / size * 100))


def guiDownloadFile(url, dest, title, msg):
	gui.mainFrame.prePopup()
	progressDialog = wx.ProgressDialog(
		title,
		msg,
		style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE,
		parent=gui.mainFrame)
	progressDialog.CentreOnScreen()
	progressDialog.Raise()
	def update(val):
		nonlocal progressDialog
		return not progressDialog.Update(val)[0]
	res = True
	while True:
		try:
			gui.ExecAndPump(downloadFile, url, dest, update)
			break
		except:
			# Translators: a message dialog asking to retry or cancel when downloading a file.
			message=_("Unable to download the file. Perhaps there is no internet access or the server is not responding. Do you want to try again?")
			# Translators: the title of a retry cancel dialog when downloading a file.
			title=_("Error downloading")
			if winUser.MessageBox(None,message,title,winUser.MB_RETRYCANCEL) != winUser.IDRETRY:
				res=False
				log.debugWarning(f"Error downloading a file, URL {url}, destination {dest}", exc_info=True)
				break
	progressDialog.Destroy()
	del progressDialog
	gui.mainFrame.postPopup()
	return res


def copyFiles(src, dest):
	import installer
	for curSourceDir,subDirs,files in os.walk(src):
		if curSourceDir == src:
			curDestDir=dest
		else:
			curDestDir=path.join(dest,path.relpath(curSourceDir, dest))
		if not path.isdir(curDestDir):
			os.makedirs(curDestDir)
		for f in files:
			sourceFilePath=path.join(curSourceDir,f)
			destFilePath = path.join(curDestDir,f)
			installer.tryCopyFile(sourceFilePath, destFilePath)


def guiCopiFiles(src, dest, title, msg):
	gui.mainFrame.prePopup()
	progressDialog = gui.IndeterminateProgressDialog(gui.mainFrame, title, msg)
	res = True
	while True:
		try:
			gui.ExecAndPump(copyFiles, src, dest)
			break
		except:
			# Translators: a message dialog asking to retry or cancel when copying files.
			message=_("Unable to copy a file. Perhaps it is currently being used by another process or you have run out of disc space on the drive you are copying to.")
			# Translators: the title of a retry cancel dialog when copying files.
			title=_("Error Copying")
			if winUser.MessageBox(None,message,title,winUser.MB_RETRYCANCEL) != winUser.IDRETRY:
				res=False
				log.debugWarning(f"Error when copying files, source {src}, destination {dest}", exc_info=True)
				break
	progressDialog.done()
	del progressDialog
	gui.mainFrame.postPopup()
	return res


def guiInstallAddon(addonPath):
	res = True
	try:
		bundle = addonHandler.AddonBundle(addonPath)
	except:
		log.error(f"Error opening addon update from {addonPath}", exc_info=True)
		gui.messageBox(
			# Translators: The message displayed when an error occurs when opening an add-on package for adding.
			_("Failed to open add-on update file at %s - missing file or invalid file format") % addonPath,
			# Translators: The title of a dialog presented when an error occurs.
			_("Error"),
			wx.OK | wx.ICON_ERROR
		)
		return False
	if not addonHandler.addonVersionCheck.hasAddonGotRequiredSupport(bundle):
		_showAddonRequiresNVDAUpdateDialog(gui.mainFrame, bundle)
		return False
	if not addonHandler.addonVersionCheck.isAddonTested(bundle):
		_showAddonTooOldDialog(gui.mainFrame, bundle)
		return False
	gui.mainFrame.prePopup()
	progressDialog = gui.IndeterminateProgressDialog(
		gui.mainFrame,
		# Translators: The title of the dialog presented while an Addon is being installed.
		_("Installing %s") % bundle.manifest['name'],
		# Translators: The message displayed while an addon is being installed.
		_("Please wait while the add-on is being installed.")
	)
	try:
		gui.ExecAndPump(bundle.extract, path.join(globalVars.appArgs.configPath, "addons", bundle.manifest['name']))
	except:
		res = False
		log.error(f"Error installing  addon bundle from {addonPath}", exc_info=True)
		gui.messageBox(
			# Translators: The message displayed when an error occurs when installing an add-on package.
			_("Failed to install add-on from %s") % addonPath,
			# Translators: The title of a dialog presented when an error occurs.
			_("Error"),
			wx.OK | wx.ICON_ERROR
		)
	progressDialog.done()
	progressDialog.Destroy()
	del progressDialog
	gui.mainFrame.postPopup()
	return res


def _updateWindowsRootCertificates(url) -> None:
	import updateCheck
	from ctypes import c_void_p, byref, sizeof
	crypt = windll.crypt32
	# Get the server certificate.
	sslCont = ssl._create_unverified_context()
	u = urlopen(url, context=sslCont)
	cert = u.fp._sock.getpeercert(True)
	u.close()
	# Convert to a form usable by Windows.
	certCont = crypt.CertCreateCertificateContext(
		0x00000001,  # X509_ASN_ENCODING
		cert,
		len(cert))
	# Ask Windows to build a certificate chain, thus triggering a root certificate update.
	chainCont = c_void_p()
	crypt.CertGetCertificateChain(None, certCont, None, None,
		byref(updateCheck.CERT_CHAIN_PARA(cbSize=sizeof(updateCheck.CERT_CHAIN_PARA),
			RequestedUsage=updateCheck.CERT_USAGE_MATCH())),
		0, None,
		byref(chainCont))
	crypt.CertFreeCertificateChain(chainCont)
	crypt.CertFreeCertificateContext(certCont)


class GithubService:
	"""
	a class that defines how to get the latest update info and the link to download the latest release.
	"""
	def __init__(self, user, repo):
		self.url = f"https://api.github.com/repos/{user}/{repo}/releases/latest"

	def getUpdateInfo(self):
		try:
			res = urlopen(self.url)
		except IOError as e:
			# this was taken from the NVDA source code
			if isinstance(e.reason, ssl.SSLCertVerificationError) and e.reason.reason == "CERTIFICATE_VERIFY_FAILED":
				_updateWindowsRootCertificates(self.url)
				res = urlopen(self.url)
			else:
				raise
		if res.code != 200:
			raise RuntimeError(f"Checking for update failed with code {res.code} of url: {self.url}")
		data = json.loads(res.read())
		asset = None
		for k in data['assets']:
			if ".nvda-addon" in k['name']:
				asset = k
				break
		if not asset:
			raise RuntimeError("Unable to find the package addon file (.add-on) in the asset list")
		return {
			'version': data['name'],
			'name': asset['name'],
			'downloadUrl': asset['browser_download_url'],
			'releaseDate': time.mktime(time.strptime(asset['updated_at'], "%Y-%m-%dT%H:%M:%SZ"))
		}


class UpdateState:
	def __init__(self):
		self.lastCheck = 0
		self.lastReleaseVersion = ""
		self.releaseDate = None
		self.ignoreCurrentVersion = False
		self.pendingFile = ""


#: The time to wait between checks.
CHECK_INTERVAL = 86400 *1000 # 1 day
RETRY_INTERVAL = 600 *1000 # 10 min
class UpdateHandler:
	"""
	handles the update of the add-on. You must provide the service class to get the update information.
	"""
	def __init__(self, addonName, service):
		if config.isAppX:
			return
		self.service = service
		self.addonName = addonName
		self.storeUpdatesDir = path.join(globalVars.appArgs.configPath, 'updates')
		self.updateStateFile = path.join(globalVars.appArgs.configPath, addonName +'UpdateState' +'.pickle')
		self.state = UpdateState()
		self.timer = None
		self.isError = False
		self.isAutoUpdate = False
		self.loadState()

	def loadState(self):
		try:
			self.state = loadPickle(self.updateStateFile)
		except:
			pass

	def saveState(self):
		try:
			savePickle(self.updateStateFile, self.state)
		except:
			log.error(f"Error saving addon update state from {self.updateStateFile}", exc_info=True)

	def installAddon(self):
		dest = self.state.pendingFile
		res = guiInstallAddon(dest)
		if res:
			self.state.pendingFile = ""
			self.saveState()
			try:
				os.remove(dest)
			except:
				log.error(f"Error removing addon update from {dest}", exc_info=True)
			promptUserForRestart()

	def startUpdateProcess(self, updateInfo):
		if not path.isdir(self.storeUpdatesDir):
			try:
				os.makedirs(self.storeUpdatesDir)
			except:
				return gui.messageBox(
					# Translators: The message displayed if the folder to store the downloaded file can't be created.
					_("Unable to create the folder to save the update file."),
					# Translators: The title displayed if the folder to store the downloaded file can't be created.
					_("Error"),
					wx.OK | wx.ICON_ERROR,
					gui.mainFrame
				)
		dest = path.join(self.storeUpdatesDir, updateInfo['name'])
		guiDownloadFile(
			updateInfo['downloadUrl'],
			dest,
			_("Downloading the new %s update") % self.addonName,
			_("downloading")
		)
		self.state.pendingFile = dest
		self.installAddon()

	def checkUpdate(self, fromGui=False):
		log.info(f"checking for an update of the addon {self.addonName}")
		if config.isAppX:
			return
		self.isError = False
		if self.state.pendingFile and path.exists(self.state.pendingFile):
			# if this happen, update the last check but don't save it to try again if the user restarts NVDA.
			self.state.lastCheck = time.time() *1000
			self.updateTimer()
			return self.installAddon()
		try:
			curAddon = next(addonHandler.getAvailableAddons(filterFunc=lambda x: x.name == self.addonName))
		except:
			# if the addon can't be found, the auto update breaks at all.
			return log.error(f"error getting the current addon {self.addonName}", exc_info=True)
		try:
			d = self.service.getUpdateInfo()
		except:
			self.isError = True
			return self.updateTimer()
		self.state.lastCheck = time.time() *1000
		self.state.lastReleaseVersion = d['version']
		self.state.releaseDate = d['releaseDate']
		self.saveState()
		if curAddon.version == d['version']:
			self.updateTimer()
			if fromGui:
				gui.messageBox(
					# Translators: The message displayed when no updates were found.
					_("There are no updates available for the %s addon.") % self.addonName,
					# Translators: The title  displayed when no updates were found.
					_("No updates available"),
					wx.OK|wx.ICON_INFORMATION,
					gui.mainFrame
				)
			return
		updateMsg = _(
			# Translators: A message asking the user if they wish to update the add-on
			"A new version of %s was found. The new version is %s. Would you like to update this add-on now?"
		) % (self.addonName, d['version'])
		# Translators: Title for message asking if the user wishes to update the add-on.
		updateTitle = _("Update add-on")
		result = gui.messageBox(
			message=updateMsg,
			caption=updateTitle,
			style=wx.YES | wx.NO | wx.ICON_WARNING
		)
		if wx.YES == result:
			self.startUpdateProcess(d)
		self.updateTimer()

	def autoCheckUpdate(self):
		wx.CallAfter(self.checkUpdate)

	def stopTimer(self):
		if self.timer and self.timer.IsRunning():
			self.timer.Stop()
			self.timer = None

	def updateTimer(self):
		if config.isAppX:
			return
		self.stopTimer()
		if not self.isAutoUpdate:
			return
		nextTime = 0
		if self.isError:
			nextTime = RETRY_INTERVAL
		else:
			nextTime = CHECK_INTERVAL -(time.time()*1000 -self.state.lastCheck)
		if nextTime <= 0:
			self.autoCheckUpdate()
		else:
			self.timer = callLater(nextTime, self.autoCheckUpdate)


def _showAddonRequiresNVDAUpdateDialog(parent, bundle):
	incompatibleMessage = _(
		# Translators: The message displayed when installing an add-on package is prohibited,
		# because it requires a later version of NVDA than is currently installed.
		"Installation of {summary} {version} has been blocked. The minimum NVDA version required for "
		"this add-on is {minimumNVDAVersion}, your current NVDA version is {NVDAVersion}"
	).format(
		summary=bundle.manifest['summary'],
		version=bundle.manifest['version'],
		minimumNVDAVersion=addonAPIVersion.formatForGUI(bundle.minimumNVDAVersion),
		NVDAVersion=addonAPIVersion.formatForGUI(addonAPIVersion.CURRENT)
	)
	gui.messageBox(
		# Translators: The message displayed when an error occurs when opening an add-on package for adding.
		incompatibleMessage,
		# Translators: The title of a dialog presented when an error occurs.
		_("Add-on not compatible"),
		wx.OK | wx.ICON_ERROR
	)


def _showAddonTooOldDialog(parent, bundle):
	msg = _(
		# Translators: A message informing the user that this addon can not be installed
		# because it is not compatible.
		"Installation of {summary} {version} has been blocked."
		" An updated version of this add-on is required,"
		" the minimum add-on API supported by this version of NVDA is {backCompatToAPIVersion}"
	).format(
		backCompatToAPIVersion=addonAPIVersion.formatForGUI(addonAPIVersion.BACK_COMPAT_TO),
		**bundle.manifest
	)
	gui.messageBox(
		msg,
		# Translators: The title of the dialog presented when the add-on is too old.
		_("Add-on not compatible"),
		wx.OK | wx.ICON_ERROR
	)
