# IBMTTS-Treiber, Erweiterung fürNVDA #

  Diese Erweiterung ermöglicht das Einbinden der IBMTTS-Sprachausgabe in NVDA.  
  Die eigentlichen IBMTTS-Bibliotheken dürfen wir nicht anbieten, daher handelt es sich hierbei nur um den Treiber.  
  Wenn Sie bei der Verbesserung des Treibers mithelfen möchten, zögern Sie nicht uns einen Pull-Request zu senden!  

## Herunterladen.
Die neueste Version kann unter [diesem Link heruntergeladen werden](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

## Was ist der IBMTTS-Synthesizer?

ViaVoice TTS ist eine von IBM entwickelte Sprachausgabe, welche die textuelle Darstellung menschlicher Sprache in gesprochenen Text umwandelt.

## Funktionen:

* Anpassung von Stimme, Variante, Geschwindigkeit, Tonhöhe, Betonung und Lautstärke.
* Zusätzliche Parameter für Kopfgröße, Rauigkeit und Atmung. Erstellen Sie Ihre eigene Stimme!
* Verwendung von Backquote-Sprachtags erlauben. Lassen Sie diese Funktion zum Schutz vor Schadcode und Scherzkeksen ausgeschaltet oder schalten Sie sie ein, um jede Menge Spaß mit der Sprachausgabe zu haben. Es müssen allerdings auch einige Anpassungen in NVDA vorgenommen werden, damit dies korrekt funktioniert.
* Geschwindigkeit zusätzlich erhöhen. Falls Ihnen die Sprachausgabe zu langsam ist, schalten Sie diese Option ein und holen das Maximum an Geschwindigkeit heraus!
* Automatischer Sprachenwechsel. Liest den Text automatisch in der richtigen Sprache vor.
* Umfangreicher Filter. Dieser Treiber enthält einen umfangreichen Satz aus Filtern, mit denen Abstürze oder seltsames Verhalten der Sprachausgabe vermieden werden.
* Wörterbuch-Unterstützung. Dieser Treiber erlaubt  das Einbinden spezieller Wörter, Stammwörterbücher sowie Abkürzungswörterbücher für jede Sprache. Fertige Wörterbücher sind im [Community-Dictionary-Repository](https://github.com/thunderdrop/IBMTTSDictionaries) oder im [alternativen Repository von mohamed00 (inklusive IBM-Sprachausgabenwörterbücher)](https://github.com/mohamed00/AltIBMTTSDictionaries) verfügbar

### Zusätzliche Einstellungen:

* Abkürzungswörterbuch verwenden: Schaltet das Aussprechen von Abkürzungen um. Bitte beachten Sie, dass durch Ausschalten dieser Funktion auch die im Benutzerwörterbuch hinterlegten Abkürzungen nicht mehr ausgesprochen werden.
* Satzvorhersage einschalten: Ist diese Funktion eingeschaltet, versucht die Sprachausgabe die Satzstruktur zum Einfügen von Sprechpausen zu analysieren, beispielsweise durch die Verwendung der Worte "und" oder "oder" zur Begrenzung von Nebensätzen. Bei ausgeschalteter Funktion werden Pausen ausschließlich bei einem vorhandenem Komma oder anderen Satzzeichen eingefügt.
* Pausen verkürzen: Schalten Sie diese Option ein, um die Pausen zwischen Satzzeichen zu verkürzen.
* Aktuelle Sprachausgabeneinstellungen immer senden: Ein Fehler in der Sprachausgabe bewirkt, dass hin und wieder die Einstellungen für Sprache und Geschwindigkeit kurzzeitig auf ihre Standardwerte zurückgesetzt werden. Die Ursache ist nicht bekannt, jedoch wird dieses Verhalten durch kontinuierliches Senden der Sprachausgabeneinstellungen vermieden. Generell sollte diese Funktion eingeschaltet sein, muss jedoch bei der Verwendung von Backquote-Sprachtags ausgeschaltet werden.
* Sample-Rate: Ändert die Klangqualität der Sprachausgabe. Diese Einstellung kann am sinnvollsten mit IBM TTS verwendet werden, bei welcher eine Sample-Rate von 22 kHz unterstützt wird.

## Voraussetzungen.
### NVDA.
  NVDA 2019.3 oder neuer ist erforderlich.

### IBMTTS-Sprachausgabenbibliotheken.
  Dies ist nur der Treiber, Sie müssen sich die Bibliotheken selbst besorgen.  
  Dieser Treiber unterstützt die etwas neueren Bibliotheken, in denen ostasiatische Sprachen sowie spezifische Fehlerkorrekturen für bessere Textkodierung enthalten sind. Ältere Bibliotheken sollten jedoch auch funktionieren.  
  Seit Version 21.03A1 wird neben den SpeechWorks-Binärdateien auch die Integration der noch etwas neueren IBM-Binärdateien unterstützt. Ein Satz unabhängiger korrekturen ist enthalten, und die zusätzlichen Sprachen und anderen Unterschiede werden berücksichtigt. Concatenative Stimmen werden unterstützt und sind zugänglich, indem die Sample-Rate auf 8 kHz eingestellt wird. Verwenden Sie für die besten Ergebnisse ibmeci.dll Version 6.6.1.0 oder älter, da neuere Versionen bei der schnellen Verarbeitung von Text instabil sein können, beispielsweise beim schnellen Scrollen durch Listeneinträge.

## Installation.
  Sie können die Erweiterung wie jede normale NVDA-Erweiterung installieren. Öffnen Sie danach die NVDA-Einstellungen und wählen die IBMTTS-Dateien in der Kategorie IBMTTS.
  Hier besteht auch die Möglichkeit, die IBMTTS-Dateien in eine Erweiterung zu kopieren, um sie lokal zu verwenden.

## Zur Übersetzung beitragen.

Zur Erleichterung der Arbeit ist eine 
[Übersetzungsvorlage im Master-Branch enthalten.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot)
Falls Sie eine neue Übersetzung erstellen möchten, jedoch auf die Verwendung von GitHub und die notwendigen Python-Werkzeuge verzichten wollen, führen Sie bitte die folgenden Schritte aus:

1. Verwenden Sie
[diese Vorlage](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot)
Als Grundlage für die Zielsprache.
2. Laden Sie sich
["Poedit"](https://poedit.net/).
herunter. Diese Software hilft Ihnen bei der Verwaltung der Übersetzung.
3. Falls Sie auch die Dokumentation übersetzen möchten, können Sie die
[englische Dokumentation als Vorlage verwenden.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/README.md)
4. Wenn die Übersetzung fertig ist, senden Sie mir diese unter der E-Mail-Adresse "dhf360@gmail.com".

Sie müssen die Quelldateien nicht selbst kompilieren, dies geschieht bei der Veröffentlichung einer neuen Version der Erweiterung. Ihr Name wird im entsprechenden Commit erwähnt. Wünschen Sie keine Erwähnung, lassen Sie es mich bitte in Ihrer E-Mail wissen.

Hinweis: Bitte verwenden Sie immer die neueste Übersetzungsvorlage.

Dies ist nur eine alternative Methode, natürlich können Sie auch den üblichen Weg gehen. Erstellen Sie einen Fork dieses Repositories, nehmen die Übersetzung für Ihre Sprache vor und  senden mir danach einen Pull-Request. Der alternative Weg macht den Vorgang nur etwas komplizierter.

## Für die Weiterverbreitung paketieren.
  Öffnen Sie eine Kommandozeile im Hauptverzeichnis der Erweiterung und lassen den Befehl scons laufen. Die Erstellte Erweiterung wird, sofern keine Fehler aufgetreten sind, im Hauptverzeichnis abgelegt.

### Bibliotheken als unabhängige Erweiterung paketieren.
Es ist nicht empfehlenswert die Sprachausgaben-Bibliotheken direkt mit dem Treiber zu bündeln, da sie entfernt werden, wenn man die Erweiterung aus dem [offiziellem Repo](https://github.com/davidacm/NVDA-IBMTTS-Driver) aktualisiert. 
Zur Lösung dieses Problems können die Bibliotheken als separate Erweiterung installiert werden. 
[Folgen Sie diesem Link](https://github.com/davidacm/ECILibrariesTemplate), 
um mehr über die Installation als separate Erweiterung zu erfahren.

### Hinweise:

* Wenn sich die Sprachausgabe in der Erweiterung oder der "eciLibraries"-Erweiterung befindet, aktualisiert der Treiber automatisch die Pfade in den Ini-Dateien, sodass Sie sie in einer portablen NVDA-Kopie verwenden können.
* Beim Verwenden der Schaltfläche zum Kopieren der IBMTTS-Dateien wird eine neue Erweiterung erstellt. Wenn Sie IBMTTS wieder deinstallieren möchten, müssen zwei Erweiterungen deinstalliert werden, nämlich "IBMTTS-Treiber" und "Eci libraries".
* Die Scons und Gettext-Werkzeuge in diesem Projekt sind nur mit Python 3 kompatibel. Python 2.7 funktioniert nicht.
* Sie können die benötigten IBMTTS-Dateien auch direkt in der Erweiterung ablegen (nur für persönliche Nutzung). Kopieren Sie sie einfach in das Verzeichnis "addon\synthDrivers\ibmtts". Der Standard-Bibliotheksname kann falls notwendig in der Datei "settingsDB.py" angepasst werden.

## Referenzen.
Dieser Treiber basiert auf dem IBM-TTS-SDK, dessen Dokumentation unter [diesem Link](http://web.archive.org/web/20191125091344/http://www.wizzardsoftware.com/docs/tts.pdf) verfügbar ist.

Auch zu bekommen bei der Universität von Columbia 
[unter diesem Link](http://www1.cs.columbia.edu/~hgs/research/projects/simvoice/simvoice/docs/tts.pdf)

Eine Kopie ist auch in [diesem Repository](https://github.com/david-acm/NVDA-IBMTTS-Driver) erhältlich.

[Pyibmtts: Python-Wrapper für IBM TTS, entwickelt von Peter Parente](https://sourceforge.net/projects/ibmtts-sdk/)

Siehe die Dateien

[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)
oder [tts.txt.](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)
