# v22.07.3

* Updated locale strings for all languages to match with the original strings.
* Updated spanish documentation and locale strings.
* Updated sendParams and shortPause settings, now are set default to true because this is the recommended setting.
* fix issue #67 "last" variable must be checked if is not empty, is not None still can be empty.
* Replaced shortpause by shortPause for consistency in the code. This can affect your settings.
* All synth settings now have keyboard shortcuts in english language.
* Added sample rate documentation.
* The sample rate can now be set in the GUI. The 22 kHz option will only appear if using IBMTTS. This also means that concatenative voices are now fully supported.
* The shortened pauses setting will now also enable or disable the p1 commands sent at the end of strings. Partially for consistency, and also because the p1 commands introduce issues with the letter a in some strings, such as alt+a
