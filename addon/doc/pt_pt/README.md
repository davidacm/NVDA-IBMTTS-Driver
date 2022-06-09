# Controlador do IBMTTS, extra para o NVDA #
  Este extra implementa a compatibilidade do NVDA com o sintetizador IBMTTS.
  Não podemos distribuir as bibliotecas do IBMTTS. Este é apenas o controlador.
  Si pretender contribuir para melhorar este controlador, sinta-se livre para enviar-nos as suas pull requests através do GitHub!

# Descarregar.
A última versão está disponível para [transferência neste link](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

# Características:
* Suporte para as configurações de voz,variante, velocidade, entoação, inflecção e volume.
* Suporte de parâmetros extras, tais como tamanho da cabeça, rugosidade, respiração. Crie a sua própria voz!
* Activar ou desactivar as etiquetas de alterações de voz. Desactivar para protecção contra códigos maliciosos, activar para fazer muitas coisas divertidas com o sintetizador. Requer um ajuste adicional com o NVDA para que funcione correctamente.
* Aumento de Velocidade. Caso o sintetizador não fale suficientemente rápido, active o aumento de velocidade para obter a velocidade máxima!
* Alteração automática do idioma. Permitir que o sintetizador leia o texto no idioma correcto quando marcado
* Filtragem ampliada. O controlador inclui um extenso conjunto de filtros para lidar com crashes e outros comportamentos estranhos do sintetizador.
* Suporte a dicionários. O controlador suporta a integração de palavras especiais, dicionários raízes e dicionários de abreviação do utilizador para cada idioma. Conjuntos de dicionários prontos podem ser obtidos [a partir do repositório de dicionários da comunidade](https://github.com/thunderdrop/IBMTTSDictionaries) ou [desde o repositório alternativo do mohamed00 (com dicionários do sintetizador IBM)](https://github.com/mohamed00/AltIBMTTSDictionaries)

# requisitos.
## NVDA.
  Necessita do NVDA 2019.3 ou posterior.

## As bibliotecas do sintetizador IBMTTS.
  Este é apenas o controlador, terá de procurar as bibliotecas noutro lugar.  
  O controlador suporta as bibliotecas ligeiramente mais recentes que adicionam suporte para os idiomas leste-asiáticos, e inclui correcções específicas para a codificação adequada do texto. No entanto, as bibliotecas mais antigas que não incluem isto, também, deveriam de funcionar.  
  A partir da versão 21.03A1, o controlador também funciona com as ainda mais novas bibliotecas IBM, em lugar de apenas com o SpeechWorks. Está incluido um conjunto de correcções independentes para estas bibliotecas, e são levados em conta os idiomas adicionais e outras diferenças. Apenas vozes formantes são actualmente suportadas. Obrigado a @mohamed00 por este trabalho. Tenha em mente que ao utilizar as bibliotecas IBM, deverá desactivar a opção "Enviar sempre as definições de voz actuais".

# Instalação.
  Apenas terá de instalá-lo tal como o faz com quaisquer outros extras do NVDA. Em seguida deverá ir ao diálogo de configurações do NVDA, e, na categoria "IBMTTS", apontar a localização dos ficheiros do IBMTTS.
  Nesta categoria, poderá também copiar os ficheiros externos do IBMTTS para dentro do extra.
  
# Empacotamento do extra para distribuição.
  Abra uma linha de comandos, mude para a directoria raíz do extra e execute o comando scons. O extra criado, se não houver erros, será posto na pasta raíz do extra.

## Notas:

* Se o sintetizador estiver dentro deste extra ou do "eciLibraries", o controlador actualizará automaticamente os caminhos dos ficheiros ini, de modo que poderá ser utilizado em versões portáteis do NVDA.
* Ao utilizar o botão "Copiar os ficheiros do IBMTTS para um extra", criará um novo extra no NVDA. Portanto, se pretender desinstalar o IBMTTS, deverá desinstalar dois extras: "Controlador do IBMTTS" e "eciLibraries".
* As ferramentas scons e gettext neste projecto suportam apenas o python 3. Não funcionam em python 2.7.
* Poderá adicionar os ficheiros extra requeridos do IBMTTS dentro do extra (para utilização pessoal somente). Simplesmente copie-os para dentro de "addon\synthDrivers\ibmtts". Ajuste o nome da biblioteca predefinida no ficheiro "settingsDB.py" se necessário.

# Referências.
 Este controlador é baseado no SDK do IBM ViaVoice (IBMTTS). Poderá encontrar a documentação [neste link](http://web.archive.org/web/20191125091344/http://www.wizzardsoftware.com/docs/tts.pdf)

ou poderá encontrar uma cópia [neste repositório](https://github.com/david-acm/NVDA-IBMTTS-Driver)

Conçulte os seguintes ficheiros:

[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)
ou [tts.txt.](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)
