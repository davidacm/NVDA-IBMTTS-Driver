# Driver IBMTTS, add-on para NVDA #
  Este add-on implementa o suporte do NVDA para o sintetizador IBMTTS.
  Não podemos distribuir as bibliotecas IBMTTS. Este é apenas o controlador.
  Se você quiser contribuir para melhorar este driver, sinta-se à vontade para nos enviar seus pull requests via GitHub!

## Download.
A última versão está disponível para [download neste link](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

## O que é o sintetizador IBMTTS?

O ViaVoice TTS é um mecanismo de conversão de texto em fala desenvolvido pela IBM, que sintetiza a representação textual da linguagem humana em fala.

## Características:
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
* Sempre enviar as configurações de voz atuais: No momento, há um problema com o sintetizador, que ocasionalmente faz com que as configurações de velocidade e tom da voz retornem brevemente aos valores padrão. A causa desse problema é atualmente desconhecida, no entanto, uma solução é enviar continuamente as configurações atuais de velocidade e tom de voz. Geralmente, esta opção deve estar sempre habilitada. No entanto, você deve desativá-la durante a leitura de textos contendo tags de alteração de voz.
* Taxa de amostragem: altera a qualidade do som do sintetizador. Mais útil para o IBM ViaVoice, em que a definição da taxa de amostragem para 8 kHz permite o acesso a um novo conjunto de vozes.

## requisitos.
###NVDA.
  Requer o NVDA 2019.3 ou posterior.

### As bibliotecas do sintetizador IBMTTS.
  Este é apenas o driver, você deve procurar as bibliotecas em outro lugar.
  O driver oferece suporte às bibliotecas um pouco mais recentes que adicionam suporte aos idiomas do leste asiático e possui correções específicas para codificação de texto adequada. No entanto, bibliotecas mais antigas sem isso devem funcionar normalmente.
  A partir da versão 21.03A1, o driver também funciona com as bibliotecas ainda mais recentes do IBM ViaVoice, em vez de apenas com as do SpeechWorks. Um conjunto separado de correções está incluído para essas bibliotecas, levando em consideração idiomas adicionais e outras diferenças. As vozes concatenativas são agora suportadas e podem ser acessadas definindo a taxa de amostragem para 8 kHz após a instalação das vozes. Para obter melhores resultados, use a compilação de Junho de 2005 da ibmeci.dll versão 7.0.0.0, pois as versões mais antigas podem ser instáveis ao receber texto rapidamente, por exemplo, ao navegar rapidamente pelos itens em uma lista.

## Instalação.
  Você só precisa instalá-lo como qualquer outro complemento do NVDA. Em seguida, abra a caixa de diálogo de configurações do NVDA e, na categoria IBMTTS, defina o caminho dos arquivos IBMTTS.
  Nesta categoria você também pode copiar os arquivos externos do IBMTTS dentro do add-on.

## Contribuindo com a tradução.

Para facilitar para os tradutores, deixei um [modelo de tradução no branch principal](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot).
Se você deseja traduzir o complemento para outro idioma e não deseja criar uma conta GitHub e instalar o Python e outras ferramentas necessárias para a tradução, execute as seguintes etapas:

1. Use [este modelo](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/IBMTTS.pot), como base para o idioma de destino.
2. Faça o download do ["poedit"](https://poedit.net/), este software irá ajudá-lo a gerenciar as strings de tradução.
3. Se você quiser traduzir a documentação também, você pode usar a [Documentação em inglês neste link](https://raw.githubusercontent.com/davidacm/NVDA-IBMTTS-Driver/master/README.md)
4. Quando terminar a tradução, pode enviá-la para "dhf360@gmail.com".

Você não precisa compilar os arquivos de origem. Farei isso quando publicar uma nova versão do complemento. Mencionarei seu nome no respectivo Commit. Se você não quiser ser mencionado, avise-me ao enviar o e-mail.

Nota: certifique-se de ter usado o modelo mais recente das strings de tradução.

Este é um método alternativo. Se desejar, você sempre pode usar o modo usual. Fork este repositório, atualize a tradução do idioma de destino e envie um PR. No entanto, este modo só trará mais complexidade para você. 

## Empacotando o add-on para distribuição.
  Abra uma linha de comando, mude para o diretório raiz do add-on e execute o comando scons. O add-on criado, se não houver erros, será colocado na pasta raiz do add-on.

### Empacotando as bibliotecas como um complemento independente.
Não é recomendado incluir as bibliotecas com este driver, pois se o usuário atualizar do [repositório oficial](https://github.com/davidacm/NVDA-IBMTTS-Driver), a versão antiga será excluída incluindo as bibliotecas.
Uma solução para isso é instalar as bibliotecas separadamente. [Siga este link](https://github.com/davidacm/ECILibrariesTemplate) para saber como empacotar as bibliotecas em um complemento separado.

### Notas:

* se o sintetizador estiver dentro deste add-on ou do add-on ["eciLibraries"](https://github.com/davidacm/ECILibrariesTemplate), o driver atualizará os caminhos do arquivo ini automaticamente. Assim, você pode usá-lo em versões portáteis do NVDA.
* Usar o botão "Copiar os arquivos do IBMTTS para um add-on" criará um novo complemento no NVDA. Portanto, se você deseja desinstalar o IBMTTS, será necessário desinstalar dois complementos: "Driver IBMTTS" e "eciLibraries".
* As ferramentas scons e gettext neste projeto suportam apenas python 3. Elas não funcionam em python 2.7.
* Você pode incluir os arquivos extras do IBMTTS necessários no add-on (somente para uso pessoal). Basta copiá-los para "addon\synthDrivers\ibmtts". Defina o nome da biblioteca padrão em "settingsDB.py" se necessário.

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