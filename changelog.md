# v22.08

* added soundcard detection change functionality. Sometimes IBMTTS was not able to detect those changes, E.G. when connecting a new sound device output.
* The abbreviation dictionary setting is now set directly through the API instead of through annotations
* updated readme and always send current speech settings description.
* Updated juar anticrash expression further.
* Annotations are now only sent at the beginning of speech sequences. The long term solution could be better, but this should fix #74. This also means that IBMTTS is now compatible with the always send current speech settings option.
* isIBM now applies if the IBMTTS version is 6.2 or higher. Fixes #69
