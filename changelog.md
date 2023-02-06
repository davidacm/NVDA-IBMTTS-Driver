# version v23.02.1

* Fixed some bugs in some cases when loading IBMTTS libraries. The way of loading the libraries has been changed to minimize the possibility of errors.
* If the driver can't load the library, an error entry will be shown in the log.
* Changed the way to determine the library being used. Now dll resources (ProductName) is used to determine it.
* Added the version where a  documentation change was introduced (for documentation translators).
* Added fixes for french.
* Updated code to use language constants.
* Improved the conditionals to determine the language to be used in process text.
* Restored the 22 kHz sample rate option. Voices that use it have surfaced recently.
* Removed outdated version of Spanish ª crash fix from spanish_ibm_fixes.
* Updated spanish documentation.
* Updated locale strings and documentation for Brazilian and Portugal Portuguese.
* Updated french documentation.
* Updated german interface and documentation.
* Updated translations for italian language.
* Updated english documentation.
