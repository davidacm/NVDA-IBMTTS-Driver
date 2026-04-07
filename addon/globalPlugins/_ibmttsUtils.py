# -*- coding: UTF-8 -*-
#Copyright (C) 2009 - 2023 David CM, released under the GPL.
# Author: David CM <dhf360@gmail.com> and others.
#globalPlugins/_ibmttsutils.py

import addonAPIVersion, config, json, os, pickle, ssl, time, winUser, wx, zipfile
from os import path
from ctypes import windll
from urllib.request import urlopen
import struct

import globalVars, gui, addonHandler
from core import callLater
from logHandler import log
from gui.addonGui import promptUserForRestart

try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.warning(
		"Unable to initialise translations. This may be because the addon is running from NVDA scratchpad."
	)


def find_symbol_in_dll(dll_path, target_symbol="eciVersion"):
	""" Verifies if a specific function symbol exists in a Windows DLL's export table.

	This function parses the Portable Executable (PE) format manually to avoid 
	loading the library, allowing a 64-bit process to verify a 32-bit DLL 
	without architecture mismatch errors.

	Args:
		dll_path (str): The absolute or relative path to the DLL file.
		target_symbol (str): The name of the function to look for. 
			Defaults to "eciVersion".

	Returns:
		bool: True if the symbol is found in the Export Name Pointer Table, 
			False otherwise.
	"""
	# import mmap here, to avoid issues with NVDA 2025 or less.
	import mmap
	try:
		with open(dll_path, "rb") as f:
			# Memory-map the file for efficient binary navigation
			mm = mmap.mmap(	f.fileno(), 0, access=mmap.ACCESS_READ)

			# Locate the PE Header signature (offset stored at 0x3C)
			pe_header_ptr = struct.unpack("<I", mm[0x3C:0x40])[0]
			if mm[pe_header_ptr:pe_header_ptr+4] != b"PE\x00\x00":
				return False # Not a valid PE file
			# Navigate to the Optional Header's Data Directories.
			# For 32-bit (PE32), the Export Table RVA is at offset 120 from the PE signature.
			# This logic assumes a standard 32-bit library.
			export_table_rva = struct.unpack("<I", mm[pe_header_ptr+120:pe_header_ptr+124])[0]
			if export_table_rva == 0:
				return False # No exports found in this library

			# Translate the Relative Virtual Address (RVA) to a physical file offset.
			# We must find which section contains the export table.
			num_sections = struct.unpack("<H", mm[pe_header_ptr+6:pe_header_ptr+8])[0]
			header_size = struct.unpack("<H", mm[pe_header_ptr+20:pe_header_ptr+22])[0]
			section_entry_start = pe_header_ptr + 24 + header_size

			file_offset_base = None
			virtual_addr_base = None

			for i in range(num_sections):
				s_start = section_entry_start + (i * 40)
				v_addr = struct.unpack("<I", mm[s_start+12:s_start+16])[0]
				v_size = struct.unpack("<I", mm[s_start+8:s_start+12])[0]
				r_ptr = struct.unpack("<I", mm[s_start+20:s_start+24])[0]
				# Check if the export table RVA falls within this section's range
				if v_addr <= export_table_rva < v_addr + v_size:
					file_offset_base = r_ptr
					virtual_addr_base = v_addr
					break

			if file_offset_base is None:
				return False

			# Calculate the physical file offset of the Export Directory
			export_dir_offset = export_table_rva - virtual_addr_base + file_offset_base

			# Parse the Export Directory to find the Name Pointer Table
			num_names = struct.unpack("<I", mm[export_dir_offset+24:export_dir_offset+28])[0]
			names_rva = struct.unpack("<I", mm[export_dir_offset+32:export_dir_offset+36])[0]

			# Translate the Names RVA to file offset
			names_ptr_offset = names_rva - virtual_addr_base + file_offset_base

			for i in range(num_names):
				name_rva = struct.unpack("<I", mm[names_ptr_offset + (i*4) : names_ptr_offset + (i*4) + 4])[0]
				name_file_offset = name_rva - virtual_addr_base + file_offset_base
				null_byte_idx = mm.find(b"\x00", name_file_offset)
				function_name = mm[name_file_offset:null_byte_idx].decode("ascii", errors="ignore")
				if function_name == target_symbol:
					mm.close()
					return True
			mm.close()
			return False
	except (IOError, struct.error, UnicodeDecodeError):
		# Handle cases where the file is locked, too small, or corrupted
		return False

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


def parseVersion(v):
	try:
		parts = v.strip().replace("v", "").split(".")
		return tuple(int(p) for p in parts)
	except:
		return (0, 0, 0)


def isNewerVersion(newVersion, currentVersion):
	return parseVersion(newVersion) > parseVersion(currentVersion)


def guiInstallAddon(addonPath):
	try:
		from systemUtils import ExecAndPump
		from gui.message import DisplayableError

		bundle = addonHandler.AddonBundle(addonPath)

		prevAddon = None
		for a in addonHandler.getAvailableAddons():
			if a.name == bundle.manifest.get("name"):
				prevAddon = a
				break
		result = ExecAndPump(addonHandler.installAddonBundle, bundle)
		addonObj = result.funcRes
		if getattr(bundle, "_installExceptions", None):
			for e in bundle._installExceptions:
				log.error(e, exc_info=True)
			raise DisplayableError(_("Failed to install add-on from %s") % addonPath)
		if prevAddon:
			prevAddon.requestRemove()
		if addonObj:
			addonObj._cleanupAddonImports()
		return True
	except Exception:
		log.error(f"Error installing addon from {addonPath}", exc_info=True)
		gui.messageBox(
			_("Failed to install the update."),
			_("Error"),
			wx.OK | wx.ICON_ERROR
		)
		return False

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
			raise RuntimeError("Unable to find the package addon file (.nvda-addon)")

		return {
			'version': data['tag_name'].replace("v", ""), # use tag_name as version
			'name': asset['name'],
			'downloadUrl': asset['browser_download_url'],
			'releaseDate': time.mktime(time.strptime(asset['updated_at'], "%Y-%m-%dT%H:%M:%SZ")),
			'body': data.get('body', _("No release notes available."))
		}

class UpdateState:
	def __init__(self):
		self.lastCheck = 0
		self.lastReleaseVersion = ""
		self.releaseDate = None
		self.ignoreCurrentVersion = False
		self.pendingFile = ""

class UpdateDialog(wx.Dialog):
	def __init__(self, parent, addonName, version, body):
		super().__init__(parent, title=_("Update available"), size=(500, 400))

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		msg = wx.StaticText(
			self,
			label=_("A new version of %s is available (%s). Do you want to update?") % (addonName, version)
		)
		mainSizer.Add(msg, 0, wx.ALL, 10)

		notesLabel = wx.StaticText(self, label=_("What's new:"))
		mainSizer.Add(notesLabel, 0, wx.LEFT | wx.TOP, 10)

		self.notesCtrl = wx.TextCtrl(
			self,
			value=body,
			style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2
		)
		mainSizer.Add(self.notesCtrl, 1, wx.EXPAND | wx.ALL, 10)

		btnSizer = self.CreateButtonSizer(wx.YES | wx.NO)
		mainSizer.Add(btnSizer, 0, wx.EXPAND | wx.ALL, 10)

		self.Bind(wx.EVT_BUTTON, lambda evt: self.onOk(), id=wx.ID_YES)
		self.Bind(wx.EVT_BUTTON, lambda evt: self.onCancel(), id=wx.ID_NO)

		self.SetSizer(mainSizer)
		self.Centre()

	def onOk(self):
		self.EndModal(wx.ID_YES)
		self.Destroy()

	def onCancel(self):
		self.EndModal(wx.ID_NO)
		self.Destroy()


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
		gui.mainFrame.prePopup()
		res = guiInstallAddon(dest)
		gui.mainFrame.postPopup()
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
		if not isNewerVersion(d['version'], curAddon.version):
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
		dlg = UpdateDialog(gui.mainFrame, self.addonName, d['version'], d.get('body', ''))
		res = dlg.ShowModal()
		if res == wx.ID_YES:
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
			nextTime = int(CHECK_INTERVAL - (time.time() * 1000 - self.state.lastCheck))
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


class DonationDialog(gui.nvdaControls.MessageDialog):
	def __init__(self, parent, title, message, donateOptions):
		self.donateOptions = donateOptions
		super().__init__(parent, title, message, dialogType=gui.nvdaControls.MessageDialog.DIALOG_TYPE_WARNING)

	def _addButtons(self, buttonHelper):
		for k in self.donateOptions:
			btn = buttonHelper.addButton(self, label=k['label'], name=k['url'])
			btn.Bind(wx.EVT_BUTTON, self.onDonate)
		cancelBtn = buttonHelper.addButton(self, id=wx.ID_CANCEL, label=_("&Not now"))
		cancelBtn.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.CANCEL))

	def onDonate(self, evt):
		donateBtn = evt.GetEventObject()
		donateUrl = donateBtn.Name
		os.startfile(donateUrl)
		self.EndModal(wx.OK)


def showDonationsDialog(parentWindow, addonName, donateOptions):
	title = _("Request for contributions to %s") % addonName
	message = _("""Creating add-ons demands substantial time and effort. With limited job prospects in my country, your donations could significantly aid in dedicating more time to developing free plugins for the community.
Your contribution would support the development of this and other free projects.
Would you like to contribute to this cause? Select from our available payment methods below. You will be redirected to the corresponding website to complete your donation.
Thank you for your support and generosity.""")
	return DonationDialog(parentWindow, title,  message, donateOptions).ShowModal()
