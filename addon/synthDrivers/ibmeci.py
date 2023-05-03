# -*- coding: UTF-8 -*-
#Copyright (C) 2009 - 2023 David CM, released under the GPL.
# Author: David CM <dhf360@gmail.com> and others.
#synthDrivers/ibmeci.py

import six, synthDriverHandler, languageHandler, os, re
from synthDriverHandler import synthDoneSpeaking, SynthDriver, synthIndexReached, VoiceInfo

from collections import OrderedDict
from six import string_types
from logHandler import log

from synthDrivers import _ibmeci
from synthDrivers._ibmeci import ECILanguageDialect as EciLangs, ECIParam, ECIVoiceParam


# compatibility with nvda 2021.1 alpha versions.
try:
	from speech.commands import BreakCommand, CharacterModeCommand, IndexCommand, LangChangeCommand, PitchCommand, RateCommand, VolumeCommand
except ImportError:
	from speech import BreakCommand, CharacterModeCommand, IndexCommand, LangChangeCommand, PitchCommand, RateCommand, VolumeCommand

try:
	from autoSettingsUtils.driverSetting import BooleanDriverSetting,NumericDriverSetting, DriverSetting
	from autoSettingsUtils.utils import StringParameterInfo
except ImportError:
	from driverHandler import BooleanDriverSetting,NumericDriverSetting, DriverSetting

import addonHandler
addonHandler.initTranslation()


minRate=40
maxRate=156
punctuation = b"-,.:;)(?!\x96\x97"
ibm_punctuation = b"-,.:;?!\x96\x97"
ibm_pause_re = re.compile(br'([a-zA-Z0-9]|\s)([%s])(\2*?)(\s|[\\/]|$)' %ibm_punctuation)
pause_re = re.compile(br'([a-zA-Z0-9]|\s)([%s])(\2*?)(\s|[\\/]|$)' %punctuation)
time_re = re.compile(br"(\d):(\d+):(\d+)")

english_fixes = {
#	Does not occur in normal use, however if a dictionary entry contains the Mc prefix, and NVDA splits it up, the synth will crash.
	re.compile(br"\b(Mc)\s+([A-Z][a-z]|[A-Z][A-Z]+)"): br"\1\2",
	#Fixes a weird issue with the date parser. Without this fix, strings like "03 Marble" will be pronounced as "march threerd ble".
	re.compile(br"\b(\d+) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)([a-z]+)"): br"\1  \2\3",
	#Don't break UK formatted dates.
	re.compile(br"\b(\d+)  (January|February|March|April|May|June|July|August|September|October|November|December)\b"): br"\1 \2",
	#Crash words, formerly part of anticrash_res.
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
	re.compile(br"(juar)([a-z']{9,})", re.I): br"\1 \2"
}
ibm_global_fixes = {
#	Prevents the synth from spelling out everything if a punctuation mark follows a word.
	re.compile(br"([a-z]+)([~#$%^*({|\\[<%\x95])", re.I): br"\1 \2",
	#Don't break phrases like books).
	re.compile(br"([a-z]+)\s+(\(s\))", re.I): br"\1\2",
	#Removes spaces if a string is followed by a punctuation mark, since ViaVoice doesn't tolerate that.
	re.compile(br"([a-z]+|\d+|\W+)\s+([:.!;,?](?![a-z]|\d))", re.I): br"\1\2",
	#Remove the two spaces separator between strings containing left and right brackets and parentheses to reduce verbosity.
	re.compile(br'([\(\[]+)  (.)'): br'\1\2',
	re.compile(br'(.)  ([\)\]]+)'): br'\1\2',
}
english_ibm_fixes = {
	#Mostly duplicates english_fixes, but removes unneded replacements.
	#This won't crash, but ViaVoice doesn't like spaces in Mc names.
	re.compile(br"\b(Mc)\s+([A-Z][a-z]|[A-Z][A-Z]+)"): br"\1\2",
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
	re.compile(br"\b(\d+|\W+)?(\w+\_+)?(\_+)?([bcdfghjklmnpqrstvwxz]+)?(\d+)?t+z[s]che", re.I): br"\1 \2 \3 \4 \5 tz sche",
	re.compile(br"(juar)([a-z']{9,})", re.I): br"\1 \2",
	#ViaVoice-Specific crash words
	re.compile(br"(http://|ftp://)([a-z]+)(\W){1,3}([a-z]+)(/*\W){1,3}([a-z]){1}", re.I): br"\1\2\3\4 \5\6",
	re.compile(br"(\d+)([-+*^/])(\d+)(\.)(\d+)(\.)(0{2,})", re.I): br"\1\2\3\4\5\6 \7",
	re.compile(br"(\d+)([-+*^/])(\d+)(\.)(\d+)(\.)(0\W)", re.I): br"\1\2\3\4 \5\6\7",
	re.compile(br"(\d+)([-+*^/]+)(\d+)([-+*^/]+)([,.+])(0{2,})", re.I): br"\1\2\3\4\5 \6",
	re.compile(br"(\d+)(\.+)(\d+)(\.+)(0{2,})(\.\d*)\s*\.*([-+*^/])", re.I): br"\1\2\3\4 \5\6\7",
	re.compile(br"(\d+)\s*([-+*^/])\s*(\d+)(,)(00\b)", re.I): br"\1\2\3\4 \5",
	re.compile(br"(\d+)\s*([-+*^/])\s*(\d+)(,)(0{4,})", re.I): br"\1\2\3\4 \5",
	#Work around various bugs where the synth can say "comma hundred" or other similarly weird things if numbers are separated by commas by removing them in some situations. These expressions aren't perfect, but should generally work.
	re.compile(br'\b(\d{1,3}),(000),(\d{1,3})\b'): br'\1\2\3',
	re.compile(br'\b(\d{1,3}),(000),(\d{1,3}),(\d{1,3})\b'): br'\1\2\3\4',
	re.compile(br'\b(\d{1,3}),(000),(\d{1,3}),(\d{1,3}),(\d{1,3})\b'): br'\1\2\3\4\5',
	re.compile(br'\b(\d{1,3}),(000),(\d{1,3}),(\d{1,3}),(\d{1,3}),(\d{1,3})\b'): br'\1\2\3\4\5\6',
}
spanish_fixes = {
	# Euros
	re.compile(b'([\x80$]\\d{1,3})((\\s\\d{3})+\\.\\d{2})'): br'\1 \2',
	# fix 0xaa (ordinal femenino) of 13 or more digits ended in (1 2 3 6 7 9).
	re.compile(br'(\d{12,}[123679])(\xaa)'): br'\1 \2',
}
spanish_ibm_fixes = {
	#ViaVoice's time parser is slightly broken in Spanish, and will crash if the minute part goes from 20 to 59.
	#For these times, convert the periods to colons.
	re.compile(br'([0-2]?[0-4])\.([2-5][0-9])\.([0-5][0-9])'): br'\1:\2:\3',
}
spanish_ibm_anticrash = {
	re.compile(br'\b(0{1,12})(\xaa)'): br'\1 \2',
	re.compile(br'(\d{12,}[123679])(\xaa)'): br'\1 \2',
}
german_fixes = {
# Crash words.
	re.compile(br'dane-ben', re.I): br'dane- ben',
	re.compile(br'dage-gen', re.I): br'dage- gen',
	re.compile(br'(audio|video)(-)(en[bcdfghjklmnpqrsvwxz][a-z]+)', re.I): br'\1\2 \3',
}
german_ibm_fixes = {
# Just like english_ibm_fixes, also avoids unneeded replacements
	re.compile(br'dane-ben', re.I): br'dane- ben',
	re.compile(br'dage-gen', re.I): br'dage- gen',
}
portuguese_ibm_fixes = {
	re.compile(br'(\d{1,2}):(00):(\d{1,2})'): br'\1:\2 \3',
}
french_fixes = {
	# Convert n  to num ro
	re.compile(br'\bn\xb0', re.I): b'num\xe9ro',
	# anticrash for "quil" that sometimes breaks Eloquence
	# but, depending on the context, "quil" does not always pronounce the same
	re.compile(br'(?<=anq)uil(?=l)', re.I): br'i',
	re.compile(br'quil(?=\W)', re.I | re.L): br'kil',
	# Fixes function keys names (f1 to f12) that are pronounced 1 franc... 12 francs
	re.compile(br'f(?=\s?\d)', re.I | re.L): br'f ',
	# fix for capitalised roman numbers followed by 'e' or 'eme' which are broken by NVDA
	# for example IIIe (third) is parsed in II Ie	
	re.compile(br'\b([CDILMVX]+)(\s?)([CDILMVX]e)(me)?\b'): b'\\1\\3',
	# fix right parenthesis inside a word which is always spoken despite the punctuation level
	re.compile(br'(\w\))(?=\w)', re.I | re.L): br'\1 ',
	re.compile(br'(n\s?vda)', re.I): b' \xe8nv\xe9d\xe9a ',
	# In some situations letter 'y' is completely ignored
	re.compile(br'([ou])y([bnp])', re.I): br"\1i\2",
}
french_ibm_fixes = {
	re.compile(br'([$\x80\xa3])\s*(\d+)\s(000)'): br'\1\2\3',
	re.compile(br'(\d+)\s(000)\s*([$\x80\xa3])'): br'\1\2\3',
}

variants = {
	1:"Reed",
	2:"Shelley",
	3:"Sandy",
	4:"Rocko",
	5:"Glen",
	6:"FastFlo",
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
	"es_MX":b"`l2.1",
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
		NumericDriverSetting("hsz", _("Hea&d size"), False),
		NumericDriverSetting("rgh", _("Rou&ghness"), False),
		NumericDriverSetting("bth", _("Breathi&ness"), False),
		BooleanDriverSetting("backquoteVoiceTags", _("Enable backquote voice &tags"), False),
		BooleanDriverSetting("ABRDICT", _("Enable &abbreviation expansion"), False),
		BooleanDriverSetting("phrasePrediction", _("Enable phras&e prediction"), False),
		BooleanDriverSetting("shortPause", _("&Shorten pauses"), False, defaultVal=True),
		BooleanDriverSetting("sendParams", _("Al&ways Send Current Speech Settings"), False, defaultVal=True),
		DriverSetting('sampleRate', _("Sa&mple Rate"), defaultVal='1'),
		)
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
		self.currentEncoding = "mbcs"
		self.sampleRate = '1'

	PROSODY_ATTRS = {
		PitchCommand: ECIVoiceParam.eciPitchBaseline,
		VolumeCommand: ECIVoiceParam.eciVolume,
		RateCommand: ECIVoiceParam.eciSpeed,
	}

	def speak(self,speechSequence):
		last = None
		defaultLanguage=self.language
		outlist = []
		charmode=False
		if self._ABRDICT:
			_ibmeci.setParam(ECIParam.eciDictionary, 0)
		else:
			_ibmeci.setParam(ECIParam.eciDictionary, 1)
		embeds=b''
		if self._phrasePrediction:
			embeds+=b"`pp1 "
		else:
			embeds+=b"`pp0 "
		if self._sendParams:
			embeds+=b"`vv%d `vs%d " % (_ibmeci.getVParam(ECIVoiceParam.eciVolume), _ibmeci.getVParam(ECIVoiceParam.eciSpeed))
		outlist.append((_ibmeci.speak, (embeds,)))
		speechSequence= self.combine_adjacent_strings(speechSequence)
		for item in speechSequence:
			if isinstance(item, string_types):
				s = self.processText(item)
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
						self.updateEncoding(l)
				else:
					outlist.append((_ibmeci.speak, (langsAnnotations[defaultLanguage],)))
					self.speakingLanguage = defaultLanguage
			elif isinstance(item,CharacterModeCommand):
				outlist.append((_ibmeci.speak, (b"`ts1" if item.state else b"`ts0",)))
				if item.state:
					charmode=True
			elif isinstance(item,BreakCommand):
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
				if type(item) == RateCommand: val = self.percentToRate(val)
				outlist.append((_ibmeci.setProsodyParam, (self.PROSODY_ATTRS[type(item)], val)))
			else:
				log.error("Unknown speech: %s"%item)
		if last and last[-1] not in punctuation:
			# check if a pitch command is at the end of the list, because p1 need to be send before this.
			# index -2 is because -1 always seem to be an index command.
			if self._shortPause:
				if outlist[-2][0] == _ibmeci.setProsodyParam: outlist.insert(-2, (_ibmeci.speak, (b'`p1 ',)))
				else: outlist.append((_ibmeci.speak, (b'`p1 ',)))
		if charmode:
			outlist.append((_ibmeci.speak, (b"`ts0",)))
		outlist.append((_ibmeci.setEndStringMark, ()))
		outlist.append((_ibmeci.synth, ()))
		_ibmeci.eciQueue.put(outlist)
		_ibmeci.process()

	def combine_adjacent_strings(self, lst):
		""" If several strings are sent at once, combines them into one large string so regular expressions can match on it, most useful for the date bug in English, but improves the experience for IBMTTS as well. """
		result = []
		current_string = ''
		for item in lst:
			if isinstance(item, str):
				current_string += item
			else:
				if current_string:
					result.append(current_string)
					current_string = ''
				result.append(item)
		if current_string:
			result.append(current_string)
		return result
	def processText(self,text):
		#this converts to ansi for anticrash. If this breaks with foreign langs, we can remove it.
		text = text.encode(self.currentEncoding, 'replace') # special unicode symbols may encode to backquote. For this reason, backquote processing is after this.
		text = text.rstrip()
		# language crash fixes.
		curLang = _ibmeci.params[_ibmeci.ECIParam.eciLanguageDialect]
		if _ibmeci.isIBM:
			text = resub(ibm_global_fixes, text)
			if curLang in (EciLangs.GeneralAmericanEnglish, EciLangs.BritishEnglish, EciLangs.MandarinChinese, EciLangs.StandardKorean, EciLangs.HongKongCantonese):
				text = resub(english_ibm_fixes, text)
			elif curLang in ('esp', EciLangs.CastilianSpanish):
				text = resub(spanish_ibm_fixes, text)
			elif curLang in (EciLangs.CastilianSpanish,  EciLangs.MexicanSpanish):
				text = resub(spanish_ibm_anticrash, text)
			elif curLang in ('fra', EciLangs.StandardFrench):
				text = resub(french_ibm_fixes, text)
			elif curLang in ('ptb', EciLangs.BrazilianPortuguese):
				text = resub(portuguese_ibm_fixes, text)
			elif curLang in ('deu', EciLangs.StandardGerman):
				text = resub(german_ibm_fixes, text)
		else:
			if curLang in (EciLangs.GeneralAmericanEnglish, EciLangs.BritishEnglish, EciLangs.MandarinChinese, EciLangs.StandardKorean):
				text = resub(english_fixes, text) #Applies to all languages with dual language support.
			elif curLang in (EciLangs.CastilianSpanish,  EciLangs.MexicanSpanish):
				text = resub(spanish_fixes, text)
			elif curLang in (EciLangs.StandardFrench, EciLangs.CanadianFrench):
				text = resub(french_fixes, text)
			if curLang in ('deu', EciLangs.StandardGerman):
				text = resub(german_fixes, text)
		if not self._backquoteVoiceTags:
			text=text.replace(b'`', b' ') # no embedded commands
		if self._shortPause:
			if _ibmeci.isIBM:
				text = ibm_pause_re.sub(br'\1 `p1\2\3\4', text) # this enforces short, JAWS-like pauses.
			else:
				text = pause_re.sub(br'\1 `p1\2\3\4', text) # this enforces short, JAWS-like pauses.
		if not _ibmeci.isIBM:
			text = time_re.sub(br'\1:\2 \3', text) # apparently if this isn't done strings like 2:30:15 will only announce 2:30
		return text

	def pause(self,switch):
		_ibmeci.pause(switch)

	def terminate(self):
		_ibmeci.terminate()

	_backquoteVoiceTags=False
	_ABRDICT=False
	_phrasePrediction=False
	_shortPause=True
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
	def _get_shortPause(self):
		return self._shortPause
	def _set_shortPause(self, enable):
		if enable == self._shortPause:
			return
		self._shortPause = enable
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
		if lang == EciLangs.MandarinChinese:
			self.currentEncoding = "gb18030"
		elif lang == EciLangs.StandardJapanese:
			self.currentEncoding = "cp932"
		elif lang == EciLangs.StandardKorean:
			self.currentEncoding = "cp949"
		elif lang == EciLangs.HongKongCantonese:
			self.currentEncoding = "big5"
		else:
			self.currentEncoding = "mbcs"

	def _get_availableSamplerates(self):
		rates = {}
		rates["0"] = StringParameterInfo("0", "8 kHz")
		rates["1"] = StringParameterInfo("1", "11 kHz")
		if _ibmeci.isIBM:
			rates["2"] = StringParameterInfo("2", "22 kHz")
		return rates

	def _set_sampleRate(self, val):
		val = int(val)
		if val == 2 and not _ibmeci.isIBM:
			val = 1
		self._sample_rate = val
		if _ibmeci.player is not None:
			self.cancel()
		_ibmeci.setParam(_ibmeci.ECIParam.eciSampleRate, val)
		_ibmeci.player = _ibmeci.createPlayer(val)

	def _get_sampleRate(self):
		return str(self._sample_rate)

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

	def _get_variant(self): return self._variant

	def _onIndexReached(self, index): synthIndexReached.notify(synth=self, index=index)

	def _onDoneSpeaking(self): synthDoneSpeaking.notify(synth=self)

def resub(dct, s):
	for r in six.iterkeys(dct):
		s = r.sub(dct[r], s)
	return s
