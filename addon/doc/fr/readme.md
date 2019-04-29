# Pilote IBMTTS, extension pour NVDA #
  Cette extension implémente la compatibilité NVDA avec le synthétiseur IBMTTS.
  Nous ne pouvons pas distribuer les bibliothèques IBMTTS. Donc, c'est juste le pilote.
  Si vous souhaitez améliorer ce pilote, n'hésitez pas à envoyer librement vos pull requests via github !

# Caractéristiques :
* Prise en charge des  paramètres de voix, variante, débit, hauteur, inflexion et volume.
* Prise en charge des  paramètres supplémentaire taille de la tête, raucité, souffle.  Créez votre propre voix !
* Activer ou désactiver les balises de changement de voix. Désactivez-les pour vous protéger contre les codes malveillants des  farceurs, activez-les pour permettre de faire beaucoup de choses amusantes avec le synthétiseur. Un plaisir garanti en toute sécurité !
* Voix turbo. Si le synthétiseur ne vous parle pas assez vite, activez  la voix turbo et obtenez la vitesse maximale !
* Changement automatique de langue. Laissez le synthétiseur parler dans la bonne langue !
* Prise en charge d'indexation. Le curseur ne sera jamais perdu lors de l'utilisation des fonctionnalités lire tout.
* Expressions de filtre anti-crash. Le pilote reconnaît les expressions pouvant endommager le fonctionnement du synthétiseur.

# Exigences.
## NVDA.
  Vous avez besoin de NVDA 2018.4 ou une version ultérieure. Ce pilote est compatible avec Python 3, vous pouvez donc l’utiliser avec les futures versions de NVDA. Une fois que NVDA avec Python 3 sera disponible, ce pilote ne sera plus compatible avec Python 2.7. Veuillez utiliser les dernières versions de NVDA. C'est gratuit !

## Bibliothèques du synthétiseur IBMTTS.
  Ce n'est que le pilote, vous devez vous procurer les bibliothèques ailleurs.

# Installation.
  Installez-le simplement comme n'importe quel extension NVDA. Ouvrez ensuite les paramètres du dialogue NVDA et dans la catégorie IBMTTS définissez le chemin des fichiers IBMTTS.
  Également dans cette catégorie, vous pouvez copier les fichiers externes IBMTTS dans l'extension.
  Remarque : si le synthétiseur est dans l'extension, le pilote mettra à jour automatiquement les chemins du fichier ini. Vous pouvez donc l'utiliser sur les versions portables de NVDA.

# Empaquetage de l'extension pour sa distribution.
  Ouvrez une ligne de commande, changer le dossier racine de l'extension et exécutez la commande scons. L'extension créée, s'il n'y a pas d'erreur, sera placée dans le dossier racine de l'extension.

## Notes:
* Les outils scons et gettext sur ce projet sont uniquement compatibles avec  Python 3. Ils ne fonctionnent pas avec Python 2.7.
* Vous pouvez ajouter les fichiers supplémentaires requis de IBMTTS dans l'extension (pour un usage personnel uniquement). Copiez-les simplement dans "addon \ synthDrivers \ ibmtts". Définissez le nom de la bibliothèque par défaut sur "settingsDB.py" si nécessaire.