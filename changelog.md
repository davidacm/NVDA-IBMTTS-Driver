# version 25.2.1

* Temporary fix for an issue with translations when the add-on starts the first time that is installed.
* updated portuguese translations.
* Changed the default encoding. from mbs to cp1252.

# Version 25.1.1

* Added support for NVDA 2025.1.
* Now the driver looks for the audio output in two config paths.
* Deleted the audio output change handler. This was created because in some cases the driver was not synchronized with the current audio output, it needs more testing but seems that this doesn't happen in wasapi mode.

# Version 23.12.1

* Updated support for NVDA 2024.2.
* added some strings that were not translatable.
* Added an option to donate to this add-on.
* Updated installTasks to request for donations during installation.
* Updated locale strings template for translators.
* Updated spanish locale strings.
* Updated documentation to add description of new pause options
* Python 3.11 compatibility (#105)
* Replaced the boolean shorten pauses setting with an expanded setting that allows to shorten no pauses, pauses at utterance boundaries, or all punctuated pauses. (#101): To implement this, the shortPause driver setting has been replaced with a choice setting called pauseMode, using logic based on that used for sample rate selection. This introduces a third pause mode, herein called utterance boundary, that will only reduce the pause at the end of a speech sequence. This has the value 1. The value 2 corresponds to the previous shorten pauses setting set to true, causing the utterance boundary to be shortened as well as the pause-related regular expressions to be applied. This does not presently load the previous shorten pauses setting and adapt to this new scheme, and the string for the utterance mode could likely do with some revision.
* avoid importing add-on modules on installTasks.py, this should fix #85.
* now the availability of the libraries should be detected properly during add-on installation.
* solved compatibility issues with NVDA Alpha V28351 and above. It closes #92, closes #93 and closes #95.
* updated the installTasks to avoid delete internal libraries inside synthDrivers/ibmtts when reinstalling the add-on.
* Added another set of expressions to reduce the verbosity of IBMTTS

# version 23.4.1

* Changed eciSynthMode from the default 0 (Sentence) to 1 (Manual): Synthesis and input clearing is controlled by commands only.
* Tried to work around situations where IBMTTS would say 'comma hundred' or other weird things in English if numbers are separated by commas
* Some fixes in english_ibm_fixes should've actually applied globally. Moved the punctuation fixes formerly part of english_ibm_fixes to a new global_ibm_fixes section to improve the experience for non-English languages
* Fixed short pauses pronouncing the right parenthesis if IBMTTS was used. While this change will make the short pauses expression slightly less affective, it will still work in general
* Updated German anticrash further to catch more cases. #88
* More space removal changes. The expression will take into account numbers as well as letters in the negative lookahead, and added the question mark to its captured punctuation
* Improved the IBMTTS space removal expression so it doesn't catch false positives such as it's a .mp3 file
* added a log message if the selected library is not correct. It shows the exception that raised the failure.

# Version 18-06-2018:

* unused imported modules were deleted.
* fixed crashing expression for spanish language.
* added utf-8 coding header in order to fix some reg expressions.

# Version 13-07-2018:

* changed  pauses from p0 to p1.
* all french fixes were placed in the same conditional.
* now uses x in (1, 2) instead of x==1 or x==2 for all cases.
* added "!" to punctuation list.

# Version 15-07-2018:

* added "-" to punctuation list.
* added pauses for dash "-" symbol.
* comma "," is replaced by dash "-" at the end of a string because eloquence seems to ignore commas at the end.
* deleted "should_pause=False" parameter in xspeaktext because it isn't used anywere in the code. It was used to fix audio issues but currently seems to be unused.
* incorrect behavior when spelling text has been fixed.
* xspeakText changed to processText to clarify code.

# Version 12-08-2018:

* maxRate changed from 250 to 156.
* added rateBoost setting. Enable this option to increase rate by 1.6x.

# Version 16-09-2018:

* Fixed rate param conversion when rate boost is active.
16/03/2019
* Deleted Queue import in ibmeci.py, since this module is not used here.
* Updated code for compatibility with python 3.
* Defined unicode function for backward compatibility with python 2.7.
* added b prefix to strings to treat them as byteStrings, since python 3 strings are unicode by default.
* CHANGED isinstance(item,basestring) TO STR.
* Updated auto language detection to simplify the code and compatibility for python 3.
* Updated processText function.
* Now in _imbesi uses io.BytesIO rater than cStringIo.StringIO
* added seek(0) since BytesIO doesn't update it automatically when truncate.
