# Controlador do IBMTTS, extra para o NVDA #

  Este extra implementa a compatibilidade do NVDA com o sintetizador IBMTTS.
  Não podemos distribuir as bibliotecas do IBMTTS. Este é apenas o controlador.
  Se pretender contribuir para melhorar este controlador, sinta-se livre para enviar-nos as suas pull requests através do GitHub!

Embora este controlador seja compatível com as bibliotecas do ETI Eloquence (uma vez que este tem a mesma API que o IBMTTS), não se recomenda a utilização do Eloquence com este controlador devido a questões de licenciamento. Antes de utilizar quaisquer bibliotecas de síntese com este controlador, recomenda-se que obtenha primeiro os direitos de utilização da licença.

Este controlador foi desenvolvido com a documentação disponível para o IBMTTS, disponível publicamente na web. Consulte a secção de referências para mais detalhes.

## Descarregar.
A última versão está disponível para [transferência neste link](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

## O que é o sintetizador IBMTTS?

O ViaVoice TTS é um motor de conversão de texto em fala desenvolvido pela IBM, que sintetiza a representação textual da linguagem humana em fala.

## Características e configurações:

* Suporte para as configurações de voz, variante, velocidade, entoação, inflexão e volume.
* Suporte de parâmetros extras, tais como tamanho da cabeça, rouquidão, respiração. Crie a sua própria voz!
* Ativar ou desativar as etiquetas de alterações de voz. Desative-o para se proteger de códigos maliciosos de brincalhões, ative-o para fazer muitas coisas divertidas com o sintetizador. Requer um ajuste adicional no NVDA para que funcione corretamente.
* Aumento de Velocidade. Caso o sintetizador não fale suficientemente rápido, ative o aumento de velocidade para obter a velocidade máxima!
* Alteração automática do idioma. Permite que o sintetizador leia o texto no idioma correto quando marcado.
* Filtragem alargada. O controlador inclui um extenso conjunto de filtros para lidar com crashes e outros comportamentos estranhos do sintetizador.
* Suporte a dicionários. O controlador suporta a integração de palavras especiais, dicionários raízes e dicionários de abreviação do utilizador para cada idioma. Conjuntos de dicionários prontos podem ser obtidos [a partir do repositório de dicionários da comunidade](https://github.com/thunderdrop/IBMTTSDictionaries) ou [desde o repositório alternativo de mohamed00 (com dicionários do sintetizador IBM)](https://github.com/mohamed00/AltIBMTTSDictionaries)

### Configurações adicionais:

* Ativar a expansão de abreviaturas: alterna a expansão de abreviaturas. Note que a desativação desta opção também desativará a expansão de quaisquer abreviaturas especificadas nos dicionários de abreviaturas fornecidos pelo utilizador.
* Ativar a previsão de frases: se esta opção estiver ativada, o sintetizador tentará prever onde se produzirão as pausas nas frases com base na sua própria estrutura, por exemplo, utilizando palavras como "e" ou "o" como limites de frases. Se esta opção estiver desativada, só fará uma pausa se encontrar vírgulas ou outro tipo de pontuação.
* Pausas: Esta é uma caixa combinada com três opções.
    * Não encurtar: as pausas não serão de todo encurtadas, e as pausas originais do IBMTTS serão utilizadas em todos os casos.
    * Encurtar apenas no fim do texto: as pausas dos símbolos de pontuação, como pontos e vírgulas, não serão encurtadas, mas serão encurtadas quando o texto terminar, por exemplo, quando premir NVDA+t duas vezes rapidamente para soletrar a barra de título de uma aplicação carácter a carácter.
    * Encurtar todas as pausas: todas as pausas, incluindo as pausas de pontuação e as pausas que ocorrem no final do texto, serão encurtadas.
* Sempre enviar as definições de voz atuais: há um erro no sintetizador que ocasionalmente fará com que as definições de velocidade e entoação sejam brevemente repostas aos seus valores por defeito. A causa desta questão é atualmente desconhecida, no entanto, uma solução alternativa consiste em enviar continuamente as definições atuais de velocidade e entoação. É suposto que esta opção fique geralmente ativada. No entanto, deve ser desativada durante a leitura de textos contendo etiquetas de alteração de voz.
* Frequência de amostragem: Alterar a qualidade sonora do sintetizador. Isto é mais útil para o IBM ViaVoice, onde a definição da frequência de amostragem para 8 kHz permite o acesso a um novo conjunto de vozes.

### Categoria de configurações do IBMTTS.

Este extra possui a sua própria categoria de opções dentro das configurações do NVDA, para gerir algumas funcionalidades internas não relacionadas com a síntese de voz.

* Verificar automaticamente se há atualizações para o IBMTTS: se esta opção estiver marcada, o extra irá verificar diariamente a existência de novas versões.
* Verificar atualização: Verifica manualmente se existem novas atualizações deste extra.
* Localização da Pasta do IBMTTS: o caminho para carregar as bibliotecas do IBMTTS. Pode ser absoluto ou relativo.
* Nome da biblioteca do IBMTTS: o nome da biblioteca (dll). Não deve incluir caminhos, apenas o nome com a extensão, normalmente ".dll".
* Localizar a Biblioteca do IBMTTS... Abre um diálogo de navegação de ficheiros para procurar a biblioteca do IBMTTS no sistema. Será guardado como um caminho absoluto.
* Copiar os ficheiros do IBMTTS para um extra (pode não funcionar para algumas distribuições do IBMTTS): se o caminho da biblioteca do IBMTTS tiver sido definido, esta opção irá copiar todos os ficheiros da pasta para um novo extra chamado "eciLibraries" e atualizar o caminho atual para um caminho relativo. É útil em versões portáteis do NVDA. Isto funciona apenas para as bibliotecas que utilizem o ficheiro "eci.ini" para as informações dos idiomas e vozes. Se a biblioteca utilizar o registo do Windows, esta opção não funcionará.

Nota: A funcionalidade de atualização automática ou manual não removerá os ficheiros internos do extra. Se mantiver as suas bibliotecas neste local, pode utilizar esta funcionalidade com segurança. As suas bibliotecas estarão seguras.

## requisitos.
### NVDA.
  Necessita do NVDA 2019.3 ou posterior.

### As bibliotecas do sintetizador IBMTTS.
  Este é apenas o controlador; é necessário obter as bibliotecas de outro local.  
  Este controlador suporta as bibliotecas ligeiramente mais recentes que adicionam suporte a idiomas do Leste Asiático e tem correções específicas para a codificação correta do texto. No entanto, é suposto que as bibliotecas mais antigas que não têm esta característica também funcionem.
  A partir da versão 21.03A1, este controlador também funciona com as bibliotecas ainda mais recentes da IBM, em vez de apenas com as do SpeechWorks. É incluído um conjunto de correções independentes para essas bibliotecas e são tidos em conta os idiomas adicionais e outras diferenças. As vozes concatenativas são suportadas e podem ser acedidas definindo a frequência de amostragem para 8 kHz depois de instalar as vozes. Para obter melhores resultados, utilize a versão de junho de 2005 do ibmeci.dll (versão 7.0.0.0), uma vez que as versões mais antigas podem ser instáveis quando se recebe texto rapidamente, por exemplo, ao percorrer rapidamente os itens de uma lista. Tenha também em atenção que, se estiver a utilizar as bibliotecas do IBM ViaVoice em cantonês de Hong Kong ou chinês, poderá querer desativar a opção "Utilizar funcionalidade de soletrar se suportada", para evitar que alguns caracteres nestes idiomas sejam soletrados utilizando o pinyin para o qual são internamente convertidos.

## Instalação.
  Basta instalá-lo como quaisquer outros extras do NVDA. Em seguida, abra o diálogo de configurações do NVDA e, na categoria "IBMTTS", defina a localização dos ficheiros do IBMTTS.
  Também nesta categoria pode copiar os ficheiros externos do IBMTTS para um extra para os utilizar localmente.

## Contribuir com a tradução.

Para facilitar o seu trabalho, deixei um [modelo de tradução no ramo principal.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot)
Para a documentação, criei um ficheiro chamado ["docChangelog-for-translators.md".](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/docChangelog-for-translators.md)
Pode utilizar esse ficheiro para ver o que foi alterado na documentação e atualizar a documentação para o seu idioma.
Se pretender traduzir o extra para outro idioma e não quiser criar uma conta no GitHub e instalar o Python e outras ferramentas necessárias para a tradução, execute os seguintes paços:

1. Utilize [este modelo](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot), como base para o idioma de destino.
2. Transfira o ["poedit"](https://poedit.net/), este software o ajudará a gerir as cadeias de tradução.
3. Se também quiser traduzir a documentação, pode ver as novas alterações da documentação
[neste link.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/docChangelog-for-translators.md) Pode ver a [documentação completa em inglês aqui.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/readme.md)
4. Quando tiver terminado a tradução, pode enviar-ma para: "dhf360@gmail.com".

Não é necessário compilar os ficheiros de origem. Fá-lo-ei quando lançar uma nova versão do extra. Mencionarei o seu nome no respetivo commit. Se não quiser ser mencionado, avise-me quando enviar o e-mail.

Nota: certifique-se de que utilizou o modelo mais recente das cadeias de tradução.

Este é um método alternativo. Se quiser, pode sempre seguir o caminho habitual. Faça um fork deste repositório, atualize a tradução para o seu idioma e envie-me um PR. Mas esta forma apenas lhe trará mais complexidade.

## Empacotamento do extra para distribuição.

Nota de tradução: Estas instruções destinam-se aos criadores de extras e não têm qualquer significado para a maioria dos utilizadores.

1. Instale o python (atualmente é utilizado o python 3.7, mas pode utilizar uma versão mais recente).
2. Instale o Gettext (pode descarregar uma distribuição para o Windows [neste link)](https://mlocati.github.io/articles/gettext-iconv-windows.html) Se estiver a utilizar o Windows de 64 bits, recomendo [esta versão](https://github.com/mlocati/gettext-iconv-windows/releases/download/v0.21-v1.16/gettext0.21-iconv1.16-shared-64.exe)
3. Passo opcional (mas recomendado) crie um ambiente virtual python para ser utilizado para gerir os extras do NVDA. Na consola, utilize "python -m venv PAT_TO_FOLDER". Em que PAT_TO_FOLDER é o caminho pretendido para o ambiente virtual.
4. Se tiver efetuado o passo 3, vá para PAT_TO_FOLDER e, dentro da pasta dos scripts, execute "activate". O nome do ambiente deve ser mostrado no prompt da consola.
5. Clone este repositório no caminho desejado: "git clone https://github.com/davidacm/NVDA-IBMTTS-Driver.git".
6. Na mesma instância da consola, vá para a pasta deste repositório.
7. Instale os requisitos: "pip install -r requirements.txt".
8. Execute o comando scons. O extra criado, se não houver erros, será posto na pasta raíz deste repositório.

Depois de fechar a consola, o ambiente virtual é desativado.

### Empacotamento das bibliotecas como um extra independente.
Não é recomendado incluir as bibliotecas com este controlador. Isto porque se o utilizador atualizar o controlador a partir do [repositório oficial](https://github.com/davidacm/NVDA-IBMTTS-Driver), utilizando o instalador de extras do NVDA, a versão antiga será eliminada, incluindo as bibliotecas.
Uma solução para isso é instalar as bibliotecas separadamente. [Siga este link](https://github.com/davidacm/ECILibrariesTemplate) para saber como empacotar as bibliotecas num extra separado.

### Notas:

* Se utilizar a funcionalidade de atualização interna (manual ou automática), as bibliotecas não serão eliminadas, mesmo que estejam dentro do extra.
* Se o sintetizador estiver dentro deste extra ou do ["eciLibraries"](https://github.com/davidacm/ECILibrariesTemplate), o controlador atualizará automaticamente os caminhos do ficheiro "eci.ini". Assim, pode utilizá-lo em versões portáteis do NVDA.
* Ao utilizar o botão "Copiar os ficheiros do IBMTTS para um extra", criará um novo extra no NVDA. Portanto, se pretender desinstalar o IBMTTS, deverá desinstalar dois extras: "Controlador do IBMTTS" e "eciLibraries".
* As ferramentas scons e gettext deste projeto são compatíveis apenas com o python 3. Não funcionam com o python 2.7.
* Pode colocar os ficheiros adicionais do IBMTTS necessários dentro do extra (apenas para uso pessoal). Basta copiá-los para a pasta "addon\synthDrivers\ibmtts". Ajuste o nome da biblioteca predefinida em "settingsDB.py" se necessário.
* se o caminho da biblioteca configurada não for relativo, o extra não atualizará os caminhos no ficheiro "eci.ini". O controlador assume que, ao utilizar caminhos absolutos, os caminhos estão corretos em "eci.ini" e evitará fazer quaisquer atualizações. Tenha isto em mente ao definir o caminho das suas bibliotecas. Se não estiverem corretos, poderão ocorrer erros que deixarão o NVDA sem fala quando utilizar este sintetizador.

## Reportar problemas:

Se encontrar um problema de segurança com algumas das bibliotecas compatíveis com este controlador, não abra um problema no github nem o comente nos fóruns antes de o problema estar resolvido. Por favor, comunique o problema [neste formulário.](https://docs.google.com/forms/d/123gSqayOAsIQLx1NiI98fEqr46oiJRZ9nNq0_KIF9WU/edit)

Se o problema não bloquear o controlador ou o leitor de ecrã, poderá então abrir um [problema do Github aqui.](https://github.com/davidacm/NVDA-IBMTTS-Driver/issues)

## Referências.
 Este controlador é baseado no SDK do IBM ViaVoice (IBMTTS). A documentação está disponível [neste link](http://web.archive.org/web/20191125091344/http://www.wizzardsoftware.com/docs/tts.pdf)

Também disponível no [website da Universidade de Columbia](http://www1.cs.columbia.edu/~hgs/research/projects/simvoice/simvoice/docs/tts.pdf)

ou pode encontrar uma cópia [neste repositório](https://github.com/david-acm/NVDA-IBMTTS-Driver)

[pyibmtts: Projeto do IBM ViaVoice SDK em Python, desenvolvido por Peter Parente](https://sourceforge.net/projects/ibmtts-sdk/)

Veja aqui uma cópia dos ficheiros:

[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)

ou [tts.txt.](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)
