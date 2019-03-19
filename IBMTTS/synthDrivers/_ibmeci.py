#Copyright (C) 2009 - 2018 David CM, released under the GPL.

import threading, time, nvwave, config, languageHandler
from ctypes import *
from io import BytesIO
from os import path
from logHandler import log

try:
	# Python 2.7 imports
	import Queue as queue 
except ImportError:
	# Python 3 import
	import queue
import addonHandler
addonHandler.initTranslation()


gb = BytesIO()
speaking=False
user32 = windll.user32
eci = None
tid = None
bgt = None
samples=3300
buffer = create_string_buffer(samples*2)
bgQueue = queue.Queue()
synth_queue = queue.Queue()
stopped = threading.Event()
started = threading.Event()
param_event = threading.Event()
Callback = WINFUNCTYPE(c_int, c_int, c_int, c_int, c_void_p)
hsz=1
pitch=2
fluctuation=3
rgh=4
bth=5
rate=6
vlm=7
lastindex=0

langs={'esp': (131072, _('Castilian Spanish'), 'es_ES', 'es'),
'esm': (131073, _('Latin American Spanish'), 'es_ME', 'es_CO'),
'ptb': (458752, _('Brazilian Portuguese'), 'pt_BR', 'pt'),
'fra': (196608, _('French'), 'fr_FR', 'fr'),
'frc': (196609, _('French Canadian'), 'fr_CA', ''),
'fin': (589824, _('Finnish'), 'fi_FI', 'fi'),
'chs': (393216, _('Chinese'), 'zh_GB', 'zh'),
'jpn': (524288, _('Japanese'), 'ja_JA', 'jp'),
'kor': (655360, _('Korean'), 'ko_KO', 'ko'),
'deu': (262144, _('German'), 'de_DE', 'de'),
'ita': (327680, _('Italian'), 'it_IT', 'it'),
'enu': (65536, _('American English'), 'en_US', 'en'),
'eng': (65537, _('British English'), 'en_UK', '')}

avLangs=0
synthPath=""
dllName=""
WM_PROCESS = 1025
WM_SILENCE = 1026
WM_PARAM = 1027
WM_VPARAM=1028
WM_COPYVOICE=1029
WM_KILL=1030
WM_SYNTH=1031
WM_INDEX=1032
params = {}
vparams = {}

audio_queue = queue.Queue()
#We can only have one of each in NVDA. Make this global
dll = None
handle = None

class eciThread(threading.Thread):
	def run(self):
		global vparams, params, speaking
		global tid, dll, handle
		tid = windll.kernel32.GetCurrentThreadId()
		msg = wintypes.MSG()
		user32.PeekMessageA(byref(msg), None, 0x400, 0x400, 0)
		(dll, handle) = eciNew()
		dll.eciRegisterCallback(handle, callback, None)
		dll.eciSetOutputBuffer(handle, samples, pointer(buffer))
		dll.eciSetParam(handle,1, 1)
		dll.eciSetParam(handle,3, 1) #dictionary off
		self.dictionaryHandle = dll.eciNewDict(handle)
		dll.eciSetDict(handle, self.dictionaryHandle)
#0 = main dictionary
		if path.exists(path.join(synthPath, "main.dic")):
			dll.eciLoadDict(handle, self.dictionaryHandle, 0, path.join(synthPath, "main.dic"))
		if path.exists(path.join(synthPath, "root.dic")):
			dll.eciLoadDict(handle, self.dictionaryHandle, 1, path.join(synthPath, "root.dic"))
		params[9] = dll.eciGetParam(handle, 9)
		started.set()
		while True:
			user32.GetMessageA(byref(msg), 0, 0, 0)
			user32.TranslateMessage(byref(msg))
			if msg.message == WM_PROCESS:
				internal_process_queue()
			elif msg.message == WM_SILENCE:
				speaking=False
				gb.seek(0)
				gb.truncate(0)
				dll.eciStop(handle)
				try:
					while True:
						bgQueue.get_nowait()
				except:
						pass
				player.stop()
			elif msg.message == WM_PARAM:
				dll.eciSetParam(handle, msg.lParam, msg.wParam)
				params[msg.lParam] = msg.wParam
				param_event.set()
			elif msg.message == WM_VPARAM:
				(param, val) = msg.wParam, msg.lParam
#don't set unless we have to
#This doesn't fix the rate problem, though.
#    if param in vparams and vparams[param] == val: continue
				dll.eciSetVoiceParam(handle, 0, msg.wParam, msg.lParam)
				vparams[msg.wParam] = msg.lParam
				param_event.set()
			elif msg.message == WM_COPYVOICE:
				dll.eciCopyVoice(handle, msg.wParam, 0)
				for i in (rate, pitch, vlm, fluctuation, hsz, rgh, bth):
					vparams[i] = dll.eciGetVoiceParam(handle, 0, i)
				param_event.set()
			elif msg.message == WM_KILL:
				dll.eciDelete(handle)
				stopped.set()
				break
			else:
				user32.DispatchMessageA(byref(msg))

def eciCheck():
	global synthPath, dllName
	synthPath=path.abspath(path.dirname(__file__))
	f  =open(path.join(synthPath, "ibmtts.cfg"), "r")
	cfg = {k[0].strip(): k[1].strip() for k in [k.split("=") for k in f.readlines()]}
	f.close()
	dllName = cfg['dllName']
	if  path.isabs(cfg['TTSPath']):
		synthPath = cfg['TTSPath']
	else:
		synthPath = path.join(synthPath, cfg['TTSPath'])
		iniCheck()
	return path.exists(synthPath)

def iniCheck():
	ini=open(path.join(synthPath, dllName[:-3] +"ini"), "r+")
	ini.seek(12)
	tml=ini.readline()[:-9]
	if tml != synthPath:
		ini.seek(12)
		tmp=ini.read()
		ini.seek(12)
		ini.write(tmp.replace(tml, synthPath))
		ini.truncate()
	ini.close()

def eciNew():
	global avLangs
	eciCheck()
	eci = windll.LoadLibrary(path.join(synthPath, dllName))
	b=c_int()
	eci.eciGetAvailableLanguages(0,byref(b))
	avLangs=(c_int*b.value)()
	eci.eciGetAvailableLanguages(byref(avLangs),byref(b))
	if 'ibmtts' in config.conf['speech'] and config.conf['speech']['ibmtts']['voice'] != '':
		handle=eci.eciNewEx(int(config.conf['speech']['ibmtts']['voice']))
	else: handle=eci.eciNewEx(getVoiceByLanguage(languageHandler.getLanguage())[0])
	for i in (rate, pitch, vlm, fluctuation, hsz, rgh, bth):
		vparams[i] = eci.eciGetVoiceParam(handle, 0, i)
	return eci,handle

@WINFUNCTYPE(c_int,c_int,c_int,c_long,c_void_p)
def _bgExec(func, *args, **kwargs):
	global bgQueue
	bgQueue.put((func, args, kwargs))
def setLast(lp):
	global lastindex
	lastindex = lp
	#we can use this to set player idle
# player.idle()
def bgPlay(stri):
	if len(stri) == 0: return
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
		except:
			player.idle()
			time.sleep(0.02)
			tries += 1
	log.error("Eloq speech failed to feed one buffer.")

curindex=None
@Callback
def callback (h, ms, lp, dt):
	global gb, curindex, speaking
	if not speaking:
		return 2
#We need to buffer x amount of audio, and send the indexes after it.
#Accuracy is lost with this method, but it should stop the say all breakage.

	if speaking and ms == 0: #audio data
		gb.write(string_at(buffer, lp*2))
		if gb.tell() >= samples*2:
			_bgExec(bgPlay, gb.getvalue())
			if curindex is not None:
				_bgExec(setLast, curindex)
				curindex=None
			gb.truncate(0)
			gb.seek(0)
	elif ms==2: #index
		if lp != 0xffff: #end of string
			curindex = lp
		else: #We reached the end of string
			if gb.tell() >= 0:
				_bgExec(bgPlay, gb.getvalue())
				gb.seek(0)
				gb.truncate(0)
			if curindex is not None:
				_bgExec(setLast, curindex)
				curindex=None
	return 1

class BgThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.setDaemon(True)

	def run(self):
		global isSpeaking
		try:
			while True:
				func, args, kwargs = bgQueue.get()
				if not func:
					break
				func(*args, **kwargs)
				bgQueue.task_done()
		except:
			log.error("bgThread.run", exc_info=True)

def _bgExec(func, *args, **kwargs):
	global bgQueue
	bgQueue.put((func, args, kwargs))
def str2mem(str):
	buf = c_buffer(str)
	blen = sizeof(buf)
	ptr = windll.kernel32.GlobalAlloc(0x40, blen)
	cdll.msvcrt.memcpy(ptr, addressof(buf), blen)
	return ptr

def initialize():
	global eci, player, bgt, dll, handle
	player = nvwave.WavePlayer(1, 11025, 16, outputDevice=config.conf["speech"]["outputDevice"])
	eci = eciThread()
	eci.start()
	started.wait()
	started.clear()
	bgt = BgThread()
	bgt.start()

def speak(text):
#Sometimes the synth slows down for one string of text. Why?
#Trying to fix it here.
	if rate in vparams: text = b"`vs%d%s" % (vparams[rate], text)
	dll.eciAddText(handle, text)

def index(x):
	dll.eciInsertIndex(handle, x)

def synth():
	global speaking
	speaking = True
	dll.eciSynthesize(handle)

def stop():
	user32.PostThreadMessageA(tid, WM_SILENCE, 0, 0)

def pause(switch):
	player.pause(switch)

def terminate():
	global bgt, player
	user32.PostThreadMessageA(tid, WM_KILL, 0, 0)
	stopped.wait()
	stopped.clear()
	bgQueue.put((None, None, None))
	eci.join()
	bgt.join()
	player.close()
	player = None
	bgt = None

def set_voice(vl):
		user32.PostThreadMessageA(tid, WM_PARAM, int(vl), 9)

def getVParam(pr):
	return vparams[pr]

def setVParam(pr, vl):
	user32.PostThreadMessageA(tid, WM_VPARAM, pr, vl)
	param_event.wait()
	param_event.clear()

def setVariant(v):
	user32.PostThreadMessageA(tid, WM_COPYVOICE, v, 0)
	param_event.wait()
	param_event.clear()

def process():
		user32.PostThreadMessageA(tid, WM_PROCESS, 0, 0)

def internal_process_queue():
	lst = synth_queue.get()
	for (func, args) in lst:
		func(*args)

def eciVersion():
	ptr="       "
	dll.eciVersion(ptr)
	return ptr

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
