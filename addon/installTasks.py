from os import path
import wx, gui, addonHandler
addonHandler.initTranslation()


## Translators: message box when user is installing the addon in NVDA. 
msg = _("""The synthesizer won't be available until you set   IBMTTS files. NVDA won't show this synthesizer in teh synthesizers list because you need to set the IBMTTS files location first.
To do it open the NVDA settings dialog, select IBMTTS category and use the "Browse for  IBMTTS library" button to select the IBMTTS files folder.""")

def onInstall():
	if not path.exists(path.join(path.dirname(__file__), 'synthDrivers', 'ibmtts')):
		gui.messageBox(msg,
			# Translators: title of message box when user is installing NVDA
			_("IBMTTS driver for NVDA"), wx.OK)
