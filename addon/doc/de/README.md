# IBMTTS-Treiber, Erweiterung fürNVDA #

  Diese Erweiterung ermöglicht das Einbinden der IBMTTS-Sprachausgabe in NVDA.  
  Die eigentlichen IBMTTS-Bibliotheken dürfen wir nicht anbieten, daher handelt es sich hierbei nur um den Treiber.  
  Wenn Sie bei der Verbesserung des Treibers mithelfen möchten, zögern Sie nicht uns einen Pull-Request zu senden!  

Auch wenn dieser Treiber mit Eloquence-Bibliotheken kompatibel ist, da Eloquence die gleiche API wie IBMTTS verwendet, wird die Verwendung von Eloquence mit diesem Treiber aufgrund von Lizenzierungsproblemen nicht empfohlen. Vor der Verwendung von Synthesebibliotheken mit diesem Treiber wird empfohlen, zuerst die Nutzungsrechte zu erwerben.

Dieser Treiber wurde mit der für IBMTTS verfügbaren Dokumentation entwickelt, die im Internet öffentlich zugänglich ist. Weitere Einzelheiten finden Sie im Abschnitt Referenzen.

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
* Sample-Rate: Ändert die Klangqualität der Sprachausgabe. Diese Einstellung kann am sinnvollsten mit IBM TTS verwendet werden, bei welcher eine Sample-Rate von 8 kHz den Zugriff auf einen neuen Satz von Stimmen erlaubt.

### IBMTTS-Kategorieeinstellungen.

Diese Erweiterung hat eine eigene Einstellungskategorie innerhalb der NVDA-Optionen, um einige nicht direkt mit der Sprachsynthese verbundenen Einstellungen zu verwalten.

* Automatisch nach Updates für IBMTTS suchen: Bei eingeschalteter Option sucht die Erweiterung einmal täglich nach neuen Versionen.
* Nach Update suchen: Eine Schaltfläche zum manuellen Prüfen auf Aktualisierungen.
* IBMTTS-Verzeichnispfad: Der absolute oder relative Pfad zum Laden der IBMTTS-Bibliotheken.
* IBMTTS-Bibliotheksname (DLL): Name der Bibliothek (DLL). Verwenden Sie hier keinen Pfad, sondern nur den Dateinamen der Bibliothek inklusive Erweiterung, typischerweise ".dll".
* Nach IBMTTS-Bibliothek suchen... Öffnet einen Dialog zum Durchsuchen des Systems nach der IBMTTS-Bibliothek. Die Bibliothek wird als absoluter Pfad gespeichert.
* IBMTTS-Dateien in eine Erweiterung kopieren (funktioniert möglicherweise nicht mit einigen IBMTTS-Distributionen): Wenn der Bibliothekspfad für IBMTTS festgelegt wurde, kopiert es alle Ordnerdateien in eine neue Erweiterung namens eciLibraries und wandelt den momentanen Pfad in einen relativen Pfad um. Dies ist sehr nützlich in portablen NVDA-Versionen. Es funktioniert nur für Bibliotheken, die "eci.ini"-Dateien für Stimmen- und Sprachinformationen verwenden. Wenn die Bibliothek die Windows-Registrierung verwendet, wird diese Option nicht funktionieren.

Hinweis: Die automatische oder manuelle Aktualisierungsfunktion wird die internen Dateien der Erweiterung nicht entfernen. Wenn Sie Ihre Bibliotheken an dieser Stelle verwenden, können Sie diese Funktion gefahrlos nutzen. Ihre Bibliotheken sind sicher.

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

Für die Dokumentation habe ich eine Datei namens ["docChangelog-for-translators.md".](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/docChangelog-for-translators.md) erstellt.
Sie können diese Datei verwenden, um zu sehen, was in der Dokumentation geändert wurde, und die Dokumentation für Ihre Sprache aktualisieren.

Zur Erleichterung der Arbeit ist eine 
[Übersetzungsvorlage im Master-Branch enthalten.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot)
Falls Sie eine neue Übersetzung erstellen möchten, jedoch auf die Verwendung von GitHub und die notwendigen Python-Werkzeuge verzichten wollen, führen Sie bitte die folgenden Schritte aus:

1. Verwenden Sie
[diese Vorlage](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot)
Als Grundlage für die Zielsprache.
2. Laden Sie sich
["Poedit"](https://poedit.net/).
herunter. Diese Software hilft Ihnen bei der Verwaltung der Übersetzung.
3. Falls Sie auch die Dokumentation übersetzen möchten, können Sie die letzten Änderungen an der Dokumentation 
[unter diesem Link einsehen.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/docChangelog-for-translators.md) You can see the [full english documentation here.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/readme.md)
4. Wenn die Übersetzung fertig ist, senden Sie mir diese unter der E-Mail-Adresse "dhf360@gmail.com".

Sie müssen die Quelldateien nicht selbst kompilieren, dies geschieht bei der Veröffentlichung einer neuen Version der Erweiterung. Ihr Name wird im entsprechenden Commit erwähnt. Wünschen Sie keine Erwähnung, lassen Sie es mich bitte in Ihrer E-Mail wissen.

Hinweis: Bitte verwenden Sie immer die neueste Übersetzungsvorlage.

Dies ist nur eine alternative Methode, natürlich können Sie auch den üblichen Weg gehen. Erstellen Sie einen Fork dieses Repositories, nehmen die Übersetzung für Ihre Sprache vor und  senden mir danach einen Pull-Request. Der alternative Weg macht den Vorgang nur etwas komplizierter.

## Für die Weiterverbreitung paketieren.

1. Installieren Sie Python. Momentan wird Python 3.7 verwendet, Sie können jedoch eine neuere Version nutzen.
2. Installieren Sie Gettext, eine Distribution für Windows ist unter [diesem Link verfügbar.](https://mlocati.github.io/articles/gettext-iconv-windows.html) Wenn sie Windows 64 Bit verwenden ist [diese Version empfehlenswert.](https://github.com/mlocati/gettext-iconv-windows/releases/download/v0.21-v1.16/gettext0.21-iconv1.16-shared-64.exe)
3. (optional, jedoch ein empfohlener Schritt) erstellen Sie eine virtuelle Umgebung in Python zur Verwaltung von NVDA-Erweiterungen. Geben sie in der Konsole "python -m venv PFAD_ZUM_ORDNER". ein, wobei PFAD_ZUM_ORDNER der gewünschte Pfad der virtuellen Umgebung ist.
4. Wenn Sie Schritt zwei ausgeführt haben, gehen Sie in den Ordnerpfad und geben dort "activate" ein. Der Umgebungsname sollte nun im Konsolenprompt angezeigt werden.
5. Clonen sie das Repository im gewünschten Pfad: "git clone https://github.com/davidacm/NVDA-IBMTTS-Driver.git".
6. Gehen Sie zum Pfad des Repositories in derselben Instanz.
7. Installieren Sie die Abhängigkeiten: "pip install -r requirements.txt".
8. Lassen Sie das Kommando scons laufen. Die erstellte Erweiterung wird, sofern keine Fehler aufgetreten sind, im Hauptverzeichnis des Repositories generiert.

Sobald Sie die Konsole schließen, wird die virtuelle Umgebung deaktiviert.

### Bibliotheken als unabhängige Erweiterung paketieren.

Es ist nicht empfehlenswert die Sprachausgaben-Bibliotheken direkt mit dem Treiber zu bündeln, da sie entfernt werden, wenn man die Erweiterung aus dem [offiziellem Repo](https://github.com/davidacm/NVDA-IBMTTS-Driver) aktualisiert. 
Zur Lösung dieses Problems können die Bibliotheken als separate Erweiterung installiert werden. 
[Folgen Sie diesem Link](https://github.com/davidacm/ECILibrariesTemplate), 
um mehr über die Installation als separate Erweiterung zu erfahren.

### Hinweise:

* Wenn Sie die interne Aktualisierung verwenden (manuell oder automatisch), werden die Bibliotheken nicht gelöscht, sogar wenn sie sich in der Erweiterung befinden.
* Wenn sich die Sprachausgabe in der Erweiterung oder der ["eciLibraries"-Erweiterung](https://github.com/davidacm/ECILibrariesTemplate) befindet, aktualisiert der Treiber automatisch die Pfade in den Ini-Dateien, sodass Sie sie in einer portablen NVDA-Kopie verwenden können.
* Beim Verwenden der Schaltfläche zum Kopieren der IBMTTS-Dateien wird eine neue Erweiterung erstellt. Wenn Sie IBMTTS wieder deinstallieren möchten, müssen zwei Erweiterungen deinstalliert werden, nämlich "IBMTTS-Treiber" und "Eci libraries".
* Die Scons und Gettext-Werkzeuge in diesem Projekt sind nur mit Python 3 kompatibel. Python 2.7 funktioniert nicht.
* Sie können die benötigten IBMTTS-Dateien auch direkt in der Erweiterung ablegen (nur für persönliche Nutzung). Kopieren Sie sie einfach in das Verzeichnis "addon\synthDrivers\ibmtts". Der Standard-Bibliotheksname kann falls notwendig in der Datei "settingsDB.py" angepasst werden.
* Wenn der konfigurierte Bibliothekspfad nicht relativ ist, wird dieses Add-on die Pfade in der Datei "eci.ini" nicht aktualisieren. Der Treiber geht davon aus, dass bei der Verwendung von absoluten Pfaden die Pfade in der Datei "eci.ini" korrekt sind und vermeidet jegliche Aktualisierung. Beachten Sie dies, wenn Sie den Pfad Ihrer Bibliotheken festlegen. Wenn sie nicht korrekt sind, kann dies zu Fehlern führen, die NVDA bei der Verwendung des Synthesizers sprachlos machen.

## Probleme melden:

Wenn Sie ein Sicherheitsproblem mit einigen der Bibliotheken finden, die mit diesem Treiber kompatibel sind, öffnen Sie bitte kein Github-Issue und kommentieren Sie es nicht in Foren, bevor das Problem gelöst ist. Bitte melden Sie das Problem über [dieses Formular.](https://docs.google.com/forms/d/123gSqayOAsIQLx1NiI98fEqr46oiJRZ9nNq0_KIF9WU/edit)

Wenn das Problem den Treiber oder den Bildschirmleser nicht zum Absturz bringt, öffne hier ein [Github-Issue.](https://github.com/davidacm/NVDA-IBMTTS-Driver/issues)

## Referenzen.
Dieser Treiber basiert auf dem IBM-TTS-SDK, dessen Dokumentation unter [diesem Link](http://web.archive.org/web/20191125091344/http://www.wizzardsoftware.com/docs/tts.pdf) verfügbar ist.

Auch zu bekommen bei der Universität von Columbia 
[unter diesem Link](http://www1.cs.columbia.edu/~hgs/research/projects/simvoice/simvoice/docs/tts.pdf)

Eine Kopie ist auch in [diesem Repository](https://github.com/david-acm/NVDA-IBMTTS-Driver) erhältlich.

[Pyibmtts: Python-Wrapper für IBM TTS, entwickelt von Peter Parente](https://sourceforge.net/projects/ibmtts-sdk/)

Siehe die Dateien

[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)
oder [tts.txt.](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)
