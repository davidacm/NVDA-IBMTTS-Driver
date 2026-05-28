# -*- coding: UTF-8 -*-
#Copyright (C) 2009 - 2026 David CM, released under the GPL.
# Author: David CM <dhf360@gmail.com> and others.
#synthDrivers/_ibmeci.py

from ctypes import byref, create_string_buffer, c_int, c_long, c_void_p, pointer, string_at, windll, wintypes, WINFUNCTYPE
from io import BytesIO
from os import path
import queue


import threading, time
import languageHandler, nvwave, addonHandler
import queueHandler
from config import conf
from logHandler import log
from fileUtils import getFileVersionInfo
from ._settingsDB import appConfig
try:
	from synthDriverHandler import findAndSetNextSynth
except ImportError:
	log.info("Couldn't import findAndSetNextSynth from synthDriverHandler. So the IBMTTS engine won't be able to switch to another synth if it fails.", exc_info=True)
	findAndSetNextSynth = lambda x: None


# determine if 32 or 64 bits.
import struct
IS_64BIT = struct.calcsize("P") == 8
if IS_64BIT:
	from ._proxyEci import EciDLL
	from ._ipc import terminate_host_32, is_host_process_alive
else:
	is_host_process_alive = lambda: True


addonHandler.initTranslation()


class  ECIParam():
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


class ECIDictVolume():
	eciMainDict, eciRootDict, eciAbbvDict, eciMainDictExt = range(4)


class ECIMessage():
	eciWaveformBuffer, eciPhonemeBuffer, eciIndexReply, eciPhonemeIndexReply, eciWordIndexReply = range(5)


class ECICallbackReturn():
	eciDataNotProcessed, eciDataProcessed, eciDataAbort= range(3)


class ECILanguageDialect():
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
WM_PROCESS_NEXT_CHUNK=1033

# Chunking parameters: split very long texts so each eciSynthesize call processes
# a small piece. The internal index is placed at the end of each chunk; the request
# for the next chunk is posted from the playback path so the player's feed-backpressure
# (a second player.feed blocks until the first is done) paces our synthesis.
CHUNK_SIZE = 2000
INTERNAL_CHUNK_INDEX = 0xfffe  # reserved internal marker (END_STRING_MARK is 0xffff)
# Encodings that are always one byte per character — split anywhere is safe.
_SINGLE_BYTE_ENCODINGS = frozenset(('cp1252', 'mbcs'))


class _PendingChunkSource:
	"""Holds a reference to a big text being chunked plus the current offset and the
	encoding it was produced with. The big payload is referenced (bytes are immutable)
	so it is not copied."""
	__slots__ = ('data', 'encoding', 'offset')
	def __init__(self, data, encoding):
		self.data = data
		self.encoding = encoding
		self.offset = 0


def _findChunkSplit(data, target, encoding):
	"""Return a split position <= target that is safe for the given encoding.
	For single-byte encodings, returns target unchanged. For the multi-byte encodings
	used by this driver (gb18030/cp932/cp949/big5), scans backwards for a byte that
	can never be a trail byte (< 0x30) and returns the position right after it."""
	if not encoding or encoding in _SINGLE_BYTE_ENCODINGS:
		return target
	start = max(target - 512, 0)
	for i in range(target - 1, start - 1, -1):
		if data[i] < 0x30:
			return i + 1
	return target


# global variables
tts_name = None
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
# Chunking and flow-control state. Only touched on the ECI thread.
pendingChunkSource = None
deferredOps = []
# Set after each synth() in an outlist; cleared once the synth's audio has been fed to
# the player. While set, any newly arriving outlist is parked on deferredOps so the
# engine doesn't race ahead of playback.
waitingForDrain = False

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

def check_lang_param(lang):
	if lang in avLangs:
		return lang
	log.warning("Language %s is not supported by the IBMTTS engine. Changing to a default language" % lang)
	lang = getVoiceByLanguage(languageHandler.getLanguage())[0]
	if lang in avLangs:
		return lang
	log.warning("Couldn't find a default language for the IBMTTS engine. Changing to the first available language.")
	return avLangs[0]


def post_message_to_eciThread(msg, wParam, lParam, exceptOnDie=True):
	"""Send a message to the ECI thread. First verifying that it is alive."""
	global eciThread
	if exceptOnDie and (eciThread is None or not eciThread.is_alive()):
		raise RuntimeError("IBMTTS Engine thread is not running. Synthesizer failure.")
	user32.PostThreadMessageA(eciThreadId, msg, wParam, lParam)


class EciThread(threading.Thread):
	def run(self):
		try:
			self._run()
		except Exception as e:
			queueHandler.queueFunction(queueHandler.eventQueue, findAndSetNextSynth, tts_name)
			raise e
		finally:
			started.set()
			stopped.set()
			param_event.set()
			if dll and is_host_process_alive():
				dll.eciDelete(handle)

	def _run(self):
		global vparams, params, speaking, endMarkersCount, buffer
		global eciThreadId, dll, handle, pendingChunkSource, waitingForDrain
		eciThreadId = windll.kernel32.GetCurrentThreadId()
		msg = wintypes.MSG()
		user32.PeekMessageA(byref(msg), None, 0x400, 0x400, 0)
		(dll, handle) = eciNew()
		dll.eciRegisterCallback(handle, eciCallback, None)
		if IS_64BIT:
			dll.eciSetOutputBuffer(handle, samples)
			buffer = dll.get_audio_buffer_ptr()
		else:
			dll.eciSetOutputBuffer(handle, samples, pointer(buffer))
		# next line is required to process audio properly
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
			elif msg.message == WM_PROCESS_NEXT_CHUNK:
				sendNextChunk()
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
				pendingChunkSource = None
				deferredOps.clear()
				waitingForDrain = False
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
	eciQueue.task_done()
	if pendingChunkSource is not None or waitingForDrain:
		# Either mid-chunking or waiting for the previous outlist's audio to be fed.
		# Either way, park the new ops so they run in order once we resume.
		deferredOps.extend(lst)
		return
	runOps(lst)


def runOps(ops):
	"""Execute ops sequentially. Two things make us return early and defer the rest:
	(a) the first speak op larger than CHUNK_SIZE — it starts chunked playback;
	(b) a synth op — that synth's audio must be fed to the player before anything else
	    is sent to the engine, so we set waitingForDrain and stop here. The drain is
	    cleared when END_STRING_MARK fires (see eciCallback) and the
	    _postNextChunkMessage queued behind this synth's bgPlay items runs."""
	global pendingChunkSource, waitingForDrain
	for i, (func, args) in enumerate(ops):
		if func is speak and len(args[0]) > CHUNK_SIZE:
			data = args[0]
			encoding = args[1] if len(args) > 1 else None
			pendingChunkSource = _PendingChunkSource(data, encoding)
			deferredOps.clear()
			deferredOps.extend(ops[i+1:])
			sendNextChunk()
			return
		if func is synth:
			# Set the flag *before* calling synth so the END_STRING_MARK callback that
			# fires inside eciSynthesize sees a consistent state.
			waitingForDrain = True
			func(*args)
			if i + 1 < len(ops):
				deferredOps.extend(ops[i+1:])
			return
		func(*args)


def sendNextChunk():
	"""Drives both flow-control mechanisms. When chunking is active, push the next
	chunk (or finish the source and resume deferred ops). Otherwise treat this as
	drain-done from a previous outlist's synth: clear the flag and run any deferred
	ops queued while we were waiting."""
	global pendingChunkSource, waitingForDrain
	if pendingChunkSource is not None:
		data = pendingChunkSource.data
		encoding = pendingChunkSource.encoding
		offset = pendingChunkSource.offset
		remaining = len(data) - offset
		if remaining <= CHUNK_SIZE:
			# Last chunk: send the rest as a single piece (no internal index needed)
			# and let the deferred ops (setEndStringMark + synth) close out the speech.
			speak(data[offset:])
			pendingChunkSource = None
			ops = list(deferredOps)
			deferredOps.clear()
			runOps(ops)
			return
		# Not the last chunk: emit the chunk + an internal index at its end, then synth.
		# The next-chunk request is posted from the playback path (see eciCallback), so
		# the player's natural backpressure (feed blocks while the previous chunk is
		# still playing) keeps us from running ahead of audio.
		chunk_end = _findChunkSplit(data, offset + CHUNK_SIZE, encoding)
		if chunk_end <= offset:
			chunk_end = offset + CHUNK_SIZE  # forced split — may cut a multi-byte char
		speak(data[offset:chunk_end])
		index(INTERNAL_CHUNK_INDEX)
		synth()
		pendingChunkSource.offset = chunk_end
		return
	# No active chunking: we got here because END_STRING_MARK fired and the audio for
	# the previous outlist's synth has been fed to the player.
	if waitingForDrain:
		waitingForDrain = False
	if deferredOps:
		ops = list(deferredOps)
		deferredOps.clear()
		runOps(ops)


def setPathsFromConfig():
	global ttsPath, dllName
	dllName = appConfig.dllName
	ttsPath =  appConfig.TTSPath
	if  not path.isabs(ttsPath):
		ttsPath = path.abspath(path.join(path.abspath(path.dirname(__file__)), ttsPath))


def updateIniPaths():
	iniPath = path.join(ttsPath, dllName[:-3] +"ini")
	if not path.exists(iniPath):
		# some libs don't have an ini file, so we just
		return
	ini=open(iniPath, "r+")
	ini.seek(12)
	synFile = ini.readline()[:-1]
	if path.exists(synFile):
		# the path is correct, so we don't need to change it.
		ini.close()
		return
	log.warning("The path in the IBMTTS ini file is incorrect. Updating it to the correct path. This may fail if NVDA doesn't have permission to write to the ini file, in which case the IBMTTS synth may not work.")
	tml = synFile[:-7]
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
	eciLibPath = path.join(ttsPath, dllName)
	etidevLibPath = path.join(ttsPath, "etidev.dll")
	if not path.exists(etidevLibPath):
		etidevLibPath = None
	if getFileVersionInfo(eciLibPath, 'ProductName')['ProductName'] == 'IBMECI':
		isIBM = True
	else:
		isIBM = False
	if IS_64BIT:
		return EciDLL(eciLibPath, etidevLibPath)
	if etidevLibPath:
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
	if IS_64BIT:
		avLangs = eci.eciGetAvailableLanguages()
	else:
		b=c_int()
		eci.eciGetAvailableLanguages(0,byref(b))
		avLangs=(c_int*b.value)()
		eci.eciGetAvailableLanguages(byref(avLangs),byref(b))
	if 'voice' in conf['speech']['ibmeci']:
		lang = int(conf['speech']['ibmeci']['voice'])
	else:
		lang = getVoiceByLanguage(languageHandler.getLanguage())[0]
	lang = check_lang_param(lang)
	handle = eci.eciNewEx(lang)
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
			# Also resume the ECI thread once this outlist's audio has been fed to the
			# player. Queued *after* endStringEvent so it runs strictly after every
			# bgPlay item for this outlist (the callback thread is FIFO).
			_callbackExec(_postNextChunkMessage)
			endStringReached = True
		elif lp == INTERNAL_CHUNK_INDEX:
			# Internal flow control: the engine reached the end of a chunk. Flush this
			# chunk's remaining audio, then queue the next-chunk request behind the
			# playback items so it only runs after this chunk has been fed to the
			# player. The player's backpressure (feed blocks while the previous chunk
			# is still playing) is what paces our synthesis. Not forwarded to NVDA.
			if audioStream.tell() > 0: playStream()
			sendIndexes()
			_callbackExec(_postNextChunkMessage)
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
	global callbackQueue, callbackThread, eciQueue, eciThread, idleTimer, onIndexReached, onDoneSpeaking, player, pendingChunkSource, waitingForDrain
	started.clear()
	stopped.clear()
	param_event.clear()
	pendingChunkSource = None
	deferredOps.clear()
	waitingForDrain = False
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
	if eciThread is None or not eciThread.is_alive():
		raise RuntimeError("IBMTTS Engine thread is not running. Synthesizer failure.")
	callbackQueue = queue.Queue()
	callbackThread = CallbackThread()
	callbackThread.start()


def speak(text, encoding=None):
	# deleted the following fix because is incompatible with NVDA's speech change command. Now send it from speak in ibmeci.py
	#Sometimes the synth slows down for one string of text. Why?
	#Trying to fix it here.
	# if ECIVoiceParam.eciSpeed in vparams: text = b"`vs%d%s" % (vparams[ECIVoiceParam.eciSpeed], text)
	# `encoding` is metadata used only by the chunking layer to pick safe split points;
	# the engine itself already knows the encoding from the active language.
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
	post_message_to_eciThread(WM_SILENCE, 0, 0, False)

def pause(switch):
	player.pause(switch)

def terminate():
	global callbackQueue, callbackThread, dll, eciQueue,eciThread, handle, idleTimer, onDoneSpeaking, onIndexReached, player
	try:
		post_message_to_eciThread(WM_KILL, 0, 0)
		stopped.wait()
		stopped.clear()
	except:
		log.info("Error terminating the IBMTTS thread", exc_info=True)
	callbackQueue.put((None, None, None))
	eciThread.join()
	callbackThread.join()
	idleTimer.cancel()	
	player.close()
	if IS_64BIT:
		terminate_host_32()
	callbackQueue= callbackThread= dll= eciQueue=eciThread= handle= idleTimer= onDoneSpeaking= onIndexReached= player = None


def setVoice(vl):
	vl = check_lang_param(vl)
	post_message_to_eciThread(WM_PARAM, vl, ECIParam.eciLanguageDialect)
	param_event.wait()
	param_event.clear()

def setParam(param, val):
	post_message_to_eciThread(WM_PARAM, val, param)
	param_event.wait()
	param_event.clear()

def getVParam(pr):
	return vparams[pr]

def setVParam(pr, vl):
	post_message_to_eciThread(WM_VPARAM, pr, vl)
	param_event.wait()
	param_event.clear()

def setProsodyParam(pr, vl):
	dll.eciSetVoiceParam(handle, 0, pr, vl)

def setVariant(v):
	post_message_to_eciThread(WM_COPYVOICE, v, 0)
	param_event.wait()
	param_event.clear()

def process():
		post_message_to_eciThread(WM_PROCESS, 0, 0)

def eciVersion():
	if IS_64BIT:
		return dll.eciVersion()
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

def _postNextChunkMessage():
	"""Run on the callback thread, after the player has been fed this chunk's audio.
	Asks the ECI thread to synthesize the next chunk."""
	user32.PostThreadMessageA(eciThreadId, WM_PROCESS_NEXT_CHUNK, 0, 0)


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
	try:
		currentSoundcardOutput = conf['speech']['outputDevice']
	except:
		currentSoundcardOutput = conf["audio"]["outputDevice"]
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
