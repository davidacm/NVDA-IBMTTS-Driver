# Controlador de IBMTTS, complemento para NVDA #
  Este complemento implementa la compatibilidad de NVDA con el sintetizador IBMTTS.
  No podemos distribuir las librerías de IBMTTS. Esto es únicamente el controlador.
  Si deseas contribuir a mejorar este controlador ¡siéntete libre de enviarnos tus pull requests a través de GitHub!

# Descargar.
La última versión está disponible para [descargar en este enlace](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

# Características:
* Soporte para las configuraciones de voz,variante, velocidad, tono, entonación y volumen.
* Soporte de  parámetros  extra como  tamaño de la cabeza, carraspeo, respiración. ¡Cree su propia voz!
* Habilite o deshabilite las etiquetas de cambio de voz. Desactívalas para protegerte de códigos maliciosos de bromistas, actívalas para hacer muchas cosas divertidas con el sintetizador. Requiere un ajuste adicional con NVDA para que funcione correctamente.
* Turbo de voz. Si el sintetizador no te habla lo suficientemente rápido ¡entonces activa el turbo de voz y obtén la velocidad máxima!
* cambios automáticos de idioma. Permítele al sintetizador que lea el texto en el idioma correcto cuando se marca.
* Filtrado ampliable. El controlador incluye un amplio conjunto de filtros para solucionar choques y otros comportamientos extraños del sintetizador.
* Soporte de diccionario. El controlador soporta la integración de palabras especiales, diccionarios raíces y diccionarios de abreviatura de los usuarios para cada idioma. Se pueden obtener conjuntos de diccionarios preparados [desde el repositorio de diccionario de la comunidad](https://github.com/thunderdrop/IBMTTSDictionaries) o [desde el repositorio alternativo de mohamed00 (con diccionarios del sintetizador IBM)](https://github.com/mohamed00/AltIBMTTSDictionaries)

# requisitos.
## NVDA.
  Necesitas NVDA 2019.3 o posterior.

## Las librerías del sintetizador IBMTTS.
  Esto es solo el controlador, debes buscar las librerías en otro lugar.  
  El controlador soporta las librerías ligeramente más recientes que añaden el soporte del idioma este-asiático, y tiene correcciones específicas para la codificación adecuada del texto. Sin embargo, las librerías más antiguas sin esto deberían funcionar.  
  A partir de la versión 21.03A1, el controlador también funciona con las librerías aún más nuevas de IBM, en lugar de solo los SpeechWorks. Se incluye un conjunto de correcciones independientes para esas librerías, y se tienen en cuenta los idiomas adicionales y otras diferencias. Solo se apoyan las voces formantes en la actualidad. Gracias a @mohamed00 por este trabajo. Tenga en cuenta que cuando se utiliza las librerías de IBM, debes deshabilitar la opción Enviar siempre la configuración de voz actual.

# Instalación.
  Simplemente instálelo como cualquier otro complemento de NVDA. Después abre el diálogo de configuraciones de NVDA, y en la categoría IBMTTS establezca la ruta de los archivos de IBMTTS.
  En esta categoría también puedes copiar los archivos externos de IBMTTS dentro del complemento.
  
# Empaquetar el complemento para su distribución.
  Abra una línea de comandos, cambie al directorio raíz del complemento y ejecute el comando scons. El complemento creado, si no hay errores, será puesto en la carpeta raíz del complemento.

## Notas:

* si el sintetizador está dentro de este complemento o en el complemento "eciLibraries", el controlador actualizará las rutas del archivo ini automáticamente. Así que puedes usarlo en versiones portables de NVDA.
* cuando utilice el botón "Copiar archivos IBMTTS en un add-on", creará un nuevo add-on en NVDA. Por lo tanto, si desea desinstalar IBMTTS, necesitará desinstalar dos complementos: "Controlador de IBMTTS" y "Eci libraries".
* Las herramientas scons y gettext de este proyecto son compatibles con python 3 únicamente. No funcionan en python 2.7.
* Puede agregar  los archivos extra requeridos de IBMTTS dentro del complemento (para uso personal solamente). Simplemente cópielos dentro de "addon\synthDrivers\ibmtts". Ajuste el nombre de la librería por defecto en "settingsDB.py" si es necesario.

#Referencias.
 Este controlador está basado en el SDK de Viavoice de IBM (IBMTTS) la documentación está disponible en [este enlace](http://web.archive.org/web/20191125091344/http://www.wizzardsoftware.com/docs/tts.pdf)

o puede encontrar una copia en [este repositorio](https://github.com/david-acm/NVDA-IBMTTS-Driver)

Vea los archivos

[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)
o [tts.txt.](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)
