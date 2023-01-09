# Driver IBMTTS, componente aggiuntivo per NVDA
Questo componente aggiuntivo implementa la compatibilità di NVDA con il sintetizzatore IBMTTS.
Non possiamo distribuire le librerie di IBMTTS. Questo è solo il driver.
Se vuoi migliorare questo driver, sentiti libero di inviare le tue pull requests!
Sebbene questo driver sia compatibile con le librerie Eloquence (dal momento che Eloquence ha la stessa API di IBMTTS) non è consigliabile utilizzare Eloquence con questo driver a causa di problemi di licenza. Prima di utilizzare qualsiasi libreria di sintesi con questo driver, si consiglia innanzitutto di ottenere i diritti di utilizzo della licenza.
Questo driver è stato sviluppato con la documentazione disponibile per IBMTTS, pubblicamente disponibile sul web. Vedere la sezione riferimenti per maggiori dettagli.
## Download.
L'ultima versione è disponibile per il download a [questo link](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)
## Che cos'è il sintetizzatore IBMTTS?
ViaVoice TTS è un motore di sintesi vocale sviluppato da IBM, che sintetizza la rappresentazione testuale del linguaggio umano in parlato.
## Caratteristiche:
* Supporto per l'impostazione di voce, variante, velocità, tono, inflessione e volume.
* Supporto per le impostazioni dei parametri extra per dimensioni della testa, raucedine e aspirazione. Crea la tua voce!
* Abilita o disabilita i tag vocali backquote. Disabilitali per proteggerti dai codici dannosi dei jolly, abilitali per fare molte cose divertenti con il sintetizzatore. Richiede alcune modifiche aggiuntive con NVDA per farli funzionare correttamente.
* Aumento velocità. Se il sintetizzatore non  parla abbastanza velocemente, abilitalo e ottieni la massima velocità vocale!
* Cambiamento automatico della lingua. Lascia che il sintetizzatore ti legga il testo nella lingua corretta quando contrassegnato.
* Filtraggio completo. Questo driver include un set completo di filtri per correggere arresti anomali e altri comportamenti strani del sintetizzatore.
* Supporto per i dizionari. Questo driver supporta l'integrazione di parole speciali, radici e dizionari utente di abbreviazioni per ciascuna lingua. I set di dizionari già pronti possono essere ottenuti dal [repository dei dizionari della comunità](https://github.com/thunderdrop/IBMTTSDictionaries) o dal [repository alternativo di mohamed00 (con dizionari del sintetizzatore IBM)](https://github.com/mohamed00/AltIBMTTSDictionaries)
## Impostazioni aggiuntive:
* Abilita espansione abbreviazioni: attiva/disattiva l'espansione delle abbreviazioni. Si noti che la disattivazione di questa opzione disabiliterà anche l'espansione di qualsiasi abbreviazione specificata nei dizionari delle abbreviazioni forniti dall'utente.
* Abilita previsione della frase: se questa opzione è abilitata, il sintetizzatore proverà a prevedere dove si verificherebbero le pause nelle frasi in base alla loro struttura, ad esempio utilizzando parole come "e" o "il" come limiti della frase. Se questa opzione è disattivata, verranno aggiunte delle pause solo se si incontrano virgole o altra punteggiatura simile.
* Accorcia le pause: abilita questa opzione per pause di punteggiatura più brevi, come quelle viste in altri screen reader.
* Invia sempre le impostazioni vocali correnti: c'è un bug nel sintetizzatore che occasionalmente causa un breve ripristino delle impostazioni vocali e del tono ai valori predefiniti. La causa di questo problema è attualmente sconosciuta, tuttavia una soluzione alternativa consiste nell'inviare continuamente le impostazioni correnti della velocità e del tono della voce. Questa opzione dovrebbe generalmente essere abilitata, ma deve essere disabilitata se si legge testo che contiene tag vocali backquote.
* Frequenza di campionamento: cambia la qualità del suono del sintetizzatore. Molto utile per IBMTTS, dove l'impostazione della frequenza di campionamento su 8 kHz consente l'accesso a un nuovo set di voci.
## Requisiti.
### NVDA.
Hai bisogno di NVDA 2019.3 o versioni successive.
### Librerie del sintetizzatore IBMTTS.
Questo è solo il driver, devi ottenere le librerie altrove.
Questo driver supporta le librerie leggermente più recenti che aggiungono il supporto per le lingue dell'Asia orientale e dispone di correzioni specifiche per la corretta codifica del testo. Tuttavia, le librerie più vecchie senza questo dovrebbero funzionare.
A partire dalla versione 21.03A1, questo driver funziona anche con le librerie ancora più recenti di IBM, anziché solo con quelle di SpeechWorks. È inclusa una serie di correzioni indipendenti per tali librerie e vengono prese in considerazione le lingue aggiuntive e altre differenze. Le voci concatenative sono supportate e sono accessibili impostando la frequenza di campionamento su 8 kHz dopo aver installato le voci. Per risultati ottimali, utilizzare la build di giugno 2005 di ibmeci.dll versione 7.0.0.0, poiché le versioni precedenti possono essere instabili durante la ricezione rapida del testo, ad esempio scorrendo rapidamente gli elementi in un elenco.
## Installazione.
Basta installarlo come un qualsiasi componente aggiuntivo per NVDA. Dopo l'installazione apri la finestra di dialogo delle impostazioni  di NVDA e imposta i file della cartella IBMTTS nella categoria IBMTTS. In questa categoria è anche possibile copiare i file di IBMTTS esterni in un componente aggiuntivo per utilizzarli localmente.
## Contribuire alla traduzione.
Per facilitarti il  lavoro, ho lasciato un [modello di traduzione](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot) nel ramo master. Se vuoi tradurre questo componente aggiuntivo in un'altra lingua e non vuoi aprire un account github o installare python e altri strumenti necessari per latraduzione, procedi come segue:
1. Usa [questo modello](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot) come base per la lingua di destinazione.
2. Scarica ["poedit"](https://poedit.net/), questo software ti aiuterà a gestire le stringhe di traduzione.
3. Se vuoi tradurre anche la documentazione, puoi farlo da quella in inglese a [questo link](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/README.md).
4. Una volta terminata la traduzione, puoi inviarmela a: "dhf360@gmail.com".

Non dovrai compilare i file sorgente. Lo farò io quando rilascerò una nuova versione del componente aggiuntivo. Menzionerò il tuo nome nel rispettivo commit. Se non desideri essere menzionato, fammelo sapere nell'e-mail.
Nota: assicurati di aver utilizzato l'ultimo modello di stringhe di traduzione.
Questo è un metodo alternativo. Se vuoi, puoi sempre procedere con il metodo classico. Effettua il fork di questo repository, aggiorna la traduzione per la tua lingua e inviami una PR, ma in questo modo sarà solo più complesso per te.
## Creare un pacchetto per la distribuzione.
1. Installa Python, attualmente viene utilizzato Python 3.7, ma puoi utilizzare una versione più recente.
2. Installa gettext, puoi scaricare una distribuzione per Windows da [questo link](https://mlocati.github.io/articles/gettext-iconv-windows.html). Se stai usando Windows a 64 bit, ti consiglio [questa versione](https://github.com/mlocati/gettext-iconv-windows/releases/download/v0.21-v1.16/gettext0.21-iconv1.16-shared-64.exe).
3. (passaggio facoltativo ma consigliato) creare un ambiente virtuale python da utilizzare per gestire i componenti aggiuntivi di NVDA. Nella console, usa "python -m venv PERCORSO DELLA CARTELLA", Dove "PERCORSO DELLA CARTELLA" è il percorso della cartella desiderata per l'ambiente virtuale.
4. Se hai eseguito il passaggio 2, vai a "PERCORSO DELLA CARTELLA" e all'interno della cartella degli script, esegui "activate". Il nome dell'ambiente dovrebbe essere mostrato nel pront della console.
5. Clona questo repository nel percorso desiderato: "git clone https://github.com/davidacm/NVDA-IBMTTS-Driver.git".
6. Nella stessa istanza della console, vai alla cartella di questo repository.
7. Installa i requisiti: "pip install -r requirements.txt".
8. Esegui il comando scons. Il componente aggiuntivo creato, se non ci sono stati errori, viene posizionato nella directory principale di questo repository.

Una volta chiusa la console, l'ambiente virtuale viene disattivato.
### Impacchettare le librerie in un componente aggiuntivo separato
Non è consigliabile includere le librerie con questo driver, perché se l'utente aggiorna il driver dal [[repository ufficiale](https://github.com/davidacm/NVDA-IBMTTS-Driver), la vecchia versione verrà eliminata comprese le librerie. Una soluzione a questo problema è installare le librerie in un componente aggiuntivo separato. Segui [questo link](https://github.com/davidacm/ECILibrariesTemplate) per sapere come impacchettare le librerie in un componente aggiuntivo separato.
### Note:
* Se il sintetizzatore si trova all'interno del componente aggiuntivo o nel componente aggiuntivo ["eciLibraries"](https://github.com/davidacm/ECILibrariesTemplate), il driver aggiornerà automaticamente i percorsi della libreria ini in modo da poterlo usare su versioni portable di NVDA.
* Quando si utilizza il pulsante "Copia i file IBMTTS in un componente aggiuntivo", verrà creato un nuovo componente aggiuntivo, quindi se vuoi disinstallare IBMTTS, dovrai disinstallare due componenti aggiuntivi: "Driver IBMTTS" e "eciLibraries".
* Gli strumenti scons e gettext su questo progetto sono compatibili solo con Python 3. Non funzionano con Python 2.7.
* È possibile inserire i file IBMTTS aggiuntivi richiesti nel componente aggiuntivo (solo per uso personale). Basta copiarli nella cartella "addon\synthDrivers\ibmtts". Imposta il nome della libreria predefinita in "settingsDB.py" se necessario.
## Segnalazione di problemi
Se riscontri un problema di sicurezza con alcune delle librerie compatibili con questo driver, non aprire un issue su github né commentarlo sui forum prima che il problema sia risolto. Si prega di segnalare il problema tramite [questo modulo](https://docs.google.com/forms/d/123gSqayOAsIQLx1NiI98fEqr46oiJRZ9nNq0_KIF9WU/edit).
Se il problema non provoca l'arresto anomalo del driver o dello screen reader, apri un issue con github da [qui](https://github.com/davidacm/NVDA-IBMTTS-Driver/issues).
## Riferimenti.
Questo driver è basato su IBM tts sdk, la documentazione è disponibile su: [questo link](http://web.archive.org/web/20191125091344/http://www.wizzardsoftware.com/docs/tts.pdf)
Anche all'università di Columbia a [questo link](http://www1.cs.columbia.edu/~hgs/research/projects/simvoice/simvoice/docs/tts.pdf)
O puoi ottenere una copia di backup da [questo repository](https://github.com/david-acm/NVDA-IBMTTS-Driver)
[pyibmtts: wrapper Python per IBM TTS sviluppato da Peter Parente](https://sourceforge.net/projects/ibmtts-sdk/)
Guarda i file di backup qui:
[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf) o [tts.txt](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)