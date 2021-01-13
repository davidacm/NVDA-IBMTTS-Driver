# -*- coding: UTF-8 -*-
#Copyright (C) 2009 - 2019 David CM, released under the GPL.
# Author: David CM <dhf360@gmail.com> and others.
#synthDrivers/ibmeci.py

import six, synthDriverHandler, speech, languageHandler, config, os, re
from collections import OrderedDict
from six import string_types
from synthDriverHandler import SynthDriver,VoiceInfo
from logHandler import log
from synthDrivers import _ibmeci
from synthDrivers._ibmeci import ECIVoiceParam
from synthDrivers._ibmeci import isIBM
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
	from driverHandler import BooleanDriverSetting,NumericDriverSetting
	from synthDriverHandler import synthIndexReached, synthDoneSpeaking
	def unicode(s): return s

minRate=40
maxRate=156
punctuation = b"-,.:;)(?!\x96\x97"
pause_re = re.compile(br'([a-zA-Z0-9]|\s)([%s])(\2*?)(\s|[\\/]|$)' %punctuation)
time_re = re.compile(br"(\d):(\d+):(\d+)")

english_fixes = {
	#	Does not occur in normal use, however if a dictionary entry contains the Mc prefix, and NVDA splits it up, the synth will crash.
	#	Also fixes ViaVoice, as the parser is more strict there and doesn't like spaces in Mc names.
	re.compile(br"\b(Mc)\s+([A-Z][a-z]+)"): br"\1\2",
	# Fixes a weird issue with the date parser. Without this fix, strings like "03 Marble" will be pronounced as "march threerd ble".
	re.compile(br"\b(\d+) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)([a-z]+)"): br"\1  \2\3",
	# Don't break UK formatted dates.
	re.compile(br"\b(\d+)  (January|February|March|April|May|June|July|August|September|October|November|December)\b"): br"\1 \2",
	# Crash words, formerly part of anticrash_res.
	re.compile(br'\b(.*?)c(ae|\xe6)sur(e)?', re.I): br'\1seizur',
	re.compile(br"\b(|\d+|\W+)h'(r|v)[e]", re.I): br"\1h \2e",
	re.compile(br"\b(\w+[bdfhjlmnqrvz])(h[he]s)([abcdefghjklmnopqrstvwy]\w+)\b", re.I): br"\1 \2\3",
	re.compile(br"\b(\w+[bdfhjlmnqrvz])(h[he]s)(iron+[degins]?)", re.I): br"\1 \2\3",
	re.compile(br"\b(\w+'{1,}[bcdfghjklmnpqrstvwxz])'*(h+[he]s)([abcdefghijklmnopqrstvwy]\w+)\b", re.I): br"\1 \2\3",
	re.compile(br"\b(\w+[bcdfghjklmnpqrstvwxz])('{1,}h+[he]s)([abcdefghijklmnopqrstvwy]\w+)\b", re.I): br"\1 \2\3",
	re.compile(br"(\d):(\d\d[snrt][tdh])", re.I): br"\1 \2",
	re.compile(br"\b([bcdfghjklmnpqrstvwxz]+)'([bcdefghjklmnpqrstvwxz']+)'([drtv][aeiou]?)", re.I): br"\1 \2 \3",
	re.compile(br"\b(you+)'(re)+'([drv]e?)", re.I): br"\1 \2 \3",
	re.compile(br"(re|un|non|anti)cosp", re.I): br"\1kosp",
	re.compile(br"(EUR[A-Z]+)(\d+)", re.I): br"\1 \2",
	re.compile(br"\b(\d+|\W+)?(\w+\_+)?(\_+)?([bcdfghjklmnpqrstvwxz]+)?(\d+)?t+z[s]che", re.I): br"\1 \2 \3 \4 \5 tz sche",
	re.compile(br"\b(juar[aeou]s)([aeiou]{6,})", re.I): br"\1 \2"
}
english_ibm_fixes = {
	#Prevents the synth from spelling out everything if a punctuation mark follows a word.
	re.compile(br"([a-z]+)([~#$%^*({|\\[<%\x95])", re.I): br"\1 \2",
	#Don't break phrases like books).
	re.compile(br"([a-z]+)\s+(\(s\))", re.I): br"\1\2",
	#Removes spaces if a string is followed by a punctuation mark, since ViaVoice doesn't tolerate that.
	re.compile(br"([a-z]+|\d+|\W+)\s+([:.!;,])", re.I): br"\1\2",
	re.compile(br"(http://|ftp://)([a-z]+)(\W){1,3}([a-z]+)(/*\W){1,3}([a-z]){1}", re.I): br"\1\2\3\4 \5\6",
	re.compile(br"(\d+)([-+*^/])(\d+)(\.)(\d+)(\.)(0{2,})", re.I): br"\1\2\3\4\5\6 \7",
	re.compile(br"(\d+)([-+*^/])(\d+)(\.)(\d+)(\.)(0\W)", re.I): br"\1\2\3\4 \5\6\7",
	re.compile(br"(\d+)([-+*^/]+)(\d+)([-+*^/]+)([,.+])(0{2,})", re.I): br"\1\2\3\4\5 \6",
	re.compile(br"(\d+)(\.+)(\d+)(\.+)(0{2,})\s*\.*([-+*^/])", re.I): br"\1\2\3\4 \5\6",
	re.compile(br"(\d+)\s*([-+*^/])\s*(\d+)(,)(0{2,})", re.I): br"\1\2\3\4 \5",
}
spanish_fixes = {
	# Euros
	re.compile(b'([\x80$]\\d{1,3})((\\s\\d{3})+\\.\\d{2})'): r'\1 \2',
}
spanish_ibm_fixes = {
	#ViaVoice's time parser is slightly broken in Spanish, and will crash if the minute part goes from 20 to 59.
	#For these times, convert the periods to colons.
	re.compile(br'([0-2][0-4])\.([2-5][0-9])\.([0-5][0-9])'): br'\1:\2:\3',
}
german_fixes = {
# Crash words.
	re.compile(br'dane-ben', re.I): br'dane- ben',
	re.compile(br'dage-gen', re.I): br'dage- gen',
}
portuguese_ibm_fixes = {
	re.compile(br'(\d{1,2}):(00):(\d{1,2})'): br'\1:\2 \3',
}

# fixme: These are only the variant names for enu. Does ECI have a way to obtain names for other languages?
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
	"zh_CN":b"`l6.0",
	"pt":b"`l7",
	"pt_BR":b"`l7.0",
	"pt_PT":b"`l7.1",
	"ja":b"`l8",
	"ja_JP":b"`l8.0",
	"fi":b"`l9",
	"fi_FI":b"`l9.0",
	"ko":b"`l10",
	"ko_KR":b"`l10.0",
	"yue":b"`l11.1",
	"nb":b"`l13",
	"nb_NO":b"`l13.0",
	"sv":b"`l14",
	"sv_SE":b"`l14.0",
	"da":b"`l15",
	"da_DK":b"`l15.0"
}

class SynthDriver(synthDriverHandler.SynthDriver):
	supportedSettings=(SynthDriver.VoiceSetting(), SynthDriver.VariantSetting(), SynthDriver.RateSetting(),
		BooleanDriverSetting("rateBoost", _("Rate boos&t"), True),
		SynthDriver.PitchSetting(), SynthDriver.InflectionSetting(), SynthDriver.VolumeSetting(),
		NumericDriverSetting("hsz", _("Head size"), False),
		NumericDriverSetting("rgh", _("Roughness"), False),
		NumericDriverSetting("bth", _("Breathiness"), False),
		BooleanDriverSetting("backquoteVoiceTags", _("Enable backquote voice &tags"), False),
		BooleanDriverSetting("ABRDICT", _("Enable &abbreviation dictionary"), False),
		BooleanDriverSetting("phrasePrediction", _("Enable phrase prediction"), False),
		BooleanDriverSetting("shortpause", _("&Shorten pauses"), False),
		BooleanDriverSetting("sendParams", _("Always Send Current Speech Settings (enable to prevent some tags from sticking, disable for viavoice binary compatibility)"), False))
	supportedCommands = {
		speech.IndexCommand,
		speech.CharacterModeCommand,
		speech.LangChangeCommand,
		speech.BreakCommand,
		speech.PitchCommand,
		speech.RateCommand,
		speech.VolumeCommand
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
		self.currentEncoding = "mbcs"

	PROSODY_ATTRS = {
		speech.PitchCommand: ECIVoiceParam.eciPitchBaseline,
		speech.VolumeCommand: ECIVoiceParam.eciVolume,
		speech.RateCommand: ECIVoiceParam.eciSpeed,
	}

	def speak(self,speechSequence):
		last = None
		defaultLanguage=self.language
		outlist = []
		charmode=False
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
						self.updateEncoding(l)
				else:
					outlist.append((_ibmeci.speak, (langsAnnotations[defaultLanguage],)))
					self.speakingLanguage = defaultLanguage
			elif isinstance(item,speech.CharacterModeCommand):
				outlist.append((_ibmeci.speak, (b"`ts1" if item.state else b"`ts0",)))
				if item.state:
					charmode=True
			elif isinstance(item,speech.BreakCommand):
				# taken from eloquence_threshold (https://github.com/pumper42nickel/eloquence_threshold)
				# Eloquence doesn't respect delay time in milliseconds.
				# Therefore we need to adjust waiting time depending on current speech rate
				# The following table of adjustments has been measured empirically
				# Then we do linear approximation
				coefficients = {
						10:1,
						43:2,
						60:3,
						75:4,
						85:5,
				}
				ck = sorted(coefficients.keys())
				if self.rate <= ck[0]:
					factor = coefficients[ck[0]]
				elif self.rate >= ck[-1]:
					factor = coefficients[ck[-1]]
				elif self.rate in ck:
					factor = coefficients[self.rate]
				else:
					li = [index for index, r in enumerate(ck) if r<self.rate][-1]
					ri = li + 1
					ra = ck[li]
					rb = ck[ri]
					factor = 1.0 * coefficients[ra] + (coefficients[rb] - coefficients[ra]) * (self.rate - ra) / (rb-ra)
				pFactor = factor*item.time
				pFactor = int(pFactor)
				outlist.append((_ibmeci.speak, (b' `p%d '%(pFactor),)))
			elif type(item) in self.PROSODY_ATTRS:
				val = max(0, min(item.newValue, 100))
				if type(item) == speech.RateCommand: val = self.percentToRate(val)
				outlist.append((_ibmeci.setProsodyParam, (self.PROSODY_ATTRS[type(item)], val)))
			else:
				log.error("Unknown speech: %s"%item)
		if last is not None and last[-1] not in punctuation:
			# check if a pitch command is at the end of the list, because p1 need to be send before this.
			# index -2 is because -1 always seem to be an index command.
			if outlist[-2][0] == _ibmeci.setProsodyParam: outlist.insert(-2, (_ibmeci.speak, (b'`p1 ',)))
			else: outlist.append((_ibmeci.speak, (b'`p1 ',)))
		if charmode:
			outlist.append((_ibmeci.speak, (b"`ts0",)))
		outlist.append((_ibmeci.setEndStringMark, ()))
		outlist.append((_ibmeci.synth, ()))
		_ibmeci.eciQueue.put(outlist)
		_ibmeci.process()

	def processText(self,text):
		#this converts to ansi for anticrash. If this breaks with foreign langs, we can remove it.
		text = text.encode(self.currentEncoding, 'replace') # special unicode symbols may encode to backquote. For this reason, backquote processing is after this.
		text = text.rstrip()
		if _ibmeci.params[9] in (65536, 65537, 393216, 655360, 720897): text = resub(english_fixes, text) #Applies to all languages with dual language support.
		if _ibmeci.params[9] in (65536, 65537, 393216, 655360, 720897) and _ibmeci.isIBM: text = resub(english_ibm_fixes, text)
		if _ibmeci.params[9] in (131072,  131073) and not _ibmeci.isIBM: text = resub(spanish_fixes, text)
		if _ibmeci.params[9] in ('esp', 131072) and _ibmeci.isIBM: text = resub(spanish_ibm_fixes, text)
		if _ibmeci.params[9] in (196609, 196608):
			text = text.replace(br'quil', br'qil') #Sometimes this string make everything buggy with IBMTTS in French
		if  _ibmeci.params[9] in ('deu', 262144):
			text = resub(german_fixes, text)
		if  _ibmeci.params[9] in ('ptb', 458752) and _ibmeci.isIBM:
			text = resub(portuguese_ibm_fixes, text)
		if not self._backquoteVoiceTags:
			text=text.replace(b'`', b' ') # no embedded commands
		if self._shortpause:
			text = pause_re.sub(br'\1 `p1\2\3\4', text) # this enforces short, JAWS-like pauses.
		if not _ibmeci.isIBM:
			text = time_re.sub(br'\1:\2 \3', text) # apparently if this isn't done strings like 2:30:15 will only announce 2:30
		embeds=b''
		if self._ABRDICT:
			embeds+=b"`da1 "
		else:
			embeds+=b"`da0 "
		if self._phrasePrediction:
			embeds+=b"`pp1 "
		else:
			embeds+=b"`pp0 "
		if self._sendParams:
			embeds+=b"`vv%d `vs%d " % (_ibmeci.getVParam(ECIVoiceParam.eciVolume), _ibmeci.getVParam(ECIVoiceParam.eciSpeed))
		text = b"%s %s" % (embeds.rstrip(), text) # bring all the printf stuff into one call, in one string. This avoids all the concatonation and printf additions of the previous organization.
		return text
	def pause(self,switch):
		_ibmeci.pause(switch)

	def terminate(self):
		_ibmeci.terminate()

	_backquoteVoiceTags=False
	_ABRDICT=False
	_phrasePrediction=False
	_shortpause=False
	_sendParams=True
	def _get_backquoteVoiceTags(self):
		return self._backquoteVoiceTags

	def _set_backquoteVoiceTags(self, enable):
		if enable == self._backquoteVoiceTags:
			return
		self._backquoteVoiceTags = enable
	def _get_ABRDICT(self):
		return self._ABRDICT
	def _set_ABRDICT(self, enable):
		if enable == self._ABRDICT:
			return
		self._ABRDICT = enable
	def _get_phrasePrediction(self):
		return self._phrasePrediction
	def _set_phrasePrediction(self, enable):
		if enable == self._phrasePrediction:
			return
		self._phrasePrediction = enable
	def _get_shortpause(self):
		return self._shortpause
	def _set_shortpause(self, enable):
		if enable == self._shortpause:
			return
		self._shortpause = enable
	def _get_sendParams(self):
		return self._sendParams
	def _set_sendParams(self, enable):
		if enable == self._sendParams:
			return
		self._sendParams = enable
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
		_ibmeci.setVoice(int(vl))
		self.updateEncoding(int(vl))

	def updateEncoding(self, lang): # lang must be a number asociated with IBMTTS languages or a string with an annotation language.
		# currently we don't need to consider the decimal part for the conversion.
		if isinstance(lang, bytes): lang = int(float(lang[2:])) * 65536
		#chinese
		if lang == 393216: self.currentEncoding = "gb2312"
		# japan
		elif lang == 524288: self.currentEncoding = "cp932"
		# korean
		elif lang == 655360: self.currentEncoding = "cp949"
		elif lang == 720897: self.currentEncoding = "big5"
		else: self.currentEncoding = "mbcs"

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