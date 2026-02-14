# -*- coding: utf-8 -*-
# Copyright (C) 2009 - 2023 David CM, released under the GPL.
# Author: David CM <dhf360@gmail.com> and others.
# synthDrivers/ibmeci.py - Proxy 64-bit for synthDriverHost32

import os
from _bridge.clients.synthDriverHost32.synthDriver import SynthDriverProxy32
from _bridge.clients.synthDriverHost32 import launcher

HAS_SYNTHDRIVER_HOST32 = (
    hasattr(launcher, "isSynthDriverHost32RuntimeAvailable")
    and launcher.isSynthDriverHost32RuntimeAvailable()
)

# Metadados definidos localmente (sem import do 32-bit)
from synthDriverHandler import SynthDriver as SynthDriverBase, synthIndexReached, synthDoneSpeaking
from speech.commands import BreakCommand, CharacterModeCommand, IndexCommand, LangChangeCommand, PitchCommand, RateCommand, VolumeCommand

try:
    from autoSettingsUtils.driverSetting import BooleanDriverSetting, NumericDriverSetting, DriverSetting
except ImportError:
    from driverHandler import BooleanDriverSetting, NumericDriverSetting, DriverSetting

import addonHandler
addonHandler.initTranslation()

from collections import OrderedDict


# Simple class to replace StringParameterInfo in synthDriverHost32
class StringParameterInfo:
    def __init__(self, id, displayName):
        self.id = id
        self.displayName = displayName


# Pause modes for synthDriverHost32
_pauseModes = {
    "0": StringParameterInfo("0", _("Do not shorten")),
    "1": StringParameterInfo("1", _("Shorten at end of text only")),
    "2": StringParameterInfo("2", _("Shorten all pauses"))
}

# Sample rates for synthDriverHost32
_sampleRates = {
    "0": StringParameterInfo("0", _("8 kHz")),
    "1": StringParameterInfo("1", _("11 kHz")),
}

# Variants for synthDriverHost32
_variants = {
    "1": "Reed",
    "2": "Shelley",
    "3": "Sandy",
    "4": "Rocko",
    "5": "Glen",
    "6": "FastFlo",
    "7": "Grandma",
    "8": "Grandpa"
}


def _get_availablePauseModes():
    from collections import OrderedDict
    try:
        from autoSettingsUtils.utils import StringParameterInfo as SPI
        return OrderedDict([
            ("0", SPI("0", _("Do not shorten"))),
            ("1", SPI("1", _("Shorten at end of text only"))),
            ("2", SPI("2", _("Shorten all pauses")))
        ])
    except ImportError:
        return OrderedDict([
            ("0", _("Do not shorten")),
            ("1", _("Shorten at end of text only")),
            ("2", _("Shorten all pauses"))
        ])


def _get_availableSampleRates(isIBM=False):
    from collections import OrderedDict
    try:
        from autoSettingsUtils.utils import StringParameterInfo as SPI
        rates = OrderedDict([
            ("0", SPI("0", _("8 kHz"))),
            ("1", SPI("1", _("11 kHz")))
        ])
        if isIBM:
            rates["2"] = SPI("2", _("22 kHz"))
        return rates
    except ImportError:
        rates = OrderedDict([("0", _("8 kHz")), ("1", _("11 kHz"))])
        if isIBM:
            rates["2"] = _("22 kHz")
        return rates


def _get_availableVariants():
    from collections import OrderedDict
    from synthDriverHandler import VoiceInfo
    return OrderedDict((id, VoiceInfo(id, name)) for id, name in _variants.items())


if HAS_SYNTHDRIVER_HOST32:
    class SynthDriver(SynthDriverProxy32):
        name = "ibmeci"
        description = "IBMTTS"
        synthDriver32Path = os.path.join(os.path.dirname(__file__), "..", "_synthDrivers32")
        synthDriver32Name = "ibmeci"

        supportedSettings = (
            SynthDriverBase.VoiceSetting(),
            SynthDriverBase.VariantSetting(),
            SynthDriverBase.RateSetting(),
            BooleanDriverSetting("rateBoost", _("Rate boos&t"), True),
            SynthDriverBase.PitchSetting(),
            SynthDriverBase.InflectionSetting(),
            SynthDriverBase.VolumeSetting(),
            NumericDriverSetting("hsz", _("Hea&d size"), False),
            NumericDriverSetting("rgh", _("Rou&ghness"), False),
            NumericDriverSetting("bth", _("Breathi&ness"), False),
            BooleanDriverSetting("backquoteVoiceTags", _("Enable backquote voice &tags"), False),
            BooleanDriverSetting("ABRDICT", _("Enable &abbreviation expansion"), False),
            BooleanDriverSetting("phrasePrediction", _("Enable phras&e prediction"), False),
            DriverSetting("pauseMode", _("&Pauses"), defaultVal="2"),
            BooleanDriverSetting("sendParams", _("Al&ways Send Current Speech Settings"), False, defaultVal=True),
            DriverSetting('sampleRate', _('Sa&mple Rate'), defaultVal='1'),
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

        @classmethod
        def check(cls):
            # Store config values for later use
            try:
                if launcher._nvdaService:
                    cls._config_dllName = launcher._nvdaService.getConfigValue("ibmeci", "dllName")
                    cls._config_TTSPath = launcher._nvdaService.getConfigValue("ibmeci", "TTSPath")
                else:
                    cls._config_dllName = "eci.dll"
                    cls._config_TTSPath = "ibmtts"
            except Exception:
                cls._config_dllName = "eci.dll"
                cls._config_TTSPath = "ibmtts"
            return super().check()

        def __init__(self):
            # Configure 32-bit with correct paths
            try:
                self._remoteService.conn.execute(
                    f"import _ibmeci; "
                    f"_ibmeci.setDllConfig({repr(self._config_dllName)}, {repr(self._config_TTSPath)})"
                )
            except Exception:
                pass
            super().__init__()

        # Getters/Setters via _remoteService
        def _get_rateBoost(self):
            return self._remoteService.getParam("rateBoost")

        def _set_rateBoost(self, value):
            self._remoteService.setParam("rateBoost", value)

        def _get_inflection(self):
            return self._remoteService.getParam("inflection")

        def _set_inflection(self, value):
            self._remoteService.setParam("inflection", value)

        def _get_hsz(self):
            return self._remoteService.getParam("hsz")

        def _set_hsz(self, value):
            self._remoteService.setParam("hsz", value)

        def _get_rgh(self):
            return self._remoteService.getParam("rgh")

        def _set_rgh(self, value):
            self._remoteService.setParam("rgh", value)

        def _get_bth(self):
            return self._remoteService.getParam("bth")

        def _set_bth(self, value):
            self._remoteService.setParam("bth", value)

        def _get_backquoteVoiceTags(self):
            return self._remoteService.getParam("backquoteVoiceTags")

        def _set_backquoteVoiceTags(self, value):
            self._remoteService.setParam("backquoteVoiceTags", value)

        def _get_ABRDICT(self):
            return self._remoteService.getParam("ABRDICT")

        def _set_ABRDICT(self, value):
            self._remoteService.setParam("ABRDICT", value)

        def _get_phrasePrediction(self):
            return self._remoteService.getParam("phrasePrediction")

        def _set_phrasePrediction(self, value):
            self._remoteService.setParam("phrasePrediction", value)

        def _get_sendParams(self):
            return self._remoteService.getParam("sendParams")

        def _set_sendParams(self, value):
            self._remoteService.setParam("sendParams", value)

        def _get_pauseMode(self):
            return self._remoteService.getParam("pauseMode")

        def _set_pauseMode(self, value):
            self._remoteService.setParam("pauseMode", value)

        def _get_sampleRate(self):
            return self._remoteService.getParam("sampleRate")

        def _set_sampleRate(self, value):
            self._remoteService.setParam("sampleRate", value)

        def _get_availableVoices(self):
            from collections import OrderedDict
            from synthDriverHandler import VoiceInfo
            # Obter vozes do lado 32-bit via remoteService
            data = self._remoteService.getAvailableVoices()
            result = OrderedDict()
            for ID, name, language in data:
                # Traduzir o nome da voz
                result[ID] = VoiceInfo(ID, _(name), language)
            return result

        def _get_availablePausemodes(self):
            return _get_availablePauseModes()

        def _get_availableSamplerates(self):
            try:
                isIBM = self._remoteService.getParam("isIBM")
                return _get_availableSampleRates(isIBM)
            except:
                return _get_availableSampleRates(False)

else:
    # synthDriverHost32 não disponível - driver não funciona
    from synthDriverHandler import SynthDriver as SynthDriverBase

    class SynthDriver(SynthDriverBase):
        name = "ibmeci"
        description = "IBMTTS (requer synthDriverHost32)"

        @classmethod
        def check(cls):
            return False  # Não disponível sem synthDriverHost32
