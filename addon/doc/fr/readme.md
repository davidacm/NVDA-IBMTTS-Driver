# Pilote IBMTTS, extension pour NVDA #
  Cette extension implémente la compatibilité NVDA avec le synthétiseur IBMTTS.
  Nous ne pouvons pas distribuer les bibliothèques IBMTTS. Donc, c'est juste le pilote.
  Si vous souhaitez améliorer ce pilote, n'hésitez pas à envoyer librement vos pull requests via GitHub !

# Télécharger.
La dernière version est disponible [en téléchargement sur ce lien](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

# Caractéristiques :
* Prise en charge des  paramètres de voix, variante, débit, hauteur, inflexion et volume.
* Prise en charge des  paramètres supplémentaire taille de la tête, enrouement , respiration.  Créez votre propre voix !
* Activer ou désactiver les balises de changement de voix. Désactivez-les pour vous protéger contre les codes malveillants des  farceurs, activez-les pour permettre de faire beaucoup de choses amusantes avec le synthétiseur. Nécessite une modification supplémentaire avec NVDA cependant pour le faire fonctionner correctement.
* Voix turbo. Si le synthétiseur ne vous parle pas assez vite, activez  la voix turbo et obtenez la vitesse maximale !
* Changement automatique de langue. Laissez le synthétiseur vous lire du texte dans la bonne langue lorsqu'il est marqué.
* Filtrage extensible. Ce pilote comprend un large ensemble de filtres pour résoudre les chocs et autres comportements étranges du synthétiseur.
* Prise en charge du dictionnaire. Ce pilote prend en charge l'intégration de mots spéciaux, dictionnaires racines et dictionnaires d'abréviation des utilisateurs pour chaque langue. Les ensembles de dictionnaires prêts à l'emploi peuvent être obtenus à partir du [repos du dictionnaire de la communauté](https://github.com/thunderdrop/IBMTTSDictionaries) ou à partir du [repos alternatif  de mohamed00 (avec des dictionnaires du synthétiseur IBM)](https://github.com/mohamed00/AltIBMTTSDictionaries)

# Exigences.
## NVDA.
  Vous avez besoin de NVDA 2019.3 ou une version ultérieure.

## Bibliothèques du synthétiseur IBMTTS.
  Ce n'est que le pilote, vous devez vous procurer les bibliothèques ailleurs.  
  Ce pilote prend en charge  les bibliothèques légèrement plus récentes qui ajoutent un support de langue est-asiatique et disposent de corrections spécifiques pour le codage approprié du texte. Cependant, les bibliothèques les plus anciennes sans cela devraient fonctionner.  
  À partir de la version 21.01, le pilote prend également en charge l'intégration appropriée avec les binaires encore plus récents d'IBM, au lieu de seulement des binaires de  SpeechWorks. Un ensemble de corrections indépendantes est inclus pour ce pilote, et des langues supplémentaires et d'autres différences sont prises en compte. Seules les voix formantes sont prises en charge actuellement. Merci à @mohamed00 pour ce travail. Notez que lorsque vous utilisez les bibliothèques IBM, vous devez désactiver l'option Toujours envoyer les paramètres de la voix actuelle.

# Installation.
  Installez-le simplement comme n'importe quel extension NVDA. Ouvrez ensuite les paramètres du dialogue NVDA et dans la catégorie IBMTTS définissez le chemin des fichiers IBMTTS.
  Également dans cette catégorie, vous pouvez copier les fichiers externes IBMTTS dans l'extension.


# Empaquetage de l'extension pour sa distribution.
  Ouvrez une ligne de commande, changer le dossier racine de l'extension et exécutez la commande scons. L'extension créée, s'il n'y a pas d'erreur, sera placée dans le dossier racine de l'extension.

## Notes:

* Si le synthétiseur est dans cette extension ou dans l'extension "eciLibraries", le pilote mettra à jour automatiquement les chemins du fichier ini. Vous pouvez donc l'utiliser sur les versions portables de NVDA.
* Lorsque vous utilisez le bouton "Copier les fichiers IBMTTS dans une extension", il créera une nouvelle extension dans NVDA. Par conséquent, si vous souhaitez désinstaller IBMTTS, vous devez désinstaller deux extensions: "Pilote IBMTTS" et "Eci libraries".
* Les outils scons et gettext sur ce projet sont uniquement compatibles avec  Python 3. Ils ne fonctionnent pas avec Python 2.7.
* Vous pouvez ajouter les fichiers supplémentaires requis de IBMTTS dans l'extension (pour un usage personnel uniquement). Copiez-les simplement dans "addon \ synthDrivers \ ibmtts". Définissez le nom de la bibliothèque par défaut sur "settingsDB.py" si nécessaire.

# Références.
 Ce pilote est basé sur le SDK de Viavoice de IBM (IBMTTS) la documentation est disponible sur [ce lien](http://web.archive.org/web/20191125091344/http://www.wizzardsoftware.com/docs/tts.pdf)

ou vous pouvez trouver une copie sur [ce repos](https://github.com/david-acm/NVDA-IBMTTS-Driver)

Voir les fichiers

[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)
ou [tts.txt.](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)
