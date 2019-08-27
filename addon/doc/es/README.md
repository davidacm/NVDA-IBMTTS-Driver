# Controlador de IBMTTS, complemento para NVDA #
  Este complemento implementa la compatibilidad de NVDA con el sintetizador IBMTTS.
  No podemos distribuir las librerías de IBMTTS. Esto es únicamente el controlador.
  Si deseas contribuir a mejorar este controlador ¡siéntete libre de enviar tus aportes vía github!

# Características:
* Soporte para las configuraciones de voz,variante, velocidad, tono, entonación y volumen.
* Soporte de  parámetros  extra como  tamaño de la cabeza, carraspeo, respiración. ¡Cree su propia voz!
* Habilite o deshabilite las etiquetas de cambio de voz. Desactívalas para protegerte de códigos maliciosos de bromistas, actívalas para hacer muchas cosas divertidas con el sintetizador. ¡Diversión segura garantizada!
* Turbo de voz. Si el sintetizador no te habla lo suficientemente rápido ¡entonces activa el turbo de voz y obtén la velocidad máxima!
* cambios automáticos de idioma. ¡Permítele al sintetizador hablar en el idioma correcto!
* Soporte de índice. El cursor nunca se perderá al usar las características de leer todo.
* Filtro de expresiones anti crashing. El controlador reconoce las expresiones que pueden dañar el funcionamiento del sintetizador.

# requisitos.
## NVDA.
  Necesitas NVDA 2018.2 o posterior. Este driver es compatible con python 3, así que podrás usarlo con versiones futuras de NVDA. Una vez que NVDA con python 3 sea liberada, este driver dejará de ser compatible con python 2.7. Por favor usa las últimas versiones de NVDA.
   ¡Es gratis!

## Las librerías del sintetizador IBMTTS.
  Esto es solo el controlador, debes buscar las librerías en otro lugar.

# Instalación.
  Simplemente instálelo como cualquier otro complemento de NVDA. Después abre el diálogo de configuraciones de NVDA, y en la categoría IBMTTS establezca la ruta de los archivos de IBMTTS.
  En esta categoría también puedes copiar los archivos externos de IBMTTS dentro del complemento.
  Nota: si el sintetizador se encuentra dentro del complemento, el controlador actualizará las rutas del archivo ini automáticamente. Así que puedes usarlo en versiones portables de NVDA.
  
# Empaquetar el complemento para su distribución.
  Abra una línea de comandos, cambie al directorio raíz del complemento y ejecute el comando scons. El complemento creado, si no hay errores, será puesto en la carpeta raíz del complemento.

## Notas:
* Las herramientas scons y gettext de este proyecto son compatibles con python 3 únicamente. No funcionan en python 2.7.
* Puede agregar  los archivos extra requeridos de IBMTTS dentro del complemento (para uso personal solamente). Simplemente cópielos dentro de "addon\synthDrivers\ibmtts". Ajuste el nombre de la librería por defecto en "settingsDB.py" si es necesario.

#Referencias.
 Este controlador está basado en el SDK de Viavoice de IBM (IBMTTS) disponible en [Este enlace](http://www.wizzardsoftware.com/docs/tts.pdf)

o puede encontrar una copia en [este repositorio](https://github.com/david-acm/NVDA-IBMTTS-Driver)

Vea los archivos
[tts.pdf](https://cdn.jsdelivr.net/gh/david-acm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)
o [tts.txt.](https://cdn.jsdelivr.net/gh/david-acm/NVDA-IBMTTS-Driver/apiReference/tts.txt)