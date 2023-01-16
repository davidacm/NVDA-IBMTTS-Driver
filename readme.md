# IBMTTS driver, Add-on for NVDA #

  This add-on implements NVDA compatibility with the IBMTTS synthesizer.  
  We can not distribute the IBMTTS libraries. So it is just the driver.  
  If you want to improve this driver, feel free to send your pull requests!  

Although this driver is compatible with Eloquence libraries (since Eloquence has the same api as IBMTTS) it's not recommended to use Eloquence with this driver due to licensing issues. Before using any synthesis libraries with this driver, it's recommended to get the license usage rights first.

This driver was developed with the documentation available for IBMTTS, publicly available on the web. See references section for more details.

## Download.
The latest release is available to [download in this link](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

## What is IBMTTS synthesizer?

ViaVoice TTS is a text-to-speech engine developed by IBM, which synthesizes textual representation of human language into speech.

## Features and settings.

* Voice, variant, rate, pitch, inflection and volume  setting support.
* Extra head size, Roughness, Breathiness parameters settings support. Create your own voice!
* Enable or disable backquote voice tags. Disable it to protect yourself from malicious codes from jokers, enable it to do many fun things with the synthesizer. Requires some extra tweaking with NVDA though to get it to work properly.
* Rate boost. If the synthesizer does not speak very fast to  you, then enable it and get the maximum voice speed!
* auto language switching. Let the synthesizer read text to you in the correct language when marked up.
* comprehensive filtering. This driver includes a comprehensive set of filters to fix crashes and other odd behavior of the synthesizer.
* dictionary support. This driver supports the integration of special words, roots, and abbreviation  user dictionaries for each language. Ready-made dictionary sets may be obtained from [the community dictionary repository](https://github.com/thunderdrop/IBMTTSDictionaries) or [mohamed00's alternative repository (with IBM synth dictionaries)](https://github.com/mohamed00/AltIBMTTSDictionaries)

### Extra settings:

* Enable abbreviation expansion: toggles expannsion of abbreviations. Note that disabling this option will also disable the expansion of any abbreviations specified in user-provided abbreviation dictionaries.
* Enable phrase prediction: if this option is enabled, the synthesizer will try to predict where pauses would occur in sentences based on their structure, for example, by using words like "and" or "the" as phrase boundaries. If this option is off, it will only pause if commas or other such punctuation is encountered.
* Shorten pauses: enable this option for shorter punctuation pauses, like those seen in other screen readers.
* Always send current speech settings: there is a bug in the synthesizer that will occasionally cause the speech and pitch settings to be briefly reset to their default values. The cause of this issue is currently unknown, however a workaround is to continuously send the current speech rate and pitch settings. This option should generally be enabled. However, it should be disabled if reading text that contains backquote voice tags.
* Sample rate: changes the synthesizer's sound quality. Most useful for IBMTTS, where setting the sample rate to 8 kHz enables access to a new set of voices.

### IBMTTS category settings.

This add-on has its own category of settings within NVDA options, to manage some internal functionality not related to speech synthesis.

* Automatically check for updates for IBMTTS: If this option is checked, the add-on will check daily for new versions available.
* Check for update  button: Manually check for new add-on updates.
* IBMTTS folder address: The path to load the IBMTTS library. It can be absolute or relative.
* IBMTTS library name (dll): The name of the library (dll). Don't include paths, only the name with the extension, typically ".dll".
* Browse for  IBMTTS library... Opens a file browse dialog to search for the IBMTTS library on the system. It will be saved as an absolute path.
* Copy IBMTTS files in an  add-on (may not work for some IBMTTS distributions): If the library path for IBMTTS has been set, it will copy all the folder files to a new add-on called eciLibraries and update the current path to a relative path. It's very useful in NVDA portable versions. It only works for libraries that use "eci.ini" files for voice language information. If the library uses the Windows registry, then this option won't work.

Note: The automatic or manual update functionality won't remove the internal files of the add-on. If you use your libraries in that place, you can safely use this function. Your libraries will be safe.

## Requirements.
### NVDA.
  You need NVDA 2019.3 or later.

### IBMTTS synthesizer libraries.
  This is just the driver, you must   get the libraries from  somewhere else.  
  This driver supports the slightly newer libraries that add East-Asian language support, and has specific fixes for the proper encoding of text. The older libraries without this should work, though.  
  As of version 21.03A1, this driver also works with the even newer libraries from IBM, rather than just the SpeechWorks ones. A set of independent fixes for those libraries is included, and the additional languages and other differences are accounted for. Concatenative voices are supported, and can be accessed by setting the sample rate to 8 kHz after installing voices. For best results, use the June 2005 build of ibmeci.dll (version 7.0.0.0) as older versions can be unstable when receiving text rapidly, for example, by quickly scrolling through items in a list. Also note that if you are using Hong Kong Cantonese or Chinese IBMTTS libraries, you may want to disable the use spelling functionality if supported option, to prevent some characters in these languages from being spelled out using the pinyin they are internally converted to.

## Installation.
  Just install it as an NVDA add-on. Then open NVDA dialog settings, and set the IBMTTS folder files in the IBMTTS category.
  Also in this category you can copy the external IBMTTS files into an Add-on to use it locally.

## Contributing to translation.

In order to make your work easier, I have left a 
[translation template in the master branch.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot)

For the documentation, I created a file called ["docChangelog-for-translators.md".](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/docChangelog-for-translators.md)
you can use that file to see what has been changed in the documentation and update the documentation for your language.

If you want to translate this add-on to another language and you don't want to open a github account or install python and other tools needed for the translation, do the following steps:

1. Use
[this template](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot),
as a base for the target language.
2. Download
["poedit"](https://poedit.net/),
this software will help you manage the translation strings.
3. If you want to translate the documentation too, you can see the new changes of the documentation
[at this link.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/docChangelog-for-translators.md) You can see the [full english documentation here.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/readme.md)
4. Once you finished the translation, you can send me it to: "dhf360@gmail.com".

You won't need to compile the source files. I'll do it when releasing a new add-on version. I will mention your name in the respective commit. If you don't wish to be mentioned, let me in the e-mail.

Note: make sure you have used the latest translation strings template.

This is an alternative method. If you want, you always can go by the usual way. Fork this repo, update the translation for your language, and send me a PR. But this way just will add more complexity for you.

## Packaging it for distribution.

1. Install python, currently python 3.7 is used, but You can use a newer version.
2. Install gettext, you can download a distribution for windows in [this link.](https://mlocati.github.io/articles/gettext-iconv-windows.html) If you're using windows 64 bits, I recommend [this version.](https://github.com/mlocati/gettext-iconv-windows/releases/download/v0.21-v1.16/gettext0.21-iconv1.16-shared-64.exe)
3. (optional but recommended step) create a python virtual environment to be used to manage NVDA add-ons. In the console, use "python -m venv PAT_TO_FOLDER". Where PAT_TO_FOLDER is the path of your desired path for the virtual environment.
4. If you did step 2, go to the PAT_TO_FOLDER and inside scripts folder, execute "activate". The name of the environment should be shown in the console prompt.
5. Clone this repo in your desired path: "git clone https://github.com/davidacm/NVDA-IBMTTS-Driver.git".
6. In the same console instance, go to the folder of this repo.
7. Install the requirements: "pip install -r requirements.txt".
8. Run the scons command. The created add-on, if there were no errors, is placed in the root directory of this repo.

Once you close the console, the virtual environment is deactivated.

### Packaging libraries as an independent add-on.

Is not recommended to include the libraries with this driver. It's because if the user updates the driver from the
[official repo](https://github.com/davidacm/NVDA-IBMTTS-Driver),
using the NVDA add-on installer, the old version will be deleted including the libraries. One solution for this, is to install the libraries in a separate add-on.
[Follow this link](https://github.com/davidacm/ECILibrariesTemplate)
to know how to package the libraries in a separate add-on.

### Notes:

* If you use the internal update feature (manual or automatic) the libraries won't be deleted even if they are inside the add-on.
* if the synthesizer is inside the add-on or in
["eciLibraries"](https://github.com/davidacm/ECILibrariesTemplate)
add-on, the driver will update the ini library paths automatically. So you can use it on portable NVDA versions.
* when you use the "Copy IBMTTS files in an  add-on" button, it will create a new add-on. So, if you want to uninstall IBMTTS, you'll need to uninstall two add-ons: "IBMTTS driver" and "Eci libraries".
* scons and gettext tools on this project are  compatible with python 3 only. Doesn't work with python 2.7.
* You can put the extra IBMTTS required files in the add-on (for personal use only). Just copy them in "addon\synthDrivers\ibmtts" folder. Adjust the default library name in "settingsDB.py" if necessary.
* if the configured library path is not relative, this add-on won't update the paths in the "eci.ini" file. The driver assumes that when using absolute paths, the paths are correct in "eci.ini" and will avoid making any updates. Keep this in mind when setting the path of your libraries. If they were not correct, this could cause errors that will render NVDA speechless when you use this synthesizer.

## Reporting issues:

If you find a security issue with some of the libraries that are compatible with this driver, please do not open a github issue nor comment it on forums before the issue is solved. Please report the issue on [this form.](https://docs.google.com/forms/d/123gSqayOAsIQLx1NiI98fEqr46oiJRZ9nNq0_KIF9WU/edit)

If the issue doesn't crash the driver or the screen reader, then open an [github issue here.](https://github.com/davidacm/NVDA-IBMTTS-Driver/issues)

## References.
This driver is based on the IBM tts sdk, the documentation is available on:
[this link](http://web.archive.org/web/20191125091344/http://www.wizzardsoftware.com/docs/tts.pdf)

also at the university of Columbia in
[this link](http://www1.cs.columbia.edu/~hgs/research/projects/simvoice/simvoice/docs/tts.pdf)

Or you can get a backup copy on [this repo](https://github.com/david-acm/NVDA-IBMTTS-Driver)

[pyibmtts: Python wrapper for IBM TTS developed by Peter Parente](https://sourceforge.net/projects/ibmtts-sdk/)

See the backup files here:

[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)

or [tts.txt.](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)
