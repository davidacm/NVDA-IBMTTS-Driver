# v22.12

* updated spanish strings and documentation.
* updated the template of locale strings (for translators).
* fixed a spanish crashing pattern.
* changed the Chinese character encoding from GB2312 to CP936 (GBK). This enables IBMTTS implementations that support it to read more characters, including Traditional Chinese ones. This should be backwards compatible with GB2312, but versions that only support that encoding won't be able to read the extra characters. Fixes #57.
* Updated readme with new information on the best DLL to use for IBMTTS. Added a new section to explain how to report new issues.
* Removed access to the 22 kHz option that previously appeared if using IBMTTS, due to some reasons related with the IBMTTS libraries.
* Updated IBMTTS anticrash to catch more cases.
* Updated german interface and documentation.
* Updated voice names to use the proper set. This also means that voices 3, 5, and 6 are finally named properly after many years.
* Renamed Enable abbreviation dictionary setting to Enable abbreviation expansion for clarity.
