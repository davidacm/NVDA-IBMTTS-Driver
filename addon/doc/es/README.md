# Controlador de IBMTTS, complemento para NVDA #

  Este complemento implementa la compatibilidad de NVDA con el sintetizador IBMTTS.
  No podemos distribuir las librerías de IBMTTS. Esto es únicamente el controlador.
  Si deseas contribuir a mejorar este controlador ¡siéntete libre de enviarnos tus pull requests a través de GitHub!

Aunque este driver es compatible con librerías de Eloquence debido a que Eloquence posee la misma api que IBMTTS, no se recomienda usar Eloquence con este controlador debido a problemas de licencias. Antes de usar cualquier librería de síntesis con este controlador, se recomienda obtener los derechos de uso primero.

Este controlador fue desarrollado con la documentación disponible para IBMTTS, disponible públicamente en la web. Ver la sección referencias para más detalles.

## Descarga.
La última versión está disponible para [descargar en este enlace](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

## ¿Qué es el sintetizador IBMTTS?

ViaVoice TTS es un motor de texto a voz desarrollado por IBM, que sintetiza la representación textual del lenguaje humano en voz.

## Características y configuraciones.
* Soporte para las configuraciones de voz,variante, velocidad, tono, entonación y volumen.
* Soporte de  parámetros  extra como  tamaño de la cabeza, carraspeo, respiración. ¡Crea tu propia voz!
* Habilita o deshabilita las etiquetas de cambio de voz. Desactívalas para protegerte de códigos maliciosos de bromistas, actívalas para hacer muchas cosas divertidas con el sintetizador. Requiere un ajuste adicional con NVDA para que funcione correctamente.
* Turbo de voz. Si el sintetizador no te habla lo suficientemente rápido ¡entonces activa el turbo de voz y obtén la velocidad máxima!
* cambios automáticos de idioma. Permítele al sintetizador que lea el texto en el idioma correcto cuando se marca.
* Filtrado ampliable. El controlador incluye un amplio conjunto de filtros para solucionar errores de patrones de texto y otros comportamientos extraños del sintetizador.
* Soporte de diccionario. El controlador soporta la integración de palabras especiales, diccionarios raíces y diccionarios de abreviatura de los usuarios para cada idioma. Se pueden obtener conjuntos de diccionarios preparados [desde el repositorio de diccionario de la comunidad](https://github.com/thunderdrop/IBMTTSDictionaries) o [desde el repositorio alternativo de mohamed00 (con diccionarios del sintetizador IBM)](https://github.com/mohamed00/AltIBMTTSDictionaries)

### Configuraciones extra:

* Habilitar expansión de abreviaturas: activa la expansión de las abreviaturas. Ten en cuenta que al desactivar esta opción también se desactivará la expansión de cualquier abreviatura especificada en los diccionarios de abreviaturas proporcionados por el usuario.
* Activar predicción de frases: si esta opción está activada, el sintetizador intentará predecir dónde se producirán las pausas en las frases basándose en su estructura, por ejemplo, utilizando palabras como "y" o "el" como límites de la frase. Si esta opción está desactivada, sólo hará una pausa si se encuentran comas u otros signos de puntuación.
* Acortar las pausas: activa esta opción para obtener pausas de puntuación más cortas, como las que se ven en otros lectores de pantalla.
* Enviar siempre la configuración de voz actual: actualmente, hay un error en el sintetizador que ocasionalmente hace que la configuración de voz y del tono se restablezca brevemente a sus valores predeterminados. La causa de este problema es actualmente desconocida, sin embargo, una solución es enviar continuamente la configuración actual de la velocidad y el tono. Por lo general, esta opción debería estar activada. Sin embargo, debería estar desactivada si estás utilizando binarios de IBM, ya que esta configuración provocará que se inserten pausas muy largas que las harán casi inutilizables, o si estás leyendo un texto que contiene etiquetas de voz con comillas.
* Frecuencia de muestreo: cambia la calidad del sonido del sintetizador. Útil para IBMTTS, donde establecer la frecuencia de muestreo en 8 kHz permite acceder a un nuevo conjunto de voces.

### Categoría de configuraciones IBMTTS.

Este complemento tiene su propia categoría de configuraciones dentro de las opciones de NVDA, para gestionar algunas funcionalidades internas no relacionadas con la síntesis de voz.

* Buscar automáticamente actualizaciones para IBMTTS: si esta opción está marcada, el complemento verificará diariamente si hay nuevas versiones disponibles.
* Buscar actualización: Verifica manualmente si hay nuevas actualizaciones de este complemento.
* Dirección de carpeta de IBMTTS: la ruta para cargar la librería IBMTTS. Puede ser absoluta o relativa.
* Nombre de la librería de IBMTTS: el nombre de la librería (dll). No incluyas rutas, solo el nombre con la extensión, normalmente ".dll".
* Buscar una librería de IBMTTS... Abre un diálogo  de exploración de archivos para buscar la librería IBMTTS en el sistema. Se guardará como una ruta absoluta.
* Copiar los archivos de IBMTTS en un complemento. (puede no funcionar para algunas distribuciones de IBMTTS): si se ha establecido la ruta de la librería para IBMTTS, copiará todos los archivos de la carpeta en un nuevo complemento llamado "eciLibraries" y actualizará la ruta actual a una relativa. Es útil en las versiones portables de NVDA. Solo funciona para librerías que usan archivos "eci.ini" para la información de los idiomas de voz. Si la librería usa el registro de Windows, esta opción no funcionará.

Nota: La funcionalidad de actualización automática o manual no borrará los archivos internos del complemento. Si mantienes tus librerías en ese lugar, puedes usar esta función con seguridad. Tus librerías estarán a salvo.

## requisitos.
### NVDA.
  Necesitas NVDA 2019.3 o posterior.

### Las librerías del sintetizador IBMTTS.
  Esto es solo el controlador, debes buscar las librerías en otro lugar.  
  El controlador soporta las librerías ligeramente más recientes que añaden el soporte del idioma este-asiático, y tiene correcciones específicas para la codificación adecuada del texto. Sin embargo, las librerías más antiguas sin esto deberían funcionar.  
  A partir de la versión 21.03A1, el controlador también funciona con las librerías aún más nuevas de IBM, en lugar de solo las de SpeechWorks. Se incluye un conjunto de correcciones independientes para esas librerías, y se tienen en cuenta los idiomas adicionales y otras diferencias. Las voces concatenadas son compatibles y se puede acceder a ellas configurando la frecuencia de muestreo en 8 kHz después de instalar las voces. Para obtener mejores resultados, utiliza la compilación de junio de 2005 de ibmeci.dll (versión 7.0.0.0) ya que las versiones anteriores pueden ser inestables al recibir texto rápidamente, por ejemplo, al desplazarse rápidamente por los elementos de una lista. También ten en cuenta que si estás utilizando librerías IBMTTS en chino o cantonés de Hong Kong, es posible que desees deshabilitar la opción "Utilizar funcionalidad de deletreo si está soportada", para evitar que algunos caracteres en estos idiomas se deletreen utilizando el pinyin al que se convierten internamente.

## Instalación.

  Simplemente instálalo como cualquier otro complemento de NVDA. Después abre el diálogo de configuraciones de NVDA, y en la categoría IBMTTS establece la ruta de los archivos de IBMTTS.
  En esta categoría también puedes copiar los archivos externos de IBMTTS dentro del complemento para ser usado localmente, útil para versiones portables de NVDA.

## Contribuyendo a la traducción.

Para facilitar tu trabajo, he dejado una
[plantilla de traducción en la rama principal.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot)

Para la documentación, creé un archivo llamado ["docChangelog-for-translators.md".](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/docChangelog-for-translators.md)
puedes usar ese archivo para ver qué se ha cambiado en la documentación y actualizar la documentación de tu idioma.

Si quieres traducir este complemento a otro idioma y no quieres abrir una cuenta en github o instalar python y otras herramientas necesarias para la traducción, haz los siguientes pasos:

1. Utiliza
[esta plantilla,](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot)
como base para el idioma de destino.
2. Descarga
["poedit,"](https://poedit.net/)
este software te ayudará a gestionar las cadenas de traducción.
3. Si quieres traducir la documentación también, puedes ver los nuevos cambios de la documentación
[en este enlace.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/docChangelog-for-translators.md) Puedes ver la [documentación completa en inglés aquí.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/readme.md)
4. Una vez que hayas terminado la traducción, puedes enviármela a "dhf360@gmail.com".

No necesitarás compilar los archivos fuente. Lo haré cuando lance una nueva versión del complemento. Mencionaré tu nombre en el respectivo commit. Si no deseas ser mencionado, házmelo saber en el correo electrónico.

Nota: asegúrate de que has utilizado la última plantilla de cadenas de traducción.

Este es un método alternativo. Si quieres, siempre puedes usar la forma habitual. Haz un fork de este repo, actualiza la traducción para el idioma destino, y envía un PR. Pero esta forma sólo añadirá más complejidad para ti.

## Empaquetar el complemento para su distribución.

1. Instala python, actualmente se usa python 3.7, pero puedes usar una versión más reciente si lo deseas.
2. Instala Gettext, puedes descargar una distribución para windows en [este enlace.](https://mlocati.github.io/articles/gettext-iconv-windows.html) Si estás usando Windows 64 bits, te recomiendo [esta versión.](https://github.com/mlocati/gettext-iconv-windows/releases/download/v0.21-v1.16/gettext0.21-iconv1.16-shared-64.exe)
3. (paso opcional pero recomendado) crea un entorno virtual de python para administrar los complementos de NVDA. En la consola, usa "python -m venv PAT_TO_FOLDER". Donde PAT_TO_FOLDER es la ruta deseada para el entorno virtual.
4. Si realizaste el paso 2, Ve a PAT_TO_FOLDER y dentro de la carpeta de scripts, ejecuta "activate". El nombre del entorno debe mostrarse en el indicador de la consola.
5. Clona este repositorio en la ruta deseada: git clone "https://github.com/davidacm/NVDA-IBMTTS-Driver.git".
6. En la misma instancia de la consola, ve a la carpeta de este repositorio.
7. Instala los requisitos: "pip install -r requirements.txt".
8. Ejecuta el comando scons. El complemento creado, si no hubo errores, se coloca en el directorio raíz de este repositorio.

Una vez que cierras la consola, el entorno virtual se desactiva.

### Empaquetar las librerías como un complemento independiente.

No se recomienda incluir las librerías con este controlador. Es porque si el usuario actualiza el driver desde el
[repo oficial](https://github.com/davidacm/NVDA-IBMTTS-Driver),
usando el instalador de complementos de NVDA, la versión antigua será eliminada incluyendo las librerías. Una solución para esto, es instalar las librerías en un complemento separado.
[Sigue este enlace](https://github.com/davidacm/ECILibrariesTemplate)
para saber cómo empaquetar las bibliotecas en un complemento separado.

### Notas:

* Si usas la función de actualización interna (manual o automática), las librerías no se eliminarán incluso si están dentro del complemento.
* si el sintetizador está dentro de este complemento o en el complemento "eciLibraries", el controlador actualizará las rutas del archivo ini automáticamente. Así que puedes usarlo en versiones portables de NVDA.
* cuando utilices el botón "Copiar archivos IBMTTS en un add-on", creará un nuevo add-on en NVDA. Por lo tanto, si deseas desinstalar IBMTTS, necesitarás desinstalar dos complementos: "Controlador de IBMTTS" y "Eci libraries".
* Las herramientas scons y gettext de este proyecto son compatibles con python 3 únicamente. No funcionan en python 2.7.
* Puedes agregar  los archivos extra requeridos de IBMTTS dentro del complemento (para uso personal solamente). Simplemente cópialos dentro de "addon\synthDrivers\ibmtts". Ajusta el nombre de la librería por defecto en "settingsDB.py" si es necesario.
* Si la ruta configurada para la librería no es relativa, Este controlador no actualizará las rutas del archivo "eci.ini". El controlador supone que al usar rutas absolutas, las rutas son correctas en "eci.ini" y evitará realizar actualizaciones. Ten esto en cuenta al establecer la ruta de tus librerías. Si no fueran correctas en dicho archivo, podría causar errores que dejarían a NVDA sin habla cuando utilices este sintetizador.

## Reporte de problemas.

Si encuentras un problema de seguridad con algunas de las bibliotecas compatibles con este controlador, no abras un problema de github ni lo comentes en los foros antes de que se resuelva el problema. Informa el problema en [este formulario.](https://docs.google.com/forms/d/123gSqayOAsIQLx1NiI98fEqr46oiJRZ9nNq0_KIF9WU/edit)

Si el problema no perjudica el controlador o el lector de pantallas, abre un [problema de github aquí.](https://github.com/davidacm/NVDA-IBMTTS-Driver/issues)

## Referencias.

Este controlador está basado en el SDK de Viavoice de IBM (IBMTTS) la documentación está disponible en [este enlace](http://web.archive.org/web/20191125091344/http://www.wizzardsoftware.com/docs/tts.pdf)

también en la universidad Columbia en [este enlace](http://www1.cs.columbia.edu/~hgs/research/projects/simvoice/simvoice/docs/tts.pdf)

o puedes encontrar una copia en [este repositorio](https://github.com/david-acm/NVDA-IBMTTS-Driver)

[pyibmtts: envoltorio de Python para IBM TTS desarrollado por Peter Parente](https://sourceforge.net/projects/ibmtts-sdk/)

Consulta los archivos de respaldo aquí:

[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)

o [tts.txt.](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)
