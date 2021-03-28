# IBMTTS-Treiber, Erweiterung fürNVDA #
  Diese Erweiterung ermöglicht das Einbinden der IBMTTS-Sprachausgabe in NVDA.  
  Die eigentlichen IBMTTS-Bibliotheken dürfen nicht angeboten werden, daher handelt es sich hierbei nur um den Treiber.  
  Wenn Sie bei der Verbesserung des Treibers mithelfen möchten, zögern Sie nicht uns einen Pull-Request zu senden!  

# Herunterladen.
Die neueste Version kann unter [diesem Link heruntergeladen werden](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

# Funktionen:
* Anpassung von Stimme, Variante, Geschwindigkeit, Tonhöhe, Betonung und Lautstärke.
* Zusätzliche Parameter für Kopfgröße, Rauigkeit und Atmung. Erstellen Sie Ihre eigene Stimme!
* Verwendung von Backquote-Sprachtags erlauben. Lassen Sie diese Funktion zum Schutz vor Schadcode und Scherzkeksen ausgeschaltet oder schalten Sie sie ein, um jede Menge Spaß mit der Sprachausgabe zu haben. Es müssen allerdings auch einige Anpassungen in NVDA vorgenommen werden, damit dies korrekt funktioniert.
* Geschwindigkeit zusätzlich erhöhen. Falls Ihnen die Sprachausgabe zu langsam ist, schalten Sie diese Option ein und holen das Maximum an Geschwindigkeit heraus!
* Automatischer Sprachenwechsel. Liest den Text automatisch in der richtigen Sprache vor.
* Umfangreicher Filter. Dieser Treiber enthält einen umfangreichen Satz aus Filtern, mit denen Abstürze oder seltsames Verhalten der Sprachausgabe vermieden werden.
* Wörterbuch-Unterstützung. Dieser Treiber erlaubt  das Einbinden spezieller Wörter, Stammwörterbücher sowie Abkürzungswörterbücher für jede Sprache. Fertige Wörterbücher sind im [Community-Dictionary-Repository](https://github.com/thunderdrop/IBMTTSDictionaries) oder im [alternativen Repository von mohamed00 (inklusive IBM-Sprachausgabenwörterbücher)](https://github.com/mohamed00/AltIBMTTSDictionaries) verfügbar

# Voraussetzungen.
## NVDA.
  NVDA 2018.4 oder neuer ist erforderlich. Dieser Treiber ist mit Python 3 kompatibel, und kann auch in zukünftigen NVDA-Versionen genutzt werden. Sobald NVDA mit Pyton 3 veröffentlicht wurde, wird diese Erweiterung nicht mehr mit Python 2.7 kompatibel sein. Bitte verwenden Sie daher immer die neueste NVDA-Version. Es ist kostenlos! 

## IBMTTS-Sprachausgabenbibliotheken.
  Dies ist nur der Treiber, Sie müssen sich die Bibliotheken selbst besorgen.  
  Dieser Treiber unterstützt die etwas neueren Bibliotheken, in denen ostasiatische Sprachen sowie spezifische Fehlerkorrekturen für bessere Textkodierung enthalten sind. Ältere Bibliotheken sollten jedoch auch funktionieren.  
  Seit Version 21.01 wird neben den SpeechWorks-Binärdateien auch die Integration der noch etwas neueren IBM-Binärdateien unterstützt. Ein Satz unabhängiger korrekturen ist enthalten, und die zusätzlichen Sprachen und anderen Unterschiede werden berücksichtigt. Nur die Formant-Stimmen werden derzeit unterstützt. Danke an @mohamed00 für diese Arbeit.

# Installation.
  Sie können die Erweiterung wie jede normale NVDA-Erweiterung installieren. Öffnen Sie danach die NVDA-Einstellungen und wählen die IBMTTS-Dateien in der Kategorie IBMTTS.
  Hier besteht auch die Möglichkeit, die IBMTTS-Dateien in eine Erweiterung zu kopieren, um sie lokal zu verwenden.

# Für die Weiterverbreitung paketieren.
  Öffnen Sie eine Kommandozeile im Hauptverzeichnis der Erweiterung und lassen den Befehl scons laufen. Die Erstellte Erweiterung wird, sofern keine Fehler aufgetreten sind, im Hauptverzeichnis abgelegt.

## Hinweise:

* Wenn sich die Sprachausgabe in der Erweiterung oder der "eciLibraries"-Erweiterung befindet, aktualisiert der Treiber automatisch die Pfade in den Ini-Dateien, sodass Sie sie in einer portablen NVDA-Kopie verwenden können.
* Beim Verwenden der Schaltfläche zum Kopieren der IBMTTS-Dateien wird eine neue Erweiterung erstellt. Wenn Sie IBMTTS wieder deinstallieren möchten, müssen zwei Erweiterungen deinstalliert werden, nämlich "IBMTTS-Treiber" und "Eci libraries".
* Die Scons und Gettext-Werkzeuge in diesem Projekt sind nur mit Python 3 kompatibel. Python 2.7 funktioniert nicht.
* Sie können die benötigten IBMTTS-Dateien auch direkt in der Erweiterung ablegen (nur für persönliche Nutzung). Kopieren Sie sie einfach in das Verzeichnis "addon\synthDrivers\ibmtts". Der Standard-Bibliotheksname kann falls notwendig in der Datei "settingsDB.py" angepasst werden.

# Referenzen.
Dieser Treiber basiert auf dem IBM-TTS-SDK, dessen Dokumentation unter [diesem Link](http://www.wizzardsoftware.com/docs/tts.pdf) verfügbar ist.

Eine Kopie ist auch in [diesem Repository](https://github.com/david-acm/NVDA-IBMTTS-Driver) erhältlich.

Siehe die Dateien

[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)
oder [tts.txt.](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)
