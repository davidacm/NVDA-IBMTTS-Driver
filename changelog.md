# version 23.4.1
Changed eciSynthMode from the default 0 (Sentence) to 1 (Manual): Synthesis and input clearing is controlled by commands only.
Tried to work around situations where IBMTTS would say 'comma hundred' or other weird things in English if numbers are separated by commas
Some fixes in english_ibm_fixes should've actually applied globally. Moved the punctuation fixes formerly part of english_ibm_fixes to a new global_ibm_fixes section to improve the experience for non-English languages
Fixed short pauses pronouncing the right parenthesis if IBMTTS was used. While this change will make the short pauses expression slightly less affective, it will still work in general
Updated German anticrash further to catch more cases. #88
More space removal changes. The expression will take into account numbers as well as letters in the negative lookahead, and added the question mark to its captured punctuation
Improved the IBMTTS space removal expression so it doesn't catch false positives such as it's a .mp3 file
added a log message if the selected library is not correct. It shows the exception that raised the failure.
