# Driver IBMTTS, add-on para NVDA #
  Este add-on implementa o suporte do NVDA para o sintetizador IBMTTS.
  Não podemos distribuir as bibliotecas IBMTTS. Este é apenas o controlador.
  Se você quiser contribuir para melhorar este driver, sinta-se à vontade para nos enviar seus pull requests via GitHub!

# Download.
A última versão está disponível para [download neste link](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

# Características:
* Suporte para configurações de voz, variante, velocidade, tom, inflexão e volume.
* Suporta parâmetros extras, como tamanho da cabeça, rouquidão, respiração. Crie sua própria voz!
* Ative ou desative as tags de mudanças de voz. Desative para se proteger contra códigos maliciosos de brincalhões, ative para permitir fazer muitas coisas divertidas com o sintetizador. Requer ajustes adicionais com o NVDA para que funcione corretamente.
* Aumento especial de velocidade. Se o sintetizador não estiver falando rápido o suficiente, ative o aumento de velocidade e obtenha a velocidade máxima!
* Mudança automática de idioma. Permita que o sintetizador leia o texto no idioma correto quando marcado.
* Filtragem estendida. O driver inclui um extenso conjunto de filtros para lidar com falhas e outros comportamentos estranhos do sintetizador.
* Suporte de dicionário. O driver suporta a integração de palavras especiais, dicionários de raiz e dicionários de abreviaturas do usuário para cada idioma. Conjuntos de dicionários prontos podem ser obtidos [no repositório de dicionários da comunidade](https://github.com/thunderdrop/IBMTTSDictionaries) ou [no repositório alternativo de mohamed00 (com dicionários de sintetizador IBM)](https:/ /github.com /mohamed00/AltIBMTTSDictionaries)

# requisitos.
##NVDA.
  Requer o NVDA 2019.3 ou posterior.

## As bibliotecas do sintetizador IBMTTS.
  Este é apenas o driver, você deve procurar as bibliotecas em outro lugar.
  O driver oferece suporte às bibliotecas um pouco mais recentes que adicionam suporte aos idiomas do leste asiático e possui correções específicas para codificação de texto adequada. No entanto, bibliotecas mais antigas sem isso devem funcionar.
  A partir da versão 21.03A1, o driver também funciona com bibliotecas IBM ainda mais recentes, em vez de apenas SpeechWorks. Um conjunto separado de correções está incluído para essas bibliotecas, levando em consideração idiomas adicionais e outras diferenças. Atualmente, apenas vozes formantes são suportadas. Obrigado a @mohamed00 por este trabalho.  Observe que ao usar as bibliotecas IBM, você deve desativar a opção Sempre enviar configurações de voz atuais.

# Instalação.
  Você só precisa instalá-lo como qualquer outro complemento do NVDA. Em seguida, abra a caixa de diálogo de configurações do NVDA e, na categoria IBMTTS, defina o caminho dos arquivos IBMTTS.
  Nesta categoria você também pode copiar os arquivos externos do IBMTTS dentro do add-on.
  
# Empacotando o add-on para distribuição.
  Abra uma linha de comando, mude para o diretório raiz do add-on e execute o comando scons. O add-on criado, se não houver erros, será colocado na pasta raiz do add-on.

## Notas:

* se o sintetizador estiver dentro deste add-on ou do add-on "eciLibraries", o driver atualizará os caminhos do arquivo ini automaticamente. Assim, você pode usá-lo em versões portáteis do NVDA.
* Usar o botão "Copiar os arquivos do IBMTTS para um add-on" criará um novo complemento no NVDA. Portanto, se você deseja desinstalar o IBMTTS, será necessário desinstalar dois complementos: "Driver IBMTTS" e "eciLibraries".
* As ferramentas scons e gettext neste projeto suportam apenas python 3. Elas não funcionam em python 2.7.
* Você pode incluir os arquivos extras do IBMTTS necessários no add-on (somente para uso pessoal). Basta copiá-los para "addon\synthDrivers\ibmtts". Defina o nome da biblioteca padrão em "settingsDB.py" se necessário.

#Referências.
 Este driver é baseado no IBM ViaVoice SDK (IBMTTS). Você pode encontrar a documentação [neste link](http://web.archive.org/web/20191125091344/http://www.wizzardsoftware.com/docs/tts.pdf)

ou você pode encontrar uma cópia [neste repositório](https://github.com/david-acm/NVDA-IBMTTS-Driver)

Consulte os seguintes arquivos:

[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)
ou [tts.txt.](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)