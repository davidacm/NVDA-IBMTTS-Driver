# Controlador de IBMTTS, complemento para NVDA #
  Este complemento implementa la compatibilidad de NVDA con el sintetizador IBMTTS.
  No podemos distribuir las librerías de IBMTTS. Esto es únicamente el controlador.
  Si deseas contribuir a mejorar este controlador ¡siéntete libre de enviarnos tus pull requests a través de GitHub!

## Descarga.
La última versión está disponible para [descargar en este enlace](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

## Características:
* Soporte para las configuraciones de voz,variante, velocidad, tono, entonación y volumen.
* Soporte de  parámetros  extra como  tamaño de la cabeza, carraspeo, respiración. ¡Cree su propia voz!
* Habilite o deshabilite las etiquetas de cambio de voz. Desactívalas para protegerte de códigos maliciosos de bromistas, actívalas para hacer muchas cosas divertidas con el sintetizador. Requiere un ajuste adicional con NVDA para que funcione correctamente.
* Turbo de voz. Si el sintetizador no te habla lo suficientemente rápido ¡entonces activa el turbo de voz y obtén la velocidad máxima!
* cambios automáticos de idioma. Permítele al sintetizador que lea el texto en el idioma correcto cuando se marca.
* Filtrado ampliable. El controlador incluye un amplio conjunto de filtros para solucionar choques y otros comportamientos extraños del sintetizador.
* Soporte de diccionario. El controlador soporta la integración de palabras especiales, diccionarios raíces y diccionarios de abreviatura de los usuarios para cada idioma. Se pueden obtener conjuntos de diccionarios preparados [desde el repositorio de diccionario de la comunidad](https://github.com/thunderdrop/IBMTTSDictionaries) o [desde el repositorio alternativo de mohamed00 (con diccionarios del sintetizador IBM)](https://github.com/mohamed00/AltIBMTTSDictionaries)

### Configuraciones extra:

* Habilitar diccionario de abreviaturas: activa la expansión de las abreviaturas. Tenga en cuenta que al desactivar esta opción también se desactivará la expansión de cualquier abreviatura especificada en los diccionarios de abreviaturas proporcionados por el usuario.
* Activar predicción de frases: si esta opción está activada, el sintetizador intentará predecir dónde se producirán las pausas en las frases basándose en su estructura, por ejemplo, utilizando palabras como "y" o "el" como límites de la frase. Si esta opción está desactivada, sólo hará una pausa si se encuentran comas u otros signos de puntuación.
* Acortar las pausas: active esta opción para obtener pausas de puntuación más cortas, como las que se ven en otros lectores de pantalla.
* Enviar siempre la configuración de voz actual: actualmente, hay un error en el sintetizador que ocasionalmente hace que la configuración de voz y del tono se restablezca brevemente a sus valores predeterminados. La causa de este problema es actualmente desconocida, sin embargo, una solución es enviar continuamente la configuración actual de la velocidad y el tono. Por lo general, esta opción debería estar activada. Sin embargo, debería estar desactivada si está utilizando binarios de IBM, ya que esta configuración provocará que se inserten pausas muy largas que las harán casi inutilizables, o si está leyendo un texto que contiene etiquetas de voz con comillas.

## requisitos.
### NVDA.
  Necesitas NVDA 2019.3 o posterior.

### Las librerías del sintetizador IBMTTS.
  Esto es solo el controlador, debes buscar las librerías en otro lugar.  
  El controlador soporta las librerías ligeramente más recientes que añaden el soporte del idioma este-asiático, y tiene correcciones específicas para la codificación adecuada del texto. Sin embargo, las librerías más antiguas sin esto deberían funcionar.  
  A partir de la versión 21.03A1, el controlador también funciona con las librerías aún más nuevas de IBM, en lugar de solo los SpeechWorks. Se incluye un conjunto de correcciones independientes para esas librerías, y se tienen en cuenta los idiomas adicionales y otras diferencias. Solo se soportan las voces formantes en la actualidad. Gracias a @mohamed00 por este trabajo. Tenga en cuenta que cuando se utiliza las librerías de IBM, debes deshabilitar la opción Enviar siempre la configuración de voz actual.

## Instalación.
  Simplemente instálelo como cualquier otro complemento de NVDA. Después abre el diálogo de configuraciones de NVDA, y en la categoría IBMTTS establezca la ruta de los archivos de IBMTTS.
  En esta categoría también puedes copiar los archivos externos de IBMTTS dentro del complemento para usarlo localmente, útil para versiones portables de NVDA.

## Contribuyendo a la traducción.

Para facilitar tu trabajo, he dejado una
[plantilla de traducción en la rama principal](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot).
Si quieres traducir este complemento a otro idioma y no quieres abrir una cuenta en github o instalar python y otras herramientas necesarias para la traducción, haz los siguientes pasos:

1. Utiliza
[esta plantilla](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot),
como base para el idioma de destino.
2. Descargue
["poedit"](https://poedit.net/),
este software le ayudará a gestionar las cadenas de traducción.
3. Si quieres traducir también la documentación, puedes utilizar la
[Documentación en inglés en este enlace](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/README.md)
4. Una vez que hayas terminado la traducción, puedes enviármela a "dhf360@gmail.com".

No necesitarás compilar los archivos fuente. Lo haré cuando lance una nueva versión del complemento. Mencionaré tu nombre en el respectivo commit. Si no deseas ser mencionado, házmelo saber en el correo electrónico.

Nota: asegúrate de que has utilizado la última plantilla de cadenas de traducción.

Este es un método alternativo. Si quieres, siempre puedes usar la forma habitual. Haz un fork de este repo, actualiza la traducción para el idioma destino, y envía un PR. Pero esta forma sólo añadirá más complejidad para usted.

## Empaquetar el complemento para su distribución.
  Abra una línea de comandos, cambie al directorio raíz del complemento y ejecute el comando scons. El complemento creado, si no hay errores, será puesto en la carpeta raíz del complemento.

### Empaquetar las librerías como un complemento independiente.
No se recomienda incluir las librerías con este controlador. Es porque si el usuario actualiza el driver desde el
[repo oficial](https://github.com/davidacm/NVDA-IBMTTS-Driver),
la versión antigua será eliminada incluyendo las librerías. Una solución para esto, es instalar las librerías en un complemento separado.
[Siga este enlace](https://github.com/davidacm/ECILibrariesTemplate)
para saber cómo empaquetar las bibliotecas en un complemento separado.

### Notas:

* si el sintetizador está dentro de este complemento o en el complemento "eciLibraries", el controlador actualizará las rutas del archivo ini automáticamente. Así que puedes usarlo en versiones portables de NVDA.
* cuando utilice el botón "Copiar archivos IBMTTS en un add-on", creará un nuevo add-on en NVDA. Por lo tanto, si desea desinstalar IBMTTS, necesitará desinstalar dos complementos: "Controlador de IBMTTS" y "Eci libraries".
* Las herramientas scons y gettext de este proyecto son compatibles con python 3 únicamente. No funcionan en python 2.7.
* Puede agregar  los archivos extra requeridos de IBMTTS dentro del complemento (para uso personal solamente). Simplemente cópielos dentro de "addon\synthDrivers\ibmtts". Ajuste el nombre de la librería por defecto en "settingsDB.py" si es necesario.

## Referencias.
 Este controlador está basado en el SDK de Viavoice de IBM (IBMTTS) la documentación está disponible en [este enlace](http://web.archive.org/web/20191125091344/http://www.wizzardsoftware.com/docs/tts.pdf)

o puede encontrar una copia en [este repositorio](https://github.com/david-acm/NVDA-IBMTTS-Driver)

Vea los archivos

[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)
o [tts.txt.](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)
