# IBMTTS driver, Add-on for NVDA #
  This add-on implements NVDA compatibility with the IBMTTS synthesizer.  
  We can not distribute the IBMTTS libraries. So it is just the driver.  
  If you want to improve this driver, feel free to send your pull requests!  

# Download.
The latest release is available to [download in this link](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

# Features:
* Voice, variant, rate, pitch, inflection and volume  setting support.
* Extra head size, Roughness, Breathiness parameters settings support. Create your own voice!
* Enable or disable backquote voice tags. Disable it to protect yourself from malicious codes from jokers, enable it to do many fun things with the synthesizer. Requires some extra tweaking with NVDA though to get it to work properly.
* Rate boost. If the synthesizer does not speak very fast to  you, then enable it and get the maximum voice speed!
* auto language switching. Let the synthesizer read text to you in the correct language when marked up.
* comprehensive filtering. This driver includes a comprehensive set of filters to fix crashes and other odd behavior of the synthesizer.
* dictionary support. This driver supports the integration of special words, roots, and abbreviation  user dictionaries for each language. Ready-made dictionary sets may be obtained from [the community dictionary repository](https://github.com/thunderdrop/IBMTTSDictionaries) or [mohamed00's alternative repository (with IBM synth dictionaries)](https://github.com/mohamed00/AltIBMTTSDictionaries)

## Extra settings:
This driver includes several extra options to control various characteristics of the synthesizer.
* Enable abbreviation dictionary: toggles expannsion of abbreviations. Note that disabling this option will also disable the expansion of any abbreviations specified in user-provided bbreviation dictionaries.
* Enable phrase prediction: if this option is enabled, the synthesizer will try to predict where pauses would occur in sentences based on their structure, for example, by using words like "and" or "the" as phrase boundaries. If this option is off, it will only pause if commas or other such punctuation is encountered.
* Shortened pauses: enable this option for shorter punctuation pauses, like those seen in other screen readers.
* Always send current speech settings: currently, there is a bug in the synthesizer that will occasionally cause the speech and pitch settings to be briefly reset to their default values. The cause of this issue is currently unknown, however a workaround is to continuously send the current speech rate and pitch settings. This option should generally be enabled. However, it should be disabled if you are using IBM binaries, as this setting will cause very long pauses to be inserted that will make them nearly unusable, or if you are reading text that contains backquote voice tags.

# Requirements.
## NVDA.
  You need NVDA 2019.3 or later.

## IBMTTS synthesizer libraries.
  This is just the driver, you must   get the libraries from  somewhere else.  
  This driver supports the slightly newer libraries that add East-Asian language support, and has specific fixes for the proper encoding of text. The older libraries without this should work, though.  
  As of version 21.03A1, this driver also works with the even newer libraries from IBM, rather than just the SpeechWorks ones. A set of independent fixes for those libraries is included, and the additional languages and other differences are accounted for. Only formant voices are supported at present. Thanks to @mohamed00 for this work.

# Installation.
  Just install it as an NVDA add-on. Then open NVDA dialog settings, and set the IBMTTS folder files in the IBMTTS category.
  Also in this category you can copy the external IBMTTS files into an Add-on to use it locally.

# Packaging it for distribution.
  Open a command line, change to the Add-on root folder  and run the scons command. The created add-on, if there were no errors, is placed in the root directory.

## Notes:

* if the synthesizer is inside the add-on or in "eciLibraries" add-on, the driver will update the ini library paths automatically. So you can use it on portable NVDA versions.
* when you use the "Copy IBMTTS files in an  add-on" button, it will create a new add-on. So, if you want to uninstall IBMTTS, you'll need to uninstall two add-ons: "IBMTTS driver" and "Eci libraries".
* scons and gettext tools on this project are  compatible with python 3 only. Doesn't work with python 2.7.
* You can put the extra IBMTTS required files in the add-on (for personal use only). Just copy them in "addon\synthDrivers\ibmtts" folder. Adjust the default library name in "settingsDB.py" if necessary.

# References.
This driver is based on the IBM tts sdk, the documentation is available on:
[this link](http://web.archive.org/web/20191125091344/http://www.wizzardsoftware.com/docs/tts.pdf)

Or you can get a copy on [this repo](https://github.com/david-acm/NVDA-IBMTTS-Driver)

See the files

[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)
or [tts.txt.](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)
