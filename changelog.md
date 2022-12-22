# v22.12.1

* fixed soundcard detection issues when another tts is used in other NVDA profile. This was happening because register and unregister the profile switch handler was being done exactly in the same moment as the profile changing. So, a delay of 1S was added to register or unregister that function.
* Changed the Chinese encoding again, from CP936 to GB18030. This can represent more characters.
* Added a \b to the Spanish IBM crashing expression to prevent false positives on things like 20ª.
* Updated the english readme with specific steps to package the driver and a small note about Eloquence.
* Updated the spanish documentation.
* updated portuguese locale strings and documentation.
