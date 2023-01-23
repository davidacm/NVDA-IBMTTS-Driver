# Controlador do IBMTTS, extra para o NVDA #

  Este extra implementa a compatibilidade do NVDA com o sintetizador IBMTTS.
  Não podemos distribuir as bibliotecas do IBMTTS. Este é apenas o controlador.
  Si pretender contribuir para melhorar este controlador, sinta-se livre para enviar-nos as suas pull requests através do GitHub!

Se bem que este controlador seja compatível com as bibliotecas do ETI Eloquence porque este possui a mesma api do IBMTTS, não é recomendado utilizar o Eloquence com este controlador devido a problemas de licença. Antes de utilizar quaisquer bibliotecas de síntese com este controlador, é recomendado obter primeiro os direitos de utilização.

Este controlador foi desenvolvido com a documentação disponível para o IBMTTS, disponível publicamente na web. Ver a secção de referências para mais detalhes.

## Descarregar.
A última versão está disponível para [transferência neste link](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

## O que é o sintetizador IBMTTS?

O ViaVoice TTS é um motor text-to-speech desenvolvido pela IBM, que sintetiza a representação textual da linguagem humana na fala.

## Características e configurações:

* Suporte para as configurações de voz,variante, velocidade, entoação, inflecção e volume.
* Suporte de parâmetros extras, tais como tamanho da cabeça, rouquidão, respiração. Crie a sua própria voz!
* Activar ou desactivar as etiquetas de alterações de voz. Desactivar para protecção contra códigos maliciosos, activar para fazer muitas coisas divertidas com o sintetizador. Requer um ajuste adicional com o NVDA para que funcione correctamente.
* Aumento de Velocidade. Caso o sintetizador não fale suficientemente rápido, active o aumento de velocidade para obter a velocidade máxima!
* Alteração automática do idioma. Permite que o sintetizador leia o texto no idioma correcto quando marcado.
* Filtragem ampliada. O controlador inclui um extenso conjunto de filtros para lidar com crashes e outros comportamentos estranhos do sintetizador.
* Suporte a dicionários. O controlador suporta a integração de palavras especiais, dicionários raízes e dicionários de abreviação do utilizador para cada idioma. Conjuntos de dicionários prontos podem ser obtidos [a partir do repositório de dicionários da comunidade](https://github.com/thunderdrop/IBMTTSDictionaries) ou [desde o repositório alternativo do mohamed00 (com dicionários do sintetizador IBM)](https://github.com/mohamed00/AltIBMTTSDictionaries)

### Configurações adicionais:

* Habilitar Expansão de Abreviaturas: Activa a expansão das abreviaturas. Note que desactivar esta opção também desactivará a expansão de quaisquer abreviaturas especificadas nos dicionários de abreviaturas fornecidos pelo utilizador.
* Activar a previsão de frases: Se esta opção estiver activada, o sintetizador tentará prever onde se produzirão as pausas nas frases tendo como base a sua própria estrutura, por exemplo, utilizando palavras como "e" e "o" como limites da frase. Se estiver desactivada, só fará uma pausa quando encontrar uma vírgula ou outros sinais de pontuação.
* Redusir pausas: Active esta opção para obter pausas de pontuação mais curtas, como visto em outros leitores de ecrã.
* Sempre enviar as definições de voz actuais: há um erro no sintetizador que ocasionalmente fará com que as definições de velocidade e entoação sejam brevemente repostas aos seus valores por defeito. A causa desta questão é actualmente desconhecida, no entanto, uma solução é enviar continuamente as definições actuais de velocidade e entoação. É suposto que esta opção fique geralmente activada. No entanto, deve ser desactivada durante a leitura de textos contendo etiquetas de alteração de voz.
* Frequência de amostragem: Alterar a qualidade sonora do sintetizador. Isto é mais útil para o IBM ViaVoice, no qual pode-se ajustar a frequência de amostragem para 8 kHz para obter acesso a um novo conjunto de vozes.

### Categoria de configurações do IBMTTS.

Este extra possui a sua própria categoria de opções dentro das configurações do NVDA, para gerir algumas funcionalidades internas não relacionadas com a síntese de voz.

* Verificar automaticamente se há actualizações para o IBMTTS: se esta opção estiver marcada, o extra irá verificar diariamente a existência de novas versões.
* Verificar actualização: Verifica manualmente se há novas actualizações deste extra.
* Localização da Pasta do IBMTTS: o caminho para as bibliotecas do IBMTTS, que tanto pode ser absoluto como relativo.
* Nome da biblioteca do IBMTTS: o nome da biblioteca (dll). Não incluir caminhos, apenas o nome com a extensão, normalmente ".dll".
* Localizar a Biblioteca do IBMTTS... Abre um diálogo de navegação de ficheiros para procurar a biblioteca do IBMTTS no sistema. Será guardado como um caminho absoluto.
* Copiar os ficheiros do IBMTTS para um extra (poderá não funcionar para algumas distribuições do IBMTTS): se definiu o caminho da biblioteca do IBMTTS, esta opção irá copiar todos os ficheiros da pasta para um novo extra chamado "eciLibraries" e actualizará o caminho actual para um caminho relativo. É útil em versões portáteis do NVDA. Isto funciona apenas para as bibliotecas que utilizem o ficheiro "eci.ini" para as informações dos idiomas e vozes. Se a biblioteca utilizar o registo do Windows, esta opção não funcionará.

Nota: A funcionalidade de actualização automática ou manual não apagará os ficheiros internos do extra. Se mantiver as suas bibliotecas aí, pode utilizar isto com segurança. As suas bibliotecas estarão seguras.

## requisitos.
### NVDA.
  Necessita do NVDA 2019.3 ou posterior.

### As bibliotecas do sintetizador IBMTTS.
  Este é apenas o controlador, terá de procurar as bibliotecas noutro lugar.  
  O controlador suporta as bibliotecas ligeiramente mais recentes que adicionam suporte para os idiomas leste-asiáticos, e inclui correcções específicas para a codificação adequada do texto. No entanto, é suposto que as bibliotecas mais antigas que não incluem isto também funcionem.
  A partir da versão 21.03A1, o controlador também funciona com as bibliotecas ainda mais recentes do IBM ViaVoice, em lugar de apenas com o SpeechWorks. Está incluido um conjunto de correcções independentes para estas bibliotecas, e são levados em conta os idiomas adicionais e outras diferenças. As vozes concatenativas são agora suportadas e podem ser encontradas ao ajustar a frequência de amostragem para 8 kHz após a instalação das vozes. Para obter melhores resultados, utilize a compilação de junho de 2005 da ibmeci.dll versão 7.0.0.0, pois as versões mais antigas podem apresentar instabilidade ao receber texto rapidamente, por exemplo, ao deslocar-se muito rapidamente pelos itens de uma lista. Note também que se estiver a utilizar as bibliotecas do IBM ViaVoice nos idiomas Cantonês de Hong Kong ou chinês, poderá querer desactivar a opção "Utilizar funcionalidade de soletrar se suportada", para evitar que alguns caracteres nestas línguas sejam soletrados usando o pinyin, em que são convertidos internamente.

## Instalação.
  Apenas terá de instalá-lo tal como o faz com quaisquer outros extras do NVDA. Em seguida deverá ir ao diálogo de configurações do NVDA, e, na categoria "IBMTTS", apontar a localização dos ficheiros do IBMTTS.
  Nesta categoria, poderá também copiar os ficheiros externos do IBMTTS para dentro do extra.

## Contribuir com a tradução.

Para facilitar o trabalho aos tradutores, deixei um [modelo de tradução no ramo principal](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot).
Para a documentação, criei um ficheiro chamado ["docChangelog-for-translators.md".](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/docChangelog-for-translators.md)
Pode utilizar esse ficheiro para ver o que foi alterado na documentação e actualizar a documentação para a sua língua.
Se pretender traduzir o extra para outro idioma e não quiser criar uma conta no GitHub e instalar o Python e outras ferramentas necessárias para a tradução, execute os seguintes paços:

1. Utilize [este modelo](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot), como base para o idioma de destino.
2. Transfira o ["poedit"](https://poedit.net/), este software o ajudará a gerir as cadeias de tradução.
3. Se quiser traduzir também a documentação, poderá ver as novas alterações da documentação
[neste link](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/docChangelog-for-translators.md) Pode ver a [documentação completa em inglês aqui.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/readme.md)
4. Quando tiver terminado a tradução, poderá enviar-ma a "dhf360@gmail.com".

Não necessita compilar os ficheiros de origem. Fá-lo-ei quando publicar uma nova versão do extra. Mencionarei o seu nome no Commit respectivo. Se não quiser ser mencionado, avise-me a quando do envio do correio electrónico.

Nota: certifique-se de ter utilizado o último modelo de cadeias de tradução.

Este é um método auternativo. Se pretender, poderá sempre utilizar o modo habitual. Faça um fork deste repo, actualize a tradução para o idioma destino e envie uma PR. Entretanto este modo apenas lhe trará maior complexidade. 

## Empacotamento do extra para distribuição.

Nota de tradução: Estas instruções destinam-se aos desenvolvedores de extras e não têm sentido para a maioria dos utilizadores.

1. Instale o python (actualmente é utilizado o python 3.7, entretanto, se pretender poderá usar uma versão mais recente.
2. Instale o Gettext, pode descarregar uma distribuição windows [neste link](https://mlocati.github.io/articles/gettext-iconv-windows.html) Se estiver a utilizar o Windows de 64 bits, recomendo [esta versão](https://github.com/mlocati/gettext-iconv-windows/releases/download/v0.21-v1.16/gettext0.21-iconv1.16-shared-64.exe)
3. Passo opcional (mas recomendado) crie um ambiente virtual python para gerir os extras do NVDA. Na consola, utilizar "python -m venv PAT_TO_FOLDER", onde PAT_TO_FOLDER é o caminho desejado para o ambiente virtual.
4. Se fez o passo 3, vá a PAT_TO_FOLDER e dentro da pasta de scripts, execute "activate". O nome do ambiente deve ser exibido no prompt da consola.
5. Clone este repositório para o caminho desejado: "git clone https://github.com/davidacm/NVDA-IBMTTS-Driver.git".
6. Na mesma instância da consola, vá para a pasta deste repositório.
7. Instale os requisitos: "pip install -r requirements.txt".
8. Execute o comando scons. O extra criado, se não houver erros, será posto na pasta raíz deste repositório.

Uma vez fechada a consola, o ambiente virtual é desactivado.

### Empacotamento das bibliotecas como um extra independente.
Não se recomenda incluir as bibliotecas com este controlador, porque se o utilizador actualizar a partir do [repositório oficial](https://github.com/davidacm/NVDA-IBMTTS-Driver), utilizando o instalador de extras do NVDA, a versão antiga será eliminada incluindo as bibliotecas.
Uma solução para isto é instalar as bibliotecas separadamente. [Siga este link](https://github.com/davidacm/ECILibrariesTemplate) para saber como empacotar as bibliotecas num extra separado.

### Notas:

* Se utilizar a funcionalidade de actualização interna (manual ou automática), as bibliotecas não serão removidas, mesmo que estejam dentro do extra.
* Se o sintetizador estiver dentro deste extra ou do ["eciLibraries"](https://github.com/davidacm/ECILibrariesTemplate), o controlador actualizará automaticamente os caminhos do ficheiro "eci.ini", de modo que poderá ser utilizado em versões portáteis do NVDA.
* Ao utilizar o botão "Copiar os ficheiros do IBMTTS para um extra", criará um novo extra no NVDA. Portanto, se pretender desinstalar o IBMTTS, deverá desinstalar dois extras: "Controlador do IBMTTS" e "eciLibraries".
* As ferramentas scons e gettext neste projecto suportam apenas o python 3. Não funcionam em python 2.7.
* Poderá adicionar os ficheiros extra requeridos do IBMTTS dentro do extra (para utilização pessoal somente). Simplesmente copie-os para dentro de "addon\synthDrivers\ibmtts". Ajuste o nome da biblioteca predefinida no ficheiro "settingsDB.py" se necessário.
* Se o caminho definido para a biblioteca não for relativo, o controlador não actualizará os caminhos no ficheiro "eci.ini". O controlador assume que, ao utilizar caminhos absolutos, os caminhos estão correctos no "eci.ini" e evitará realizar actualizações. Tenha isto em mente ao definir os caminhos das suas bibliotecas. Se não estiverem correctos neste ficheiro, poderá causar erros que deixarão o NVDA sem voz ao utilizar este sintetizador.

## Reportar problemas:

Caso encontre um problema de segurança com algumas das bibliotecas compatíveis com este controlador, não abra um problema do Github nem comente nos fóruns antes que se resolva o problema. Informe-nos através [deste formulário.](https://docs.google.com/forms/d/123gSqayOAsIQLx1NiI98fEqr46oiJRZ9nNq0_KIF9WU/edit)

Caso o problema não prejudique o controlador ou o leitor de ecrã, poderá então abrir um [problema do Github aqui.](https://github.com/davidacm/NVDA-IBMTTS-Driver/issues)

## Referências.
 Este controlador é baseado no SDK do IBM ViaVoice (IBMTTS). Poderá encontrar a documentação [neste link](http://web.archive.org/web/20191125091344/http://www.wizzardsoftware.com/docs/tts.pdf)

Também disponível no [website da Universidade de Columbia](http://www1.cs.columbia.edu/~hgs/research/projects/simvoice/simvoice/docs/tts.pdf)

ou poderá encontrar uma cópia [neste repositório](https://github.com/david-acm/NVDA-IBMTTS-Driver)

[pyibmtts: Projecto do IBM ViaVoice SDK em Python, desenvolvido por Peter Parente](https://sourceforge.net/projects/ibmtts-sdk/)

Veja os ficheiros de cópia de segurança aqui:

[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)

ou [tts.txt.](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)
