# -*- coding: UTF-8 -*-
#Copyright (C) 2009 - 2023 David CM, released under the GPL.
# Author: David CM <dhf360@gmail.com> and others.
#synthDrivers/_ibmeci.py

from ctypes import byref, create_string_buffer, c_int, c_long, c_void_p, pointer, string_at, windll, wintypes, WINFUNCTYPE
from io import BytesIO
from os import path
import queue

import threading, time
import config, languageHandler, nvwave, addonHandler
from logHandler import log
from fileUtils import getFileVersionInfo
from ._settingsDB import appConfig, speechConfig

addonHandler.initTranslation()


class  ECIParam:
	eciSynthMode=0
	eciInputType=1
	eciTextMode=2
	eciDictionary=3
	eciSampleRate = 5
	eciWantPhonemeIndices = 7
	eciRealWorldUnits=8
	eciLanguageDialect=9
	eciNumberMode=10
	eciWantWordIndex = 12


class ECIVoiceParam:
	params = range(1,8)
	eciGender, eciHeadSize, eciPitchBaseline, eciPitchFluctuation, eciRoughness, eciBreathiness, eciSpeed, eciVolume = range(8)


class ECIDictVolume:
	eciMainDict, eciRootDict, eciAbbvDict, eciMainDictExt = range(4)


class ECIMessage:
	eciWaveformBuffer, eciPhonemeBuffer, eciIndexReply, eciPhonemeIndexReply, eciWordIndexReply = range(5)


class ECICallbackReturn:
	eciDataNotProcessed, eciDataProcessed, eciDataAbort= range(3)


class ECILanguageDialect:
	NODEFINEDCODESET = 0x00000000
	GeneralAmericanEnglish = 0x00010000
	BritishEnglish = 0x00010001
	CastilianSpanish = 0x00020000
	MexicanSpanish = 0x00020001
	StandardFrench = 0x00030000
	CanadianFrench = 0x00030001
	StandardGerman = 0x00040000
	StandardItalian = 0x00050000
	MandarinChinese = 0x00060000
	MandarinChineseGB = MandarinChinese
	MandarinChinesePinYin = 0x00060100
	MandarinChineseUCS = 0x00060800
	TaiwaneseMandarin = 0x00060001
	TaiwaneseMandarinBig5 = TaiwaneseMandarin
	TaiwaneseMandarinZhuYin = 0x00060101
	TaiwaneseMandarinPinYin = 0x00060201
	TaiwaneseMandarinUCS = 0x00060801
	BrazilianPortuguese = 0x00070000
	StandardJapanese = 0x00080000
	StandardJapaneseSJIS = StandardJapanese
	StandardJapaneseUCS = 0x00080800
	StandardFinnish = 0x00090000
	StandardKorean = 0x000A0000
	StandardKoreanUHC = StandardKorean
	StandardKoreanUCS = 0x000A0800
	StandardCantonese = 0x000B0000
	StandardCantoneseGB = StandardCantonese
	StandardCantoneseUCS = 0x000B0800
	HongKongCantonese = 0x000B0001
	HongKongCantoneseBig5 = HongKongCantonese
	HongKongCantoneseUCS = 0x000B0801
	StandardDutch = 0x000C0000
	StandardNorwegian = 0x000D0000
	StandardSwedish = 0x000E0000
	StandardDanish = 0x000F0000
	StandardReserved = 0x00100000
	StandardThai = 0x00110000


langs={
	'esp': (ECILanguageDialect.CastilianSpanish, _('Castilian Spanish'), 'es_ES', 'es'),
	'esm': (ECILanguageDialect.MexicanSpanish, _('Latin American Spanish'), 'es_MX', 'es_CO'),
	'ptb': (ECILanguageDialect.BrazilianPortuguese, _('Brazilian Portuguese'), 'pt_BR', 'pt'),
	'fra': (ECILanguageDialect.StandardFrench, _('French'), 'fr_FR', 'fr'),
	'frc': (ECILanguageDialect.CanadianFrench, _('French Canadian'), 'fr_CA', ''),
	'fin': (ECILanguageDialect.StandardFinnish, _('Finnish'), 'fi_FI', 'fi'),
	'chs': (ECILanguageDialect.MandarinChinese, _('Chinese'), 'zh_CN', 'zh'),
	'jpn': (ECILanguageDialect.StandardJapanese, _('Japanese'), 'ja_JP', 'jp'),
	'kor': (ECILanguageDialect.StandardKorean, _('Korean'), 'ko_KR', 'ko'),
	'deu': (ECILanguageDialect.StandardGerman, _('German'), 'de_DE', 'de'),
	'ita': (ECILanguageDialect.StandardItalian, _('Italian'), 'it_IT', 'it'),
	'enu': (ECILanguageDialect.GeneralAmericanEnglish, _('American English'), 'en_US', 'en'),
	'eng': (ECILanguageDialect.BritishEnglish, _('British English'), 'en_UK', ''),
	'swe': (ECILanguageDialect.StandardSwedish, _('Swedish'), 'sv_SE', 'sv'),
	'nor': (ECILanguageDialect.StandardNorwegian, _('Norwegian'), 'nb_NO', 'nb'),
	'dan': (ECILanguageDialect.StandardDanish, _('Danish'), 'da_DK', 'da'),
	'ctt': (ECILanguageDialect.HongKongCantonese, _('Hong Kong Cantonese'), 'yue', '')
}


# constants
samples=3300
user32 = windll.user32

WM_PROCESS = 1025
WM_SILENCE = 1026
WM_PARAM = 1027
WM_VPARAM=1028
WM_COPYVOICE=1029
WM_KILL=1030
WM_SYNTH=1031
WM_INDEX=1032


# global variables
audioStream = BytesIO()
player = None
currentSoundcardOutput = None
currentSampleRate = None
isIBM=False
speaking=False
eciThread = None
callbackQueue = None
callbackThread = None
eciQueue = None
eciThreadId = None
idleTimer = None
onIndexReached = None
onDoneSpeaking = None
endMarkersCount = 0

buffer = create_string_buffer(samples*2)

stopped = threading.Event()
started = threading.Event()
param_event = threading.Event()
lastindex=0
avLangs=0
ttsPath=""
dllName=""
#We can only have one of each in NVDA. Make this global
dll = None
handle = None
dictHandles={}
params = {}
vparams = {}


class EciThread(threading.Thread):
	def run(self):
		global vparams, params, speaking, endMarkersCount
		global eciThreadId, dll, handle
		eciThreadId = windll.kernel32.GetCurrentThreadId()
		msg = wintypes.MSG()
		user32.PeekMessageA(byref(msg), None, 0x400, 0x400, 0)
		(dll, handle) = eciNew()
		dll.eciRegisterCallback(handle, eciCallback, None)
		dll.eciSetOutputBuffer(handle, samples, pointer(buffer))
		dll.eciSetParam(handle, ECIParam.eciSynthMode, 1)
		dll.eciSetParam(handle, ECIParam.eciInputType, 1)
		params[ECIParam.eciLanguageDialect] = dll.eciGetParam(handle, ECIParam.eciLanguageDialect)
		# loading of fallback root.dic/main.dic/abbr.dic officially removed as of 20.08-x0_personal, to make room for other languages' dictionaries.
		v=loadDictForLanguage()
		if v is not None:
			dictHandles[v[0]]=v[1]
			dll.eciSetDict(handle,v[1])
		started.set()
		while True:
			user32.GetMessageA(byref(msg), 0, 0, 0)
			user32.TranslateMessage(byref(msg))
			if msg.message == WM_PROCESS:
				processEciQueue()
			elif msg.message == WM_SILENCE:
				speaking=False
				audioStream.seek(0)
				audioStream.truncate(0)
				dll.eciStop(handle)
				try:
					while True:
						callbackQueue.get_nowait()
						callbackQueue.task_done()
				except:
						pass
				player.stop()
				endMarkersCount = 0
			elif msg.message == WM_PARAM:
				dll.eciSetParam(handle, msg.lParam, msg.wParam)
				params[msg.lParam] = msg.wParam
				param_event.set()
				if msg.lParam==ECIParam.eciLanguageDialect:
					if msg.wParam not in dictHandles:
						v=loadDictForLanguage()
						if v is not None:
							dictHandles[v[0]]=v[1]
							dll.eciSetDict(handle,v[1])
			elif msg.message == WM_VPARAM:
				(param, val) = msg.wParam, msg.lParam
				# don't set unless we have to
				#This doesn't fix the rate problem, though.
				#if param in vparams and vparams[param] == val: continue
				dll.eciSetVoiceParam(handle, 0, msg.wParam, msg.lParam)
				vparams[msg.wParam] = msg.lParam
				param_event.set()
			elif msg.message == WM_COPYVOICE:
				dll.eciCopyVoice(handle, msg.wParam, 0)
				for i in ECIVoiceParam.params:
					vparams[i] = dll.eciGetVoiceParam(handle, 0, i)
				param_event.set()
			elif msg.message == WM_KILL:
				dll.eciDelete(handle)
				dictHandles.clear()
				stopped.set()
				break
			else:
				user32.DispatchMessageA(byref(msg))

def processEciQueue():
	lst = eciQueue.get()
	for (func, args) in lst:
		func(*args)
	eciQueue.task_done()


def setPathsFromConfig():
	global ttsPath, dllName
	dllName = appConfig.dllName
	ttsPath =  appConfig.TTSPath
	if  not path.isabs(ttsPath):
		ttsPath = path.abspath(path.join(path.abspath(path.dirname(__file__)), ttsPath))


def updateIniPaths():
	iniPath = path.join(ttsPath, dllName[:-3] +"ini")
	if path.isabs(appConfig.TTSPath) or not path.exists(iniPath):
		return
	ini=open(iniPath, "r+")
	ini.seek(12)
	tml=ini.readline()[:-8]
	newPath = ttsPath + "\\"
	if tml != newPath:
		ini.seek(12)
		tmp=ini.read()
		ini.seek(12)
		ini.write(tmp.replace(tml, newPath))
		ini.truncate()
	ini.close()


def loadEciLibrary():
	global isIBM
	# the absolute paths must be set first.
	# if the dll has been loaded, it won't load the library again.
	if dll:
		return dll
	etidevLibPath = path.join(ttsPath, "etidev.dll")
	eciLibPath = path.join(ttsPath, dllName)
	if getFileVersionInfo(eciLibPath, 'ProductName')['ProductName'] == 'IBMECI':
		isIBM = True
	else:
		isIBM = False
	if path.exists(etidevLibPath):
		windll.LoadLibrary(etidevLibPath)
	return windll.LoadLibrary(eciLibPath)


def eciCheck():
	if dll: return True
	setPathsFromConfig()
	if not path.exists(ttsPath): return False
	try:
		# the ini file must be updated before the first load of the library.
		updateIniPaths()
		loadEciLibrary().eciVersion
		return True
	except:
		log.info("Error checking the IBMTTS library", exc_info=True)
		return False


def eciNew():
	global avLangs
	eciCheck()
	eci = loadEciLibrary()
	b=c_int()
	eci.eciGetAvailableLanguages(0,byref(b))
	avLangs=(c_int*b.value)()
	eci.eciGetAvailableLanguages(byref(avLangs),byref(b))
	try:
		handle=eci.eciNewEx(int(speechConfig.ibmtts['voice']))
	except:
		handle=eci.eciNewEx(getVoiceByLanguage(languageHandler.getLanguage())[0])
	for i in ECIVoiceParam.params:
		vparams[i] = eci.eciGetVoiceParam(handle, 0, i)
	return eci,handle


@WINFUNCTYPE(c_int,c_int,c_int,c_long,c_void_p)
def _callbackExec(func, *args, **kwargs):
	global callbackQueue
	callbackQueue.put((func, args, kwargs))

def setLast(lp):
	global lastindex
	lastindex = lp
	onIndexReached(lp)

def bgPlay(stri):
	global player, currentSampleRate
	if not player or len(stri) == 0: return
	# Sometimes player.feed() tries to open the device when it's already open,
	# causing a WindowsError. This code catches and works around this.
	# [DGL, 2012-12-18 with help from Tyler]
	tries = 0
	while tries < 10:
		try:
			player.feed(stri)
			if tries > 0:
				log.warning("Eloq speech retries: %d" % (tries))
			return
		except FileNotFoundError:
			# reset the player if the used soundcard is not present. E.G. the total number of sound devices has changed.
			player.close()
			player = createPlayer(currentSampleRate)
		except:
			player.idle()
			time.sleep(0.02)
			tries += 1
	log.error("Eloq speech failed to feed one buffer.")

indexes = []
def sendIndexes():
	global indexes
	for i in indexes: _callbackExec(setLast, i)
	indexes = []

def playStream():
	global audioStream
	_callbackExec(bgPlay, audioStream.getvalue())
	audioStream.truncate(0)
	audioStream.seek(0)
	sendIndexes()

endStringReached = False

@WINFUNCTYPE(c_int, c_int, c_int, c_int, c_void_p)
def eciCallback (h, ms, lp, dt):
	global audioStream, speaking, END_STRING_MARK, endMarkersCount, indexes, endStringReached
	if speaking and ms == ECIMessage.eciWaveformBuffer:
		audioStream.write(string_at(buffer, lp*2))
		if audioStream.tell() >= samples*2: playStream()
		endStringReached = False
	elif ms==ECIMessage.eciIndexReply:
		if lp == END_STRING_MARK:
			if audioStream.tell() > 0: playStream()
			sendIndexes()
			_callbackExec(endStringEvent)
			endStringReached = True
		else:
			if endStringReached: _callbackExec(setLast, lp)
			else: indexes.append(lp)
	return ECICallbackReturn.eciDataProcessed

class CallbackThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.daemon = True

	def run(self):
		try:
			while True:
				func, args, kwargs = callbackQueue.get()
				if not func:
					break
				func(*args, **kwargs)
				callbackQueue.task_done()
		except:
			log.error("CallbackThread.run", exc_info=True)

def _callbackExec(func, *args, **kwargs):
	global callbackQueue
	callbackQueue.put((func, args, kwargs))

def initialize(indexCallback, doneCallback):
	global callbackQueue, callbackThread, eciQueue, eciThread, idleTimer, onIndexReached, onDoneSpeaking, player
	onIndexReached = indexCallback
	onDoneSpeaking = doneCallback
	idleTimer = threading.Timer(0.3, time.sleep) # fake timer because this can't be None.
#	player = createPlayer(1)
	if not eciCheck():
		raise RuntimeError("No IBMTTS  synthesizer  available")
	eciQueue = queue.Queue()
	eciThread = EciThread()
	eciThread.start()
	started.wait()
	started.clear()
	callbackQueue = queue.Queue()
	callbackThread = CallbackThread()
	callbackThread.start()
	toggleProbileSwitchRegistration(config.post_configProfileSwitch.register)

def speak(text):
	# deleted the following fix because is incompatible with NVDA's speech change command. Now send it from speak in ibmeci.py
	#Sometimes the synth slows down for one string of text. Why?
	#Trying to fix it here.
	# if ECIVoiceParam.eciSpeed in vparams: text = b"`vs%d%s" % (vparams[ECIVoiceParam.eciSpeed], text)
	dll.eciAddText(handle, text)

def index(x):
	dll.eciInsertIndex(handle, x)

END_STRING_MARK = 0xffff
endMarkersCount = 0
def setEndStringMark():
	global endMarkersCount, END_STRING_MARK
	dll.eciInsertIndex(handle, END_STRING_MARK)
	endMarkersCount+=1


def synth():
	global idleTimer, speaking
	speaking = True
	idleTimer.cancel()
	dll.eciSynthesize(handle)

def stop():
	user32.PostThreadMessageA(eciThreadId, WM_SILENCE, 0, 0)

def pause(switch):
	player.pause(switch)

def terminate():
	global callbackQueue, callbackThread, dll, eciQueue,eciThread, handle, idleTimer, onDoneSpeaking, onIndexReached, player
	user32.PostThreadMessageA(eciThreadId, WM_KILL, 0, 0)
	stopped.wait()
	stopped.clear()
	callbackQueue.put((None, None, None))
	eciThread.join()
	callbackThread.join()
	idleTimer.cancel()	
	player.close()
	callbackQueue= callbackThread= dll= eciQueue=eciThread= handle= idleTimer= onDoneSpeaking= onIndexReached= player = None
	toggleProbileSwitchRegistration(config.post_configProfileSwitch.unregister)


def setVoice(vl):
	user32.PostThreadMessageA(eciThreadId, WM_PARAM, vl, ECIParam.eciLanguageDialect)
	param_event.wait()
	param_event.clear()

def setParam(param, val):
	user32.PostThreadMessageA(eciThreadId, WM_PARAM, val, param)
	param_event.wait()
	param_event.clear()

def getVParam(pr):
	return vparams[pr]

def setVParam(pr, vl):
	user32.PostThreadMessageA(eciThreadId, WM_VPARAM, pr, vl)
	param_event.wait()
	param_event.clear()

def setProsodyParam(pr, vl):
	dll.eciSetVoiceParam(handle, 0, pr, vl)

def setVariant(v):
	user32.PostThreadMessageA(eciThreadId, WM_COPYVOICE, v, 0)
	param_event.wait()
	param_event.clear()

def process():
		user32.PostThreadMessageA(eciThreadId, WM_PROCESS, 0, 0)

def eciVersion():
	ptr=b"       "
	dll.eciVersion(ptr)
	return ptr.decode('ascii')

def getVoiceByLanguage(lang):
	""" Return the voice corresponding to the given language
	@param lang The lang we  want to use
	@return The corresponding voice, else English.
	"""
	for v in langs.values():
		if v[2] == lang:
			return v
		elif v[3] == lang:
			return v
	return langs['enu']

def getLangByEciId(eciId):
	""" Return the corresponding lang code in the format ECI expects given its internal identifying numbers for each.
	@param eciId The numeric ECI identifier of a given language, such as 65536 for enu
	@return the three letter language code if valid, else 'enu'
	"""
	for k,v in langs.items():
		if v[0]==eciId:
			return k
	return 'enu'

def loadDictForLanguage():
	""" If dictionary files exist for the language at the time of calling, creates a new dict handle and loads these, then returns a tuple.
	Note: Does not call setDict!
	@return a 2 tuple of ECILanguageDialect, ECIDictHand if a dictionary has been loaded, else None
	"""
	# obtain the identifier string used to prefix dictionary files to separate them for different languages
	langid=getLangByEciId(params[ECIParam.eciLanguageDialect])
	# check to see if any dictionaries we want exist
	# fixme: doesn't even check for mainext. Character sets make that somewhat strange.
	if path.exists(path.join(path.abspath(ttsPath), langid+"main.dic")) or \
	path.exists(path.join(path.abspath(ttsPath), langid+"root.dic")) or \
	path.exists(path.join(path.abspath(ttsPath), langid+"abbr.dic")):
		dictionaryHandle=dll.eciNewDict(handle)
		if path.exists(path.join(path.abspath(ttsPath), langid+"main.dic")):
			dll.eciLoadDict(handle, dictionaryHandle, 0, path.join(path.abspath(ttsPath), langid+"main.dic").encode('mbcs'))
		if path.exists(path.join(path.abspath(ttsPath), langid+"root.dic")):
			dll.eciLoadDict(handle, dictionaryHandle, 1, path.join(path.abspath(ttsPath), langid+"root.dic").encode('mbcs'))
		if path.exists(path.join(path.abspath(ttsPath), langid+"abbr.dic")):
			dll.eciLoadDict(handle, dictionaryHandle, 2, path.join(path.abspath(ttsPath), langid+"abbr.dic").encode('mbcs'))
		return (params[ECIParam.eciLanguageDialect], dictionaryHandle)
	else: return None

def endStringEvent():
	global idleTimer, speaking, endMarkersCount
	endMarkersCount -=1
	if endMarkersCount == 0:
		speaking = False
		idleTimer = threading.Timer(0.3, idlePlayer)
		idleTimer.start()

def idlePlayer():
	global player, speaking
	if not speaking:
		player.idle()
		onDoneSpeaking()

def createPlayer(sampleRate):
	global currentSoundcardOutput, currentSampleRate
	currentSoundcardOutput = speechConfig.outputDevice
	currentSampleRate = sampleRate
	if sampleRate == 0:
		player = nvwave.WavePlayer(1, 8000, 16, outputDevice=currentSoundcardOutput)
	elif sampleRate == 1:
		player = nvwave.WavePlayer(1, 11025, 16, outputDevice=currentSoundcardOutput)
	elif sampleRate == 2:
		player = nvwave.WavePlayer(1, 22050, 16, outputDevice=currentSoundcardOutput)
	else:
		player = nvwave.WavePlayer(1, 11025, 16, outputDevice=currentSoundcardOutput)
	return player

def handleSoundcardChange():
	global currentSoundcardOutput, currentSampleRate, player
	# if player is none, this driver is not active.
	# This may occur because post_configProfileSwitch.unregister is delaied by 1 second.
	if player and currentSoundcardOutput != speechConfig.outputDevice:
		player.close()
		player = createPlayer(currentSampleRate)

profileSwitchRegister = None
def toggleProbileSwitchRegistration(fn):
	""" the register or unregister of the handler for config changes can't be done when a profile switch is being done.
	this function helps to avoid that.
	fn: the function to be called (usually register or unregister)
	"""
	global profileSwitchRegister
	if profileSwitchRegister:
		profileSwitchRegister.cancel()
		profileSwitchRegister = None
	profileSwitchRegister = threading.Timer(1, fn, [handleSoundcardChange])
	profileSwitchRegister.start()
