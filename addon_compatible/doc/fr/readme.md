# Pilote IBMTTS, extension pour NVDA #

  Cette extension implémente la compatibilité NVDA avec le synthétiseur IBMTTS.  
  Nous ne pouvons pas distribuer les bibliothèques IBMTTS. Donc, c'est juste le pilote.  
  Si vous souhaitez améliorer ce pilote, n'hésitez pas à envoyer librement vos pull requests via GitHub !  

Bien que ce pilote soit compatible avec les bibliothèques d'Eloquence puisque Eloquence a la même API que IBMTTS), il n'est pas recommandé d'utiliser Eloquence avec ce pilote en raison de problèmes de licence. Avant d'utiliser des bibliothèques de synthèse avec ce pilote, il est recommandé d'obtenir d'abord les droits d'utilisation des licences.

Ce pilote a été développé avec la documentation disponible pour IBMTTS, accessible au public sur le Web. Voir la section Références pour plus de détails.

## Télécharger.
La dernière version est disponible [en téléchargement sur ce lien](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

## Qu'est-ce que le synthétiseur IBMTTS ?

ViaVoice TTS est un moteur de texte à parole développé par IBM, qui synthétise la représentation textuelle du langage humain en voix.

## Caractéristiques et paramètres.

* Prise en charge des  paramètres de voix, variante, débit, hauteur, inflexion et volume.
* Prise en charge des  paramètres supplémentaire taille de la tête, enrouement , respiration.  Créez votre propre voix !
* Activer ou désactiver les balises de changement de voix. Désactivez-les pour vous protéger contre les codes malveillants des  farceurs, activez-les pour permettre de faire beaucoup de choses amusantes avec le synthétiseur. Nécessite une modification supplémentaire avec NVDA cependant pour le faire fonctionner correctement.
* Voix turbo. Si le synthétiseur ne vous parle pas assez vite, activez  la voix turbo et obtenez la vitesse maximale !
* Changement automatique de langue. Laissez le synthétiseur vous lire du texte dans la bonne langue lorsqu'il est coché.
* Filtrage extensible. Ce pilote comprend un large ensemble de filtres pour résoudre les chocs et autres comportements étranges du synthétiseur.
* Prise en charge du dictionnaire. Ce pilote prend en charge l'intégration de mots spéciaux, dictionnaires racines et dictionnaires d'abréviation des utilisateurs pour chaque langue. Les ensembles de dictionnaires prêts à l'emploi peuvent être obtenus à partir du [dépôt du dictionnaire de la communauté](https://github.com/thunderdrop/IBMTTSDictionaries) ou à partir du [dépôt alternatif  de mohamed00 (avec des dictionnaires du synthétiseur IBM)](https://github.com/mohamed00/AltIBMTTSDictionaries)

### Paramètres supplémentaires:

* Activer l'expansion des abréviations: Bascule l'expansion des abréviations. Notez que la désactivation de cette option désactivera également l'expansion de toute abréviation spécifiée dans les dictionnaires des abréviations fournis par l'utilisateur.
* Activer la prédiction de phrase: Si cette option est activée, le synthétiseur essaiera de prédire où des pauses se produiraient en phrases en fonction de leur structure, par exemple, en utilisant des mots comme "et" ou "le" comme limites de phrase. Si cette option est désactivée, elle ne fera que faire une pause que si des virgules ou d'autres ponctuations sont rencontrées.
* Réduire les pauses: Activez cette option pour des pauses de ponctuation plus courtes, comme celles vues dans d'autres lecteurs d'écran.
* Toujours envoyer les paramètres vocaux: Il y a actuellement un bug dans le synthétiseur qui entraînera parfois les paramètres vocaux  et hauteur à être brièvement réinitialisé à leurs valeurs par défaut. La cause de ce problème est actuellement inconnue, mais une solution de contournement consiste à envoyer en permanence les paramètres vocaux de débit actuelle et de hauteur. Cette option doit généralement être activée. Cependant, il doit être désactivé si la lecture du texte contient des balises de changement de voix.
* Taux d'échantillonnage: Modifie la qualité sonore du synthétiseur. Utile pour IBMTTS, où il est possible de définir le taux d'échantillonnage à 8 kHz permettant d'accéder à un nouvel ensemble de voix.

### Paramètres de la catégorie IBMTTS.

Cette extension a sa propre catégorie de paramètres dans les options de NVDA, pour gérer certaines fonctionnalités internes non liées à la synthèse vocale.

* Rechercher automatiquement les mises à jour pour IBMTTS: Si cette option est cochée, l'extension recherchera quotidiennement les nouvelles versions disponibles.
* Le bouton Rechercher une mise à jour: Recherche manuellement les nouvelles mises à jour de l'extension.
* Adresse du dossier IBMTTS: Le chemin pour charger la bibliothèque IBMTTS. Il peut être absolu ou relatif.
* Nom de la bibliothèque IBMTTS (dll): Le nom de la bibliothèque (dll). N'inclue pas les chemins, seulement le nom avec l'extension, généralement ".dll".
* Rechercher une bibliothèque IBMTTS... Ouvre une boîte de dialogue Explorateur de fichiers pour rechercher la bibliothèque IBMTTS sur le système. Il sera enregistré comme un chemin absolu.
* Copier les fichiers IBMTTS dans une extension. (Cela ne fonctionne peut-être pas pour certaines distributions IBMTTS): Si le chemin de la bibliothèque pour IBMTTS a été défini, il copiera tous les fichiers du dossier dans une nouvel extension appelée eciLibraries et mettra à jour le chemin actuel vers un chemin relatif. Il est très utile dans les versions portables de  NVDA. Il ne fonctionne que pour les bibliothèques qui utilisent des fichiers "eci.ini" pour les informations sur la langue de la voix. Si la bibliothèque utilise le registre de Windows, cette option ne fonctionnera pas.

Remarque: La fonctionnalité de mise à jour automatique ou manuelle ne supprime pas les fichiers internes de l'extension. Si vous utilisez vos bibliothèques à cet endroit, vous pouvez utiliser cette fonction en toute sécurité. Vos bibliothèques seront en sécurité.

## Exigences.
### NVDA.
  Vous avez besoin de NVDA 2019.3 ou une version ultérieure.

### Bibliothèques du synthétiseur IBMTTS.
  Ce n'est que le pilote, vous devez vous procurer les bibliothèques ailleurs.  
  Ce pilote prend en charge  les bibliothèques légèrement plus récentes qui ajoutent un support de langue est-asiatique et disposent de corrections spécifiques pour le codage approprié du texte. Cependant, les bibliothèques les plus anciennes sans cela devraient fonctionner.  
  À partir de la version 21.03A1, le pilote travaille également avec les bibliothèques encore plus récentes d'IBM, au lieu de seulement les SpeechWorks. Un ensemble de correctifs indépendants pour ces bibliothèques est inclus, et les langues supplémentaires et d'autres différences sont prises en compte. Seules les voix concaténatives sont prises en charge et sont accessibles en définissant le taux d'échantillonnage sur 8 kHz après l'installation de la voix. Pour des meilleurs résultats, utilisez la build de Juin 2005 de ibmeci.dll version 7.0.0.0, car les versions plus anciennes peuvent être instables lors de la réception du texte rapidement, par exemple, en faisant rapidement défiler les éléments dans une liste. Notez également que si vous utilisez des bibliothèques IBMTTS cantonaises ou chinoises de Hong Kong, vous voudrez peut-être désactiver la fonction d'épellation si elle est supportée, pour éviter que certains caractères de ces langues ne soient épelés en utilisant le pinyin quand ils sont convertis en interne.

## Installation.
  Installez-le simplement comme n'importe quel extension NVDA. Ouvrez ensuite les paramètres du dialogue NVDA et dans la catégorie IBMTTS définissez le chemin des fichiers IBMTTS.
  Également dans cette catégorie, vous pouvez copier les fichiers externes IBMTTS dans l'extension pour l'utiliser localement, utile pour les versions portables de NVDA.

## Contribuant à la traduction.

Afin de faciliter votre travail, j'ai laissé un 
[modèle de traduction dans la branche master.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot)

Pour la documentation, j'ai créé un fichier appelé ["docChangelog-for-translators.md".](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/docChangelog-for-translators.md)
Vous pouvez utiliser ce fichier pour voir ce qui a été modifié dans la documentation et mettre à jour la documentation de votre langue.

Si vous souhaitez traduire cette extension dans une autre langue et que vous ne souhaitez pas ouvrir un compte GitHub ou installer Python et d'autres outils nécessaires pour la traduction, effectuez les étapes suivantes:

1. Utilisez
[ce modèle](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot),
comme base pour la langue cible.
2. Téléchargez
["poedit"](https://poedit.net/),
ce logiciel vous aidera à gérer les chaînes de traduction.
3. Si vous souhaitez également traduire la documentation, vous pouvez voir les nouveaux changements de la documentation
[sur ce lien.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/docChangelog-for-translators.md) Vous pouvez voir la [documentation en anglais complète ici.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/readme.md)
4. Une fois que vous avez terminé la traduction, vous pouvez m'envoyer à: "dhf360@gmail.com".

Vous n'aurez pas besoin de compiler les fichiers source. Je le ferai lors du lancement d'une nouvelle version de l'extension. Je mentionnerai votre nom dans le commit respectif. Si vous ne voulez pas être mentionné, faites-le moi savoir par e-mail.

Remarque: assurez-vous que vous avez utilisé le dernier modèle de chaînes de traduction.

Il s'agit d'une méthode alternative. Si vous le souhaitez, vous pouvez toujours passer de la manière habituelle. Faire une duplication (Fork) de ce dépôt, mettez à jour la traduction de votre langue, et envoyez-moi un PR. Mais de cette façon, cela ajoutera plus de complexité pour vous.

## Empaquetage de l'extension pour sa distribution.

1. Installez Python, actuellement Python 3.7 est utilisé, mais vous pouvez utiliser une version plus récente.
2. Installez GetText, vous pouvez télécharger une distribution pour Windows sur [ce lien.](https://mlocati.github.io/articles/gettext-iconv-windows.html) Si vous utilisez Windows 64 bits, je recommande [cette version.](https://github.com/mlocati/gettext-iconv-windows/releases/download/v0.21-v1.16/gettext0.21-iconv1.16-shared-64.exe)
3. (étape facultative mais recommandée) Créez un environnement virtuel Python à utiliser pour gérer les extensions NVDA. Dans la console, utilisez "python -m venv PAT_TO_FOLDER". Où  PAT_TO_FOLDER est le chemin de votre chemin souhaité pour l'environnement virtuel.
4. Si vous avez fait l'étape 2, accédez à PAT_TO_FOLDER et à l'intérieur du dossier des scripts, exécutez "activate". Le nom de l'environnement doit être montré dans l'invite de la console.
5. Clonez ce dépôt dans votre chemin souhaité: "git clone https://github.com/davidacm/NVDA-IBMTTS-Driver.git".
6. Dans la même instance de la console, accédez au dossier de ce dépôt.
7. Installez les exigences: "pip install -r requirements.txt".
8. Exécutez la commande scons. L'extension créée, s'il n'y a pas d'erreur, sera placée dans le répertoire racine de ce dépôt.

Une fois que vous fermez la console, l'environnement virtuel est désactivé.

### Empaquetage des bibliothèques comme extension indépendante.

N'est pas recommandé d'inclure les bibliothèques avec ce pilote. C'est parce que si l'utilisateur met à jour le pilote à partir du
[dépôt officiel](https://github.com/davidacm/NVDA-IBMTTS-Driver),
à l'aide de l'installateur de l'extension de NVDA, l'ancienne version sera supprimée, y compris les bibliothèques. Une solution pour cela consiste à installer les bibliothèques dans une extension séparée.
[Suivez ce lien](https://github.com/davidacm/ECILibrariesTemplate)
pour savoir comment empaqueter les bibliothèques dans une extension séparée.

### Notes:

* Si vous utilisez la fonctionnalité de mise à jour interne (manuel ou automatique), les bibliothèques ne seront pas supprimées même si elles se trouvent à l'intérieur de l'extension.
* Si le synthétiseur est dans cette extension ou dans l'extension
["eciLibraries"](https://github.com/davidacm/ECILibrariesTemplate),
le pilote mettra à jour automatiquement les chemins  de la bibliothèque ini. Vous pouvez donc l'utiliser sur les versions portables de NVDA.
* Lorsque vous utilisez le bouton "Copier les fichiers IBMTTS dans une extension", il créera une nouvelle extension dans NVDA. Par conséquent, si vous souhaitez désinstaller IBMTTS, vous devez désinstaller deux extensions: "Pilote IBMTTS" et "Eci libraries".
* Les outils scons et gettext sur ce projet sont uniquement compatibles avec  Python 3. Ils ne fonctionnent pas avec Python 2.7.
* Vous pouvez ajouter les fichiers supplémentaires requis de IBMTTS dans l'extension (pour un usage personnel uniquement). Copiez-les simplement dans  le dossier "addon\synthDrivers\ibmtts". Définissez le nom de la bibliothèque par défaut dans  "settingsDB.py" si nécessaire.
* Si le chemin de la bibliothèque configuré n'est pas relatif, cette extension ne metra pas à jour les chemins dans le fichier "eci.ini". Le pilote suppose que lors de l'utilisation de chemins absolus, les chemins sont corrects dans "eci.ini" et éviteront de faire des mises à jour. Gardez cela à l'esprit lorsque vous définissez le chemin de vos bibliothèques. S'ils n'étaient pas corrects, cela pourrait entraîner des erreurs qui rendront NVDA sans parole lorsque vous utilisez ce synthétiseur.

## Signalant des problèmes:

Si vous trouvez un problème de sécurité avec certaines des bibliothèques compatibles avec ce pilote, veuillez ne pas ouvrir une  incidence (issue) en GitHub ni le commenter sur les forums avant que le problème ne soit résolu. Veuillez signaler le problème sur [ce formulaire.](https://docs.google.com/forms/d/123gSqayOAsIQLx1NiI98fEqr46oiJRZ9nNq0_KIF9WU/edit)

Si le problème ne plante pas le pilote ou le lecteur d'écran, ouvrez une  [incidence (issue) en GitHub par ici.](https://github.com/davidacm/NVDA-IBMTTS-Driver/issues)

## Références.
Ce pilote est basé sur le SDK de Viavoice de IBM (IBMTTS), la documentation est disponible sur
[ce lien](http://web.archive.org/web/20191125091344/http://www.wizzardsoftware.com/docs/tts.pdf)

également à l'Université de Columbia sur
[ce lien](http://www1.cs.columbia.edu/~hgs/research/projects/simvoice/simvoice/docs/tts.pdf)

Ou vous pouvez obtenir une copie sur [ce déppôt](https://github.com/david-acm/NVDA-IBMTTS-Driver)

[pyibmtts: Python wrapper pour IBM TTS développé par Peter Parente](https://sourceforge.net/projects/ibmtts-sdk/)

Voir les fichiers de sauvegarde ici:

[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)

ou [tts.txt.](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)
