#coding=utf-8
#Copyright (C) 2009 - 2019 David CM, released under the GPL.
#synthDrivers/ibmeci.py

import synthDriverHandler, speech, languageHandler, config, os, re
from collections import OrderedDict
from six import string_types
from synthDriverHandler import SynthDriver,VoiceInfo,BooleanSynthSetting,NumericSynthSetting
from logHandler import log
import _ibmeci
import addonHandler
addonHandler.initTranslation()

try:
	unicode
except:
	def unicode(s):
		return s


punctuation = [x for x in "-,.?!:;"]
minRate=0
maxRate=156

pause_re = re.compile(br'([a-zA-Z])([-.(),:;!?])( |$)')
time_re = re.compile(br"(\d):(\d+):(\d+)")

anticrash_res = {
	re.compile(br'\b(|\d+|\W+)(|un|anti|re)c(ae|\xe6)sur', re.I): br'\1\2seizur',
	re.compile(br"\b(|\d+|\W+)h'(r|v)[e]", re.I): br"\1h ' \2 e",
# re.compile(r"\b(|\d+|\W+)wed[h]esday", re.I): r"\1wed hesday",
re.compile(br'hesday'): b' hesday',
		re.compile(br"\b(|\d+|\W+)tz[s]che", re.I): br"\1tz sche"
}

english_fixes = {
re.compile(r'(\w+)\.([a-zA-Z]+)'): r'\1 dot \2',
re.compile(r'([a-zA-Z0-9_]+)@(\w+)'): r'\1 at \2',
}
french_fixes = {
re.compile(r'([a-zA-Z0-9_]+)@(\w+)'): r'\1 arobase \2',
}
spanish_fixes = {
#for emails
re.compile(r'([a-zA-Z0-9_]+)@(\w+)'): r'\1 arroba \2',
re.compile(u'([€$]\d{1,3})((\s\d{3})+\.\d{2})'): r'\1 \2',
}


variants = {1:"Reed",
2:"Shelley",
3:"Bobby",
4:"Rocko",
5:"Glen",
6:"Sandy",
7:"Grandma",
8:"Grandpa"}

# For langChangeCommand
langsAnnotations={
"en":b"`l1",
"en_US":b"`l1.0",
"en_UK":b"`l1.1",
"en_GB":b"`l1.1",
"es":b"`l2",
"es_ES":b"`l2.0",
"es_ME":b"`l2.1",
"fr":b"`l3",
"fr_FR":b"`l3.0",
"fr_CA":b"`l3.1",
"de":b"`l4",
"de_DE":b"`l4",
"it":b"`l5",
"it_IT":b"`l5",
"zh":b"`l6",
"zh_gb":b"`l6.0",
"pt":b"`l7",
"pt_BR":b"`l7.0",
"pt_PT":b"`l7.1",
"ja":b"`l8",
"ja_ja":b"`l8.0",
"ko":b"`l10",
"ko_ko":b"`l10.0",
"fi":b"`l9",
"fi_FI":b"`l9.0"
}

class SynthDriver(synthDriverHandler.SynthDriver):
	supportedSettings=(SynthDriver.VoiceSetting(), SynthDriver.VariantSetting(),
	SynthDriver.RateSetting(), BooleanSynthSetting("rateBoost", _("Rate boos&t")),
	SynthDriver.PitchSetting(), SynthDriver.InflectionSetting(), SynthDriver.VolumeSetting(), NumericSynthSetting("hsz", _("Head Size"), False), NumericSynthSetting("rgh", _("Roughness"), False), NumericSynthSetting("bth", _("Breathiness"), False), BooleanSynthSetting("backquoteVoiceTags", _("Enable backquote voice &tags"), False))
	description='IBMTTS'
	name='ibmeci'
	speakingLanguage=""
	@classmethod
	def check(cls):
		return _ibmeci.eciCheck()
		
	def __init__(self):
		_ibmeci.initialize()
		# This information doesn't really need to be displayed, and makes IBMTTS unusable if the addon is not in the same drive as NVDA executable.
		# But display it only on debug mode in case of it can be useful
		log.debug("Using IBMTTS version %s" % _ibmeci.eciVersion())
		lang = languageHandler.getLanguage()
		self.rate=50
		self.speakingLanguage=lang
		self.variant="1"


	def speak(self,speechSequence):
		last = None
		defaultLanguage=self.language
		outlist = []
		for item in speechSequence:
			if isinstance(item, string_types):
				s = self.processText(unicode(item))
				outlist.append((_ibmeci.speak, (s,)))
				last = s
			elif isinstance(item,speech.IndexCommand):
				outlist.append((_ibmeci.index, (item.index,)))
			elif isinstance(item,speech.LangChangeCommand):
				l=None
				if item.lang in langsAnnotations: l = langsAnnotations[item.lang]
				elif item.lang and item.lang[0:2] in langsAnnotations: l = langsAnnotations[item.lang[0:2]]
				if l:
					if item.lang != self.speakingLanguage and item.lang != self.speakingLanguage[0:2]:
						outlist.append((_ibmeci.speak, (l,)))
						self.speakingLanguage=item.lang
				else:
					outlist.append((_ibmeci.speak, (langsAnnotations[defaultLanguage],)))
					self.speakingLanguage = defaultLanguage
			elif isinstance(item,speech.CharacterModeCommand):
				outlist.append((_ibmeci.speak, (b"`ts1" if item.state else "b`ts0",)))
			elif isinstance(item,speech.SpeechCommand):
				log.debugWarning("Unsupported speech command: %s"%item)
			else:
				log.error("Unknown speech: %s"%item)
		if last is not None and not last[-1] in punctuation: outlist.append((_ibmeci.speak, (b'`p1.',)))
		outlist.append((_ibmeci.setEndStringMark, (None,)))
		
		outlist.append((_ibmeci.speak, (b"`ts0",)))
		outlist.append((_ibmeci.synth,()))
		_ibmeci.synthQueue.put(outlist)
		_ibmeci.process()

	def processText(self,text):
		text = text.rstrip()
		if _ibmeci.params[9] in (65536, 65537): text = resub(english_fixes, text)
		if _ibmeci.params[9] in (131072,  131073): text = resub(spanish_fixes, text)
		if _ibmeci.params[9] in (196609, 196608):
			text = resub(french_fixes, text)
			text = text.replace('quil', 'qil') #Sometimes this string make everything buggy with IBMTTS in French
		#if not self._backquoteVoiceTags: text = text.replace(u'‵', ' ')
		if self._backquoteVoiceTags:
			text = "`pp0 `vv%d %s" % (self.getVParam(_ibmeci.vlm), text.replace('`', ' ')) #no embedded commands
			text = resub(anticrash_res, text)
			#this converts to ansi for anticrash. If this breaks with foreign langs, we can remove it.
			text = text.encode('mbcs', 'replace')
		else:
			#this converts to ansi for anticrash. If this breaks with foreign langs, we can remove it.
			text = text.encode('mbcs', 'replace')
			text = resub(anticrash_res, text)
			text = b"`pp0 `vv%d %s" % (self.getVParam(_ibmeci.vlm), text.replace(b'`', b' ')) #no embedded commands
		text = pause_re.sub(br'\1 `p1\2\3', text)
		text = time_re.sub(br'\1:\2 \3', text)
		# temporal fix: replace , with `" -" because IBMTTS seems ignore commas at the end.
		# if you know a better solution please let me know to update it.
		if text[-1] == b",": text = text[0:-1]+b" -"
		return text



	def pause(self,switch):
		_ibmeci.pause(switch)

	def terminate(self):
		_ibmeci.terminate()

	_backquoteVoiceTags=False
	def _get_backquoteVoiceTags(self):
		return self._backquoteVoiceTags

	def _set_backquoteVoiceTags(self, enable):
		if enable == self._backquoteVoiceTags:
			return
		self._backquoteVoiceTags = enable

	_rateBoost = False
	RATE_BOOST_MULTIPLIER = 1.6
	def _get_rateBoost(self):
		return self._rateBoost

	def _set_rateBoost(self, enable):
		if enable != self._rateBoost:
			rate = self.rate
			self._rateBoost = enable
			self.rate = rate


	def _get_rate(self):
		val = self.getVParam(_ibmeci.rate)
		if self._rateBoost: val=int(round(val/self.RATE_BOOST_MULTIPLIER))
		return self._paramToPercent(val, minRate, maxRate)

	def _set_rate(self,vl):
		val = self._percentToParam(vl, minRate, maxRate)
		if self._rateBoost: val = int(round(val *self.RATE_BOOST_MULTIPLIER))
		self._rate = val
		self.setVParam(_ibmeci.rate, val)

	def _get_pitch(self):
		return self.getVParam(_ibmeci.pitch)

	def _set_pitch(self,vl):
		self.setVParam(_ibmeci.pitch,vl)

	def _get_volume(self):
		return self.getVParam(_ibmeci.vlm)

	def _set_volume(self,vl):
		self.setVParam(_ibmeci.vlm,int(vl))

	def _set_inflection(self,vl):
		vl = int(vl)
		self.setVParam(_ibmeci.fluctuation,vl)

	def _get_inflection(self):
		return self.getVParam(_ibmeci.fluctuation)

	def _set_hsz(self,vl):
		vl = int(vl)
		self.setVParam(_ibmeci.hsz,vl)

	def _get_hsz(self):
		return self.getVParam(_ibmeci.hsz)

	def _set_rgh(self,vl):
		vl = int(vl)
		self.setVParam(_ibmeci.rgh,vl)

	def _get_rgh(self):
		return self.getVParam(_ibmeci.rgh)

	def _set_bth(self,vl):
		vl = int(vl)
		self.setVParam(_ibmeci.bth,vl)

	def _get_bth(self):
		return self.getVParam(_ibmeci.bth)

	def _getAvailableVoices(self):
		o = OrderedDict()
		for name in os.listdir(_ibmeci.ttsPath):
			if name.lower().endswith('.syn'):
				info = _ibmeci.langs[name.lower()[:3]]
				o[str(info[0])] = VoiceInfo(str(info[0]), info[1], info[2])
		return o

	def _get_voice(self):
		return str(_ibmeci.params[9])
	def _set_voice(self,vl):
		_ibmeci.set_voice(vl)
	def getVParam(self,pr):
		return _ibmeci.getVParam(pr)

	def setVParam(self, pr,vl):
		_ibmeci.setVParam(pr, vl)

	def _get_lastIndex(self):
#fix?
		return _ibmeci.lastindex

	def cancel(self):
		_ibmeci.stop()

	def _getAvailableVariants(self):
		global variants
		return OrderedDict((str(id), synthDriverHandler.VoiceInfo(str(id), name)) for id, name in variants.items())

	def _set_variant(self, v):
		global variants
		self._variant = v if int(v) in variants else "1"
		_ibmeci.setVariant(int(v))
		self.setVParam(_ibmeci.rate, self._rate)
#  if 'ibmtts' in config.conf['speech']:
#   config.conf['speech']['ibmtts']['pitch'] = self.pitch

	def _get_variant(self): return self._variant


def resub(dct, s):
	for r in dct.keys():
		s = r.sub(dct[r], s)
	return s
