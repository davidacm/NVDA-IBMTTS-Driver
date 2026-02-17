#  Controlador IBMTTS, complement per a NVDA#

Aquest complement implementa compatibilitat de NVDA amb el sintetitzador IBMTTS.
No podem distribuir les biblioteques IBMTTS. Així que només és el conductor.
Si voleu millorar aquest controlador, no dubteu a enviar les vostres sol·licituds de pull requests a través de GitHub!

Tot i que aquest controlador és compatible amb les biblioteques d'Eloquence (ja que l'Eloquence té el mateix api que l'IBMTTS) no es recomana utilitzar l'Eloquence amb aquest controlador a causa de problemes de llicència. Abans d'utilitzar qualsevol biblioteca de síntesi amb aquest controlador, es recomana obtenir primer els drets d'ús de la llicència.

Aquest controlador es va desenvolupar amb la documentació disponible per a IBMTTS, disponible públicament a la web. Vegeu la secció de referències per a més detalls.

## Descarrega

L'última versió està disponible per a [descarregar en aquest enllaç](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

## Què és el sintetitzador IBMTTS?

ViaVoice TTS és un motor de text a veu desenvolupat per IBM, que sintetitza la representació textual del llenguatge humà en la parla.

## Característiques i configuració.

* Suport de veu, variant, entonació, to, flexió i ajust de volum.
* Suport de paràmetres extra com Mida del cap, Rugositat, Respiració. Crea la teva pròpia veu!
* Habilita o deshabilita les etiquetes de canvi de veu. Desactiva-les per a protegir-te de codis maliciosos de bromistes, activa-les per a fer moltes coses divertides amb el sintetitzador. Requereix un ajust addicional amb NVDA perquè funcioni correctament.
* Turbo de veu. Si el sintetitzador no et parla suficientment ràpid, a continuació, habilitar i obtenir la màxima velocitat de veu!
* commutació d'idioma automàtic. Deixa que el sintetitzador et llegeixi text en l'idioma correcte quan estigui marcat.
* filtratge complet. Aquest controlador inclou un conjunt complet de filtres per corregir fallades i altres comportaments estranys del sintetitzador.
* Suport per al diccionari. Aquest controlador admet la integració de paraules especials, arrels i diccionaris d'usuari d'abreviació per a cada idioma. Es poden obtenir conjunts de diccionaris preparats del [repositori de diccionari de la comunitat](https://github.com/thunderdrop/IBMTTSDictionaries) o del [repositori alternatiu de Mohamed00 (amb diccionaris de síntesi d'IBM)](https://github.com/mohamed00/AltIBMTTSDictionaries)

### Configuracions extra:

* Habilita l'expansió de l'abreviatura: commuta l'expansió de les abreviatures. Tingueu en compte que desactivar aquesta opció també desactivarà l'expansió de les abreviatures especificades als diccionaris d'abreviatura proporcionats per l'usuari.
* Habilita la predicció de frases: si aquesta opció està activada, el sintetitzador intentarà predir on es produiran les pauses en frases basades en la seva estructura, per exemple, utilitzant paraules com "i" o "el" com a límits de frases. Si aquesta opció està desactivada, només s'aturarà si es troben comes o altres signes de puntuació.
* Pauses: Es tracta d'un quadre combinat amb tres opcions.
  * No escurça: les pauses no s'escurcen en absolut, i les pauses originals d'IBMTTS s'utilitzaran en tots els casos.
  * Escurça només al final del text: les pauses dels símbols de puntuació com ara els punts i les comes no s'escurcen, sinó que s'escurcen quan el text acaba, per exemple quan es prem NVDA+t dues vegades ràpidament per escriure la barra de títol d'una aplicació de caràcter per caràcter.
  * Escurça totes les pauses: s'escurçaran totes les pauses, incloses les pauses de puntuació i les pauses que es produeixen al final del text.
* Envia sempre la configuració actual de la veu: hi ha un error al sintetitzador que ocasionalment farà que la configuració de la parla i la del to es reiniciï breument als seus valors predeterminats. La causa d'aquest problema és actualment desconeguda, però una solució és enviar contínuament la taxa de parla actual i la configuració del to. Aquesta opció s'ha d'habilitar generalment. No obstant això, s'hauria d'inhabilitar si es llegeix text que conté etiquetes de veu de cita prèvia.
* Taxa de mostra: canvia la qualitat del so del sintetitzador. Més útil per a IBMTTS, on establir la freqüència de mostreig a 8 kHz permet l'accés a un nou conjunt de veus.

### Configuració de la categoria IBMTTS.

Aquest complement té la seva pròpia categoria de configuració dins de les opcions NVDA, per gestionar algunes funcionalitats internes no relacionades amb la síntesi de veu.

* Comprova automàticament si hi ha actualitzacions per a IBMTTS: Si aquesta opció està marcada, el complement comprovarà diàriament si hi ha noves versions disponibles.
* Comproveu si hi ha actualitzacions: comproveu manualment si hi ha actualitzacions noves del complements .
* Adreça de la carpeta IBMTTS: El camí per carregar la biblioteca IBMTTS. Pot ser absoluta o relativa.
* Nom de la biblioteca IBMTTS (dll): El nom de la biblioteca (dll). No inclou camins, només el nom amb l'extensió, típicament ".dll".
* Navega per la biblioteca IBMTTS... Obre un diàleg de navegació de fitxers per a cercar la biblioteca IBMTTS al sistema. Es guardarà com un camí absolut.
* Copia els fitxers IBMTTS en un complement (pot ser que no funcioni per a algunes distribucions IBMTTS): Si s'ha establert el camí de la biblioteca per a IBMTTS, copiarà tots els fitxers de carpeta a un complement nou anomenat eciLibraries i actualitzarà el camí actual a un camí relatiu. És molt útil en versions portàtils NVDA. Només funciona per a biblioteques que utilitzen fitxers «eci.ini» per a la informació del llenguatge de veu. Si la biblioteca utilitza el registre de Windows, aquesta opció no funcionarà.

Nota: La funcionalitat d'actualització automàtica o manual no eliminarà els fitxers interns del complement. Si utilitzeu les vostres biblioteques en aquest lloc, podeu utilitzar aquesta funció amb seguretat. Les vostres biblioteques estaran segures.

## Requisits.

### NVDA.

Necessites NVDA 2019.3 o posterior.

### Biblioteques de sintetitzadors IBMTTS.

Aquest és només el controlador, heu d'obtenir les biblioteques d'un altre lloc.
Aquest controlador admet les biblioteques lleugerament més noves que afegeixen suport per a l'idioma de l'Àsia Oriental, i té correccions específiques per a la codificació correcta del text. Però les biblioteques més antigues sense això haurien de funcionar.
A partir de la versió 21.03A1, aquest controlador també funciona amb les biblioteques encara més noves d'IBM, en lloc de només les de SpeechWorks. S'inclou un conjunt de correccions independents per a aquestes biblioteques, i es comptabilitzen les llengües addicionals i altres diferències. Les veus Concatenatives són compatibles, i es pot accedir establint la freqüència de mostreig a 8 kHz després d'instal·lar veus. Per obtenir els millors resultats, utilitzeu la construcció de juny de 2005 d'ibmeci.dll (versió 7.0.0.0) ja que les versions més antigues poden ser inestables quan es rep text ràpidament, per exemple, desplaçant ràpidament a través d'elements en una llista. També cal tenir en compte que si esteu utilitzant biblioteques IBMTTS cantoneses o xineses de Hong Kong, és possible que vulgueu desactivar la funcionalitat ortogràfica d'ús si s'admet l'opció, per evitar que alguns caràcters d'aquests idiomes s'escriuen utilitzant el pinyin al qual es converteixen internament.

## Instal·lació.

Només cal instal·lar-lo com a complement NVDA. A continuació, obriu la configuració del diàleg NVDA i establiu els fitxers de carpeta IBMTTS a la categoria IBMTTS.
També en aquesta categoria podeu copiar els fitxers IBMTTS externs en un complement per utilitzar-los localment.

## Contribuir a la traducció.

Per tal de facilitar la vostra feina, he deixat una
[plantilla de traducció a la branca mestra.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot)

Per a la documentació, he creat un fitxer anomenat ["docChangelog-for-translators.md".](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/docChangelog-for-translators.md)
Podeu utilitzar aquest fitxer per veure què s'ha canviat a la documentació i actualitzar la documentació per al vostre idioma.

Si voleu traduir aquest complement a un altre idioma i no voleu obrir un compte de github o instal·lar Python i altres eines necessàries per a la traducció, feu els passos següents:

1. Utilitza
[aquesta plantilla](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot),
com a base per a l'idioma de destinació.
2. Baixa
["poedit"](https://poedit.net/),
Aquest programari us ajudarà a gestionar les cadenes de traducció.
3. Si també voleu traduir la documentació, podeu veure els nous canvis de la documentació
[en aquest enllaç.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/docChangelog-for-translators.md) Aquí podeu veure la [documentació en anglès completa.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/readme.md)
4. Un cop hagis acabat la traducció, pots enviar-me-la a: "dhf360".gmail.com".

No necessitareu compilar els fitxers d'origen. Ho faré quan publiqui una nova versió del complement. Esmentaré el teu nom en el commit respectiu. Si no vols que t'esmenti, fes-m'ho saber al correu electrònic.

Nota: assegureu-vos que heu utilitzat la darrera plantilla de cadenes de traducció.

Aquest és un mètode alternatiu. Si vols, sempre pots anar pel camí habitual. fes un fork d'aquest repo, actualitza la traducció per al vostre idioma i envia'm un PR. Però d'aquesta manera només s'afegirà més complexitat per a tu.

## Empaquetar el complement per a la seva distribució.

1. Instal·leu el Python, actualment s'utilitza el Python 3.7, però podeu utilitzar una versió més nova.
2. Instal·leu gettext, podeu baixar una distribució per a Windows en [aquest enllaç.](https://mlocati.github.io/articles/gettext-iconv-windows.html) Si utilitzeu Windows 64 bits, recomano [aquesta versió.](https://github.com/mlocati/gettext-iconv-windows/releases/download/v0.21-v1.16/gettext0.21-iconv1.16-shared-64.exe)
3. (opcional però recomanable pas) crear un entorn virtual Python per a ser utilitzat per gestionar complements NVDA. A la consola, utilitzeu «python -m venv PAT".TO".FOLDER». On PATTOTO.FOLDER és el camí del teu camí desitjat per a l'entorn virtual.
4. Si heu fet el pas 2, aneu a PAT".TO".FOLDER i dins de la carpeta scripts, executeu «activa». El nom de l'entorn s'ha de mostrar a l'indicador de la consola.
5. Clona aquest repositori en la ruta desitjada: "git clone https://github.com/davidacm/NVDA-IBMTTS-Driver.git".
6. En la mateixa instància de consola, aneu a la carpeta d'aquest repositori.
7. Instal·la els requisits: «pip install -r requirements.txt».
8. Executa l'ordre de les icones. El complement creat, si no hi ha errors, es col·loca al directori arrel d'aquest repositori.

Un cop tanqueu la consola, l'entorn virtual es desactiva.

### Empaquetar les biblioteques com un complement independent.

No es recomana incloure les biblioteques amb aquest controlador. És perquè si l'usuari actualitza el controlador des del
[repositori oficial](https://github.com/davidacm/NVDA-IBMTTS-Driver),
utilitzant l'instal·lador de complements NVDA, s'eliminarà la versió antiga, incloses les biblioteques. Una solució per a això és instal·lar les biblioteques en un complement separat.
[Seguiu aquest enllaç](https://github.com/davidacm/ECILibrariesTemplate)
saber empaquetar les biblioteques en un complement separat.

### Notes:

* Si utilitzeu la funció d'actualització interna (manual o automàtica) les biblioteques no s'eliminaran encara que estiguin dins del complement.
* si el sintetitzador està dins del complement o a
["eciLibraries"](https://github.com/davidacm/ECILibrariesPlantilla)
complement, el controlador actualitzarà automàticament els camins de la biblioteca de l'ini. Per tant, podeu utilitzar-lo en versions portàtils NVDA.
* quan utilitzeu el botó «Copia fitxers IBMTTS en un complement», es crearà un complement nou. Per tant, si voleu desinstal·lar IBMTTS, haureu de desinstal·lar dos complements: «conductor d'IBMTTS» i «biblioteques Eci».
* les icones i les eines gettext d'aquest projecte són compatibles només amb Python 3. No funciona amb Python 2.7.
* Podeu posar els fitxers IBMTTS addicionals requerits al complement (només per a ús personal). Només cal copiar-los a la carpeta "addon\synthDrivers\ibmtts". Ajusta el nom de la biblioteca per defecte a «settingsDB.py» si cal.
* si el camí de la biblioteca configurada no és relatiu, aquest complement no actualitzarà els camins al fitxer «eci.ini». El controlador assumeix que quan s'utilitzen camins absoluts, els camins són correctes a "eci.ini" i evitaran fer cap actualització. Tingues això en compte en establir el camí de les biblioteques. Si no eren correctes, això podria causar errors que faran que NVDA no parli quan utilitzeu aquest sintetitzador.

## Informació de problemes:

Si trobeu un problema de seguretat amb algunes de les biblioteques que són compatibles amb aquest controlador, si us plau, no obriu un problema de github ni comenteu-lo als fòrums abans de resoldre el problema. Informeu del problema en [aquest formulari.](https://docs.google.com/forms/d/123gSqayOAsIQLx1NiI98fEqr46oiJRZ9nNq0)KIF9WU/edit)

Si el problema no falla al controlador o al lector de pantalla, obriu aquí un [problema de Github.](https://github.com/davidacm/NVDA-IBMTTS-Driver/issues)

## Referències.

Aquest controlador es basa en l'IBM tts sdk, la documentació està disponible a:
[aquest enllaç](http://web.archive.org/web/20191125091344/http://www.wizzardsoftware.com/docs/tts.pdf)

també a la universitat de Columbia
[aquest enllaç](http://www1.cs.columbia.edu/)hgs/research/projects/simvoice/simvoice/docs/tts.pdf)

O podeu obtenir una còpia de seguretat a [aquest dipòsit](https://github.com/david-acm/NVDA-IBMTTS-Driver)

[pyibmtts: embolcall de Python per a IBM TTS desenvolupat per Peter Parente](https://sourceforge.net/projects/ibmtts-sdk/)

Vegeu els fitxers de còpia de seguretat aquí:

[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)

o [tts.txt.](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)
