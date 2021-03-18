# -*- coding: UTF-8 -*-
#Copyright (C) 2009 - 2019 David CM, released under the GPL.
# Author: David CM <dhf360@gmail.com> and others.
#synthDrivers/ibmeci.py

import six, synthDriverHandler, languageHandler, config, os, re
try:
	from speech.commands import IndexCommand, CharacterModeCommand, LangChangeCommand, BreakCommand, PitchCommand, RateCommand, VolumeCommand
except ImportError:
	from speech import IndexCommand, CharacterModeCommand, LangChangeCommand, BreakCommand, PitchCommand, RateCommand, VolumeCommand
from collections import OrderedDict
from six import string_types
from synthDriverHandler import SynthDriver,VoiceInfo
from logHandler import log
from synthDrivers import _ibmeci
from synthDrivers._ibmeci import ECIVoiceParam
import addonHandler
addonHandler.initTranslation()

try: # for python 2.7
	unicode
	from synthDriverHandler import BooleanSynthSetting as BooleanDriverSetting,NumericSynthSetting as NumericDriverSetting
	
	class synthIndexReached:
		@classmethod
		def notify (cls, synth=None, index=None): pass
	synthDoneSpeaking = synthIndexReached
except:
	from autoSettingsUtils.driverSetting import BooleanDriverSetting,NumericDriverSetting
	from synthDriverHandler import synthIndexReached, synthDoneSpeaking
	def unicode(s): return s

minRate=40
maxRate=156
punctuation = b"-,.:;)(?!"
pause_re = re.compile(br'([a-zA-Z])([%s])( |$)' %punctuation)
time_re = re.compile(br"(\d):(\d+):(\d+)")

anticrash_res = {
	re.compile(br'\b(|\d+|\W+)?(|un|anti|re)c(ae|\xe6)sur', re.I): br'\1\2seizur',
	re.compile(br"\b(|\d+|\W+)h'(r|v)[e]", re.I): br"\1h ' \2 e",
	re.compile(br"\b(\w+[bdflmnrvzqh])(h[he]s)([bcdfgjklmnprtw]\w+)\b", re.I): br"\1 \2\3",
	re.compile(br"(\d):(\d\d[snrt][tdh])", re.I): br"\1 \2",
	re.compile(br"([hjsxz])'([bdfhjklpstvxz']+)'([rtv][aeiou]?)", re.I): br"h \1 \2 \3",
	re.compile(br"(re|un|non|anti)cosp", re.I): br"\1kosp",
	re.compile(br"(anti|non|re|un)caesure", re.I): br"\1ceasure",
	re.compile(br"(EUR[A-Z]+)(\d+)", re.I): br"\1 \2",
	re.compile(br"\b(|\d+|\W+)?t+z[s]che", re.I): br"\1tz sche"
	}

english_fixes = {
	re.compile(r'(\w+)\.([a-zA-Z]+)'): r'\1 dot \2',
	re.compile(r'([a-zA-Z0-9_]+)@(\w+)'): r'\1 at \2',
}

french_fixes = { re.compile(r'([a-zA-Z0-9_]+)@(\w+)'): r'\1 arobase \2' }

spanish_fixes = {
	#for emails
	re.compile(r'([a-zA-Z0-9_]+)@(\w+)'): r'\1 arroba \2',
	re.compile(u'([€$]\d{1,3})((\s\d{3})+\.\d{2})'): r'\1 \2',
}

variants = {
	1:"Reed",
	2:"Shelley",
	3:"Bobby",
	4:"Rocko",
	5:"Glen",
	6:"Sandy",
	7:"Grandma",
	8:"Grandpa"
}

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
	supportedSettings=(SynthDriver.VoiceSetting(), SynthDriver.VariantSetting(), SynthDriver.RateSetting(),
		BooleanDriverSetting("rateBoost", _("Rate boos&t"), True),
		SynthDriver.PitchSetting(), SynthDriver.InflectionSetting(), SynthDriver.VolumeSetting(),
		NumericDriverSetting("hsz", _("Head Size"), False),
		NumericDriverSetting("rgh", _("Roughness"), False),
		NumericDriverSetting("bth", _("Breathiness"), False),
		BooleanDriverSetting("backquoteVoiceTags", _("Enable backquote voice &tags"), False))
	supportedCommands = {
		IndexCommand,
		CharacterModeCommand,
		LangChangeCommand,
		BreakCommand,
		PitchCommand,
		RateCommand,
		VolumeCommand
	}
	supportedNotifications = {synthIndexReached, synthDoneSpeaking}

	description='IBMTTS'
	name='ibmeci'
	speakingLanguage=""
	
	@classmethod
	def check(cls):
		return _ibmeci.eciCheck()

	def __init__(self):
		_ibmeci.initialize(self._onIndexReached, self._onDoneSpeaking)
		# This information doesn't really need to be displayed, and makes IBMTTS unusable if the addon is not in the same drive as NVDA executable.
		# But display it only on debug mode in case of it can be useful
		log.debug("Using IBMTTS version %s" % _ibmeci.eciVersion())
		lang = languageHandler.getLanguage()
		self.rate=50
		self.speakingLanguage=lang
		self.variant="1"

	PROSODY_ATTRS = {
		PitchCommand: ECIVoiceParam.eciPitchBaseline,
		VolumeCommand: ECIVoiceParam.eciVolume,
		RateCommand: ECIVoiceParam.eciSpeed,
	}

	def speak(self,speechSequence):
		last = None
		defaultLanguage=self.language
		outlist = []
		outlist.append((_ibmeci.speak, (b"`ts0",)))
		for item in speechSequence:
			if isinstance(item, string_types):
				s = self.processText(unicode(item))
				outlist.append((_ibmeci.speak, (s,)))
				last = s
			elif isinstance(item,IndexCommand):
				outlist.append((_ibmeci.index, (item.index,)))
			elif isinstance(item,LangChangeCommand):
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
			elif isinstance(item,CharacterModeCommand):
				outlist.append((_ibmeci.speak, (b"`ts1" if item.state else b"`ts0",)))
			elif isinstance(item,BreakCommand):
				outlist.append((_ibmeci.speak, (b' `p%d ' %item.time,)))
			elif type(item) in self.PROSODY_ATTRS:
				val = max(0, min(item.newValue, 100))
				if type(item) == RateCommand: val = self.percentToRate(val)
				outlist.append((_ibmeci.setProsodyParam, (self.PROSODY_ATTRS[type(item)], val)))
			else:
				log.error("Unknown speech: %s"%item)
		if last is not None and last[-1] not in punctuation:
			# check if a pitch command is at the end of the list, because p1 need to be send before this.
			# index -2 is because -1 always seem to be an index command.
			if outlist[-2][0] == _ibmeci.setProsodyParam: outlist.insert(-2, (_ibmeci.speak, (b'`p1. ',)))
			else: outlist.append((_ibmeci.speak, (b'`p1. ',)))
		outlist.append((_ibmeci.setEndStringMark, ()))
		outlist.append((_ibmeci.synth, ()))
		#print(outlist)
		_ibmeci.eciQueue.put(outlist)
		_ibmeci.process()

	def processText(self,text):
		text = text.rstrip()
		if _ibmeci.params[9] in (65536, 65537): text = resub(english_fixes, text)
		if _ibmeci.params[9] in (131072,  131073): text = resub(spanish_fixes, text)
		if _ibmeci.params[9] in (196609, 196608):
			text = resub(french_fixes, text)
			text = text.replace('quil', 'qil') #Sometimes this string make everything buggy with IBMTTS in French
		if self._backquoteVoiceTags:
			#this converts to ansi for anticrash. If this breaks with foreign langs, we can remove it.
			text = text.replace('`', ' ').encode('mbcs', 'replace') #no embedded commands
			text = b"`pp0 `vv%d %s" % (_ibmeci.getVParam(ECIVoiceParam.eciVolume), text)
			text = resub(anticrash_res, text)
		else:
			#this converts to ansi for anticrash. If this breaks with foreign langs, we can remove it.
			text = text.encode('mbcs', 'replace')
			text = resub(anticrash_res, text)
			text = b"`pp0 `vv%d %s" % (_ibmeci.getVParam(ECIVoiceParam.eciVolume), text.replace(b'`', b' ')) #no embedded commands
		text = pause_re.sub(br'\1 `p1\2\3', text)
		text = time_re.sub(br'\1:\2 \3', text)
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
		val = _ibmeci.getVParam(ECIVoiceParam.eciSpeed)
		if self._rateBoost: val=int(round(val/self.RATE_BOOST_MULTIPLIER))
		return self._paramToPercent(val, minRate, maxRate)

	def percentToRate(self, val):
		val = self._percentToParam(val, minRate, maxRate)
		if self._rateBoost: val = int(round(val *self.RATE_BOOST_MULTIPLIER))
		return val

	def _set_rate(self,val):
		val = self.percentToRate(val)
		self._rate = val
		_ibmeci.setVParam(ECIVoiceParam.eciSpeed, val)

	def _get_pitch(self):
		return _ibmeci.getVParam(ECIVoiceParam.eciPitchBaseline)

	def _set_pitch(self,vl):
		_ibmeci.setVParam(ECIVoiceParam.eciPitchBaseline,vl)

	def _get_volume(self):
		return _ibmeci.getVParam(ECIVoiceParam.eciVolume)

	def _set_volume(self,vl):
		_ibmeci.setVParam(ECIVoiceParam.eciVolume,int(vl))

	def _set_inflection(self,vl):
		vl = int(vl)
		_ibmeci.setVParam(ECIVoiceParam.eciPitchFluctuation,vl)

	def _get_inflection(self):
		return _ibmeci.getVParam(ECIVoiceParam.eciPitchFluctuation)

	def _set_hsz(self,vl):
		vl = int(vl)
		_ibmeci.setVParam(ECIVoiceParam.eciHeadSize,vl)

	def _get_hsz(self):
		return _ibmeci.getVParam(ECIVoiceParam.eciHeadSize)

	def _set_rgh(self,vl):
		vl = int(vl)
		_ibmeci.setVParam(ECIVoiceParam.eciRoughness,vl)

	def _get_rgh(self):
		return _ibmeci.getVParam(ECIVoiceParam.eciRoughness)

	def _set_bth(self,vl):
		vl = int(vl)
		_ibmeci.setVParam(ECIVoiceParam.eciBreathiness,vl)

	def _get_bth(self):
		return _ibmeci.getVParam(ECIVoiceParam.eciBreathiness)

	def _getAvailableVoices(self):
		o = OrderedDict()
		for name in os.listdir(_ibmeci.ttsPath):
			if name.lower().endswith('.syn'):
				info = _ibmeci.langs[name.lower()[:3]]
				o[str(info[0])] = VoiceInfo(str(info[0]), info[1], info[2])
		return o

	def _get_voice(self):
		return str(_ibmeci.params[_ibmeci.ECIParam.eciLanguageDialect])
	def _set_voice(self,vl):
		_ibmeci.set_voice(vl)

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
		_ibmeci.setVParam(ECIVoiceParam.eciSpeed, self._rate)
		#if 'ibmtts' in config.conf['speech']:
		#config.conf['speech']['ibmtts']['pitch'] = self.pitch

	def _get_variant(self): return self._variant

	def _onIndexReached(self, index): synthIndexReached.notify(synth=self, index=index)

	def _onDoneSpeaking(self): synthDoneSpeaking.notify(synth=self)

def resub(dct, s):
	for r in six.iterkeys(dct):
		s = r.sub(dct[r], s)
	return s