# Driver IBMTTS, add-on para NVDA #

  Este add-on implementa o suporte do NVDA para o sintetizador IBMTTS.
  Não podemos distribuir as bibliotecas IBMTTS. Este é apenas o controlador.
  Se você quiser contribuir para melhorar este driver, sinta-se à vontade para nos enviar seus pull requests via GitHub!

Embora este driver seja compatível com as bibliotecas do Eloquence (já que o Eloquence tem a mesma api que o IBMTTS), não é recomendável usar o Eloquence com este driver devido a problemas de licenciamento. Antes de usar qualquer biblioteca de síntese com este driver, recomenda-se obter os direitos de uso da licença primeiro.

Este driver foi desenvolvido com a documentação disponível para o IBMTTS, disponível publicamente na web. Consulte a seção de referências para obter mais detalhes.

## Download.
A última versão está disponível para [download neste link](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

## O que é o sintetizador IBMTTS?

O ViaVoice TTS é um mecanismo de conversão de texto em fala desenvolvido pela IBM, que sintetiza a representação textual da linguagem humana em fala.

## Recursos e configurações.

* Suporte para configurações de voz, variante, velocidade, tom, inflexão e volume.
* Suporta parâmetros extras, como tamanho da cabeça, rouquidão, respiração. Crie sua própria voz!
* Ative ou desative as tags de mudanças de voz. Desative para se proteger contra códigos maliciosos de brincalhões, ative para permitir fazer muitas coisas divertidas com o sintetizador. Requer um ajuste adicional no NVDA para que funcione corretamente.
* Aumento especial de velocidade. Se o sintetizador não estiver falando rápido o suficiente, ative o aumento de velocidade e obtenha a velocidade máxima!
* Mudança automática de idioma. Permite que o sintetizador leia o texto no idioma correto quando marcado.
* Filtragem estendida. O driver inclui um extenso conjunto de filtros para lidar com falhas e outros comportamentos estranhos do sintetizador.
* Suporte de dicionário. O driver suporta a integração de palavras especiais, dicionários de raiz e dicionários de abreviaturas do usuário para cada idioma. Conjuntos de dicionários prontos podem ser obtidos [no repositório de dicionários da comunidade](https://github.com/thunderdrop/IBMTTSDictionaries) ou [no repositório alternativo de mohamed00 (com dicionários de sintetizador IBM)](https:/ /github.com /mohamed00/AltIBMTTSDictionaries)

### Configurações adicionais:

* Expandir Abreviaturas: Ativa a expansão de abreviaturas. Observe que desabilitar esta opção também desabilitará a expansão de quaisquer abreviações especificadas nos dicionários de abreviaturas fornecidos pelo usuário.
* Habilitar previsão de frases: Se esta opção estiver habilitada, o sintetizador tentará prever onde as pausas nas frases ocorrerão com base em sua própria estrutura, por exemplo, usando palavras como "e" e "o" como limites de frase. Se estiver desligada, ele só fará uma pausa quando encontrar uma vírgula ou outros sinais de pontuação.
* Reduzir pausas: marque esta opção para obter pausas de pontuação mais curtas, como as vistas em outros leitores de tela.
* Sempre enviar as configurações de voz atuais: há um bug no sintetizador que ocasionalmente fará com que as configurações de velocidade e tom de voz sejam brevemente redefinidas para seus valores padrão. A causa desse problema é atualmente desconhecida, no entanto, uma solução alternativa é enviar continuamente as configurações atuais de velocidade e tom. Esta opção geralmente deve ser habilitada. No entanto, deve desabilitá-la se estiver lendo texto que contenha tags de mudança de voz.
* Taxa de amostragem: altera a qualidade do som do sintetizador. Mais útil para o IBM ViaVoice, em que a definição da taxa de amostragem para 8 kHz permite o acesso a um novo conjunto de vozes.

### Categoria de configurações do IBMTTS.

Este complemento possui sua própria categoria de configurações nas opções do NVDA, para gerenciar algumas funcionalidades internas não relacionadas à síntese de fala.

* Procurar atualizações do IBMTTS automaticamente: Se esta opção estiver marcada, o complemento verificará diariamente se há novas versões disponíveis.
* Botão Procurar atualização: verifique manualmente se há novas atualizações do complemento.
* Endereço da pasta do IBMTTS: O caminho para carregar as bibliotecas do IBMTTS. Pode ser absoluto ou relativo.
* Nome da biblioteca do IBMTTS (dll): O nome da biblioteca (dll). Não inclua caminhos, apenas o nome com a extensão, geralmente ".dll".
* Procurar a biblioteca do IBMTTS... Abre uma caixa de diálogo de navegação de arquivo para procurar a biblioteca do IBMTTS no sistema. Será salvo como um caminho absoluto.
* Copiar os arquivos do IBMTTS para um add-on. (pode não funcionar para algumas distribuições do IBMTTS): Se o caminho da biblioteca do IBMTTS tiver sido definido, ele copiará todos os arquivos da pasta para um novo complemento chamado eciLibraries e atualizará o caminho atual para um caminho relativo. É muito útil nas versões portáteis do NVDA. Funciona apenas para as bibliotecas que usam o arquivo "eci.ini" para as informações dos idiomas de voz. Se a biblioteca usar o registro do Windows, essa opção não funcionará.

Observação: a funcionalidade de atualização automática ou manual não removerá os arquivos internos do complemento. Se você usar suas bibliotecas nesse local, poderá usar essa função com segurança. Suas bibliotecas estarão seguras.

## requisitos.
###NVDA.
  Requer o NVDA 2019.3 ou posterior.

### As bibliotecas do sintetizador IBMTTS.
  Este é apenas o driver, você deve procurar as bibliotecas em outro lugar.
  O driver oferece suporte às bibliotecas um pouco mais recentes que adicionam suporte aos idiomas do leste asiático e possui correções específicas para codificação de texto adequada. No entanto, bibliotecas mais antigas sem isso devem funcionar normalmente.
  A partir da versão 21.03A1, o driver também funciona com as bibliotecas ainda mais recentes do IBM ViaVoice, em vez de apenas com as do SpeechWorks. Um conjunto separado de correções está incluído para essas bibliotecas, levando em consideração idiomas adicionais e outras diferenças. As vozes concatenativas são agora suportadas e podem ser acessadas definindo a taxa de amostragem para 8 kHz após a instalação das vozes. Para obter melhores resultados, use a compilação de Junho de 2005 da ibmeci.dll versão 7.0.0.0, pois as versões mais antigas podem ser instáveis ao receber texto rapidamente, por exemplo, ao navegar rapidamente pelos itens em uma lista. observe também que, se você estiver usando as bibliotecas do IBM ViaVoice em cantonês de Hong Kong ou chinês, convém desativar a opção "Usar soletragem melhorada quando suportado", para evitar que alguns caracteres nesses idiomas sejam soletrados usando o pinyin para o qual são convertidos internamente.

## Instalação.
  Você só precisa instalá-lo como qualquer outro complemento do NVDA. Em seguida, abra a caixa de diálogo de configurações do NVDA e, na categoria IBMTTS, defina o caminho dos arquivos IBMTTS.
  Nesta categoria você também pode copiar os arquivos externos do IBMTTS dentro do add-on.

## Contribuindo com a tradução.

Para facilitar para os tradutores, deixei um [modelo de tradução no branch principal](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot).
Para a documentação, criei um arquivo chamado ["docChangelog-for-translators.md".](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/docChangelog-for-translators.md)
Você pode usar esse arquivo para ver o que foi alterado na documentação e atualizar a documentação para o seu idioma.
Se você deseja traduzir o complemento para outro idioma e não deseja criar uma conta GitHub e instalar o Python e outras ferramentas necessárias para a tradução, execute as seguintes etapas:

1. Use [este modelo](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot), como base para o idioma de destino.
2. Faça o download do ["poedit"](https://poedit.net/), este software irá ajudá-lo a gerenciar as strings de tradução.
3. Se você quiser traduzir a documentação também, pode ver as novas alterações da documentação
[neste link.](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/docChangelog-for-translators.md) Veja a [documentação completa em inglês aqui.](https:/ /raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/readme.md)
4. Quando terminar a tradução, pode enviá-la para "dhf360@gmail.com".

Você não precisa compilar os arquivos de origem. Farei isso quando publicar uma nova versão do complemento. Mencionarei seu nome no respectivo Commit. Se você não quiser ser mencionado, avise-me ao enviar o e-mail.

Nota: certifique-se de ter usado o modelo mais recente das strings de tradução.

Este é um método alternativo. Se desejar, você sempre pode usar o modo usual. Fork este repositório, atualize a tradução do idioma de destino e envie um PR. No entanto, este modo só trará mais complexidade para você. 

## Empacotando o add-on para distribuição.

Nota de tradução: Estas instruções são apenas para desenvolvedores de complementos e não fazem sentido para o usuário comum.

1. Instale o python, atualmente o python 3.7 é usado, mas você pode usar uma versão mais recente.
2. Instale o gettext, você pode baixar uma distribuição para windows [neste link.](https://mlocati.github.io/articles/gettext-iconv-windows.html) Se estiver usando windows 64 bits, recomendo [esta versão.](https://github.com/mlocati/gettext-iconv-windows/releases/download/v0.21-v1.16/gettext0.21-iconv1.16-shared-64.exe)
3. (etapa opcional, mas recomendada) crie um ambiente virtual python para ser usado para gerenciar complementos do NVDA. No console, use "python -m venv PAT_TO_FOLDER". Onde PAT_TO_FOLDER é o caminho desejado para o seu ambiente virtual.
4. Se você fez o passo 2, vá até a pasta PAT_TO_FOLDER e dentro da pasta scripts, execute "activate". O nome do ambiente deve ser mostrado no prompt do console.
5. Clone este repositório no caminho desejado: "git clone https://github.com/davidacm/NVDA-IBMTTS-Driver.git".
6. Na mesma instância do console, vá para a pasta deste repositório.
7. Instale os requisitos: "pip install -r requirements.txt".
8. Execute o comando scons. O complemento criado, se não houver erros, é colocado no diretório raiz deste repositório.

Depois de fechar o console, o ambiente virtual é desativado.

### Empacotando as bibliotecas como um complemento independente.
Não é recomendado incluir as bibliotecas com este driver, pois se o usuário atualizar a partir do [repositório oficial](https://github.com/davidacm/NVDA-IBMTTS-Driver), usando o instalador de complementos do NVDA, a versão antiga será excluída incluindo as bibliotecas.
Uma solução para isso é instalar as bibliotecas separadamente. [Siga este link](https://github.com/davidacm/ECILibrariesTemplate) para saber como empacotar as bibliotecas em um complemento separado.

### Notas:

* Se você usar o recurso interno de atualizações manuais ou automáticas, as bibliotecas não serão excluídas, mesmo que estejam dentro do complemento.
* se o sintetizador estiver dentro deste add-on ou do add-on ["eciLibraries"](https://github.com/davidacm/ECILibrariesTemplate), o driver atualizará os caminhos do arquivo ini automaticamente. Assim, você pode usá-lo em versões portáteis do NVDA.
* Usar o botão "Copiar os arquivos do IBMTTS para um add-on" criará um novo complemento no NVDA. Portanto, se você deseja desinstalar o IBMTTS, será necessário desinstalar dois complementos: "Driver IBMTTS" e "eciLibraries".
* As ferramentas scons e gettext neste projeto suportam apenas python 3. Elas não funcionam em python 2.7.
* Você pode incluir os arquivos extras do IBMTTS necessários no add-on (somente para uso pessoal). Basta copiá-los para "addon\synthDrivers\ibmtts". Defina o nome da biblioteca padrão em "settingsDB.py" se necessário.
* Se o caminho configurado para a biblioteca não for relativo, este driver não atualizará os caminhos do arquivo "eci.ini". O driver assume que, ao usar caminhos absolutos, os caminhos estão corretos no "eci.ini" e evitará fazer atualizações. Tenha isso em mente ao definir o caminho de suas bibliotecas. Se não estiverem corretos no arquivo "eci.ini", poderá causar erros que deixarão o NVDA mudo quando você usar este sintetizador.

## Reportar problemas:

Se você encontrar um problema de segurança com algumas das bibliotecas compatíveis com este driver, não abra um problema do github nem o comente em fóruns antes que o problema seja resolvido. Por favor, comunique a questão [neste formulário.](https://docs.google.com/forms/d/123gSqayOAsIQLx1NiI98fEqr46oiJRZ9nNq0_KIF9WU/edit)

Se o problema não travar o driver ou o leitor de tela, abra um [problema do github aqui.](https://github.com/davidacm/NVDA-IBMTTS-Driver/issues)

##Referências.
 Este driver é baseado no IBM ViaVoice SDK (IBMTTS). Você pode encontrar a documentação [neste link](http://web.archive.org/web/20191125091344/http://www.wizzardsoftware.com/docs/tts.pdf)

Também disponível no [site da Universidade de Columbia](http://www1.cs.columbia.edu/~hgs/research/projects/simvoice/simvoice/docs/tts.pdf)

há uma cópia  [neste repositório](https://github.com/david-acm/NVDA-IBMTTS-Driver)

[pyibmtts: projeto do IBM ViaVoice SDK em Python, desenvolvido por Peter Parente](https://sourceforge.net/projects/ibmtts-sdk/)

Consulte os seguintes arquivos:

[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)
ou [tts.txt.](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)