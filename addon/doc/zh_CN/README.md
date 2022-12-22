# NVDA插件， IBMTTS 驱动程序

此插件实现了 NVDA 与 IBMTTS 合成器的兼容。

因为我们无法发布 IBMTTS 库，这只是一个驱动程序。

如果您想改进此驱动程序，请随时提交 Pull request 。

尽管此驱动兼容 Eloquence （因为 Eloquence 与 IBMTTS 具有相同的 API），但由于许可问题，不建议将 Eloquence 与此驱动一起使用。在使用此驱动的任何语音库之前，建议先获得许可使用权。

该驱动是使用互联网上公开的 IBMTTS 文档开发的，有关更多详细信息，请参阅参考资料部分。
## 下载
最新版本可在[此链接下载](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

## 什么是 IBMTTS 合成器？

ViaVoice TTS 是 IBM 开发的文本转语音引擎，它可以将人类的语言文本合成为语音。

## 特性:

* 支持语音，变声，速度，声调和音量设置。
* 另外还支持头部尺寸，粗糙度，呼吸参数设置。你可以创建属于你自己的声音！
* 能够启用或禁用反引号语音标签。禁用该选项可以保护自己免受那些恶意语音代码的干扰，启用该选项，可以使 NVDA 合成器做一些有趣的事情。
* 语速加倍。如果您认为合成器的语速不够快，那么启用该选项可以大幅提高语音速度。
* 过滤。该驱动程序包括一套完整的过滤器，用于修复合成器的崩溃和其他奇怪行为。
* 自动语言切换。让合成器以正确的语言朗读相应语种的文本。
* 词典支持。此驱动程序支持集成各种语言的特殊词、词根和缩写用户词典。现成的词典可以从[社区词典存储库](https://github.com/thunderdrop/IBMTTSDictionaries) 或 [mohamed00 的替代存储库（包含 IBM 合成器词典）](https://github.com/mohamed00/AltIBMTTSDictionaries)中获取。

### 额外设置：

* 启用缩写扩展：开关缩写扩展。请注意，禁用此选项也会禁用用户提供的缩写词典中指定的任何缩写的扩展。
* 缩短停顿时间：启用此选项可缩短标点符号之间的停顿时间，就像在其他屏幕阅读器中看到的那样。
* 启用短语预测：如果启用此选项，合成器将尝试根据句子结构预测句子中的停顿位置，例如，使用“and”或“the”等词作为短语边界。如果关闭此选项，则只会在遇到逗号或其他同类标点符号时暂停。
* 始终发送当前语音设置：该合成器中有一个错误，偶尔会导致语音和音调设置短暂地被重置为默认值。此问题的原因目前未知，但解决方法是持续发送当前语速和音调设置。通常应启用此选项。但是，如果阅读包含反引号语音标签的文本，则应禁用该选项。
* 采样率：改变合成器的音质。对 IBMTTS 最有用，将采样率设置为 8 kHz 可以使用一组新语音。

## 要求

### NVDA
  您需要NVDA 2019.3 或更高版本。

## IBMTTS 语音库

这只是驱动程序，您必须从其他地方获取语音库。

此驱动程序支持添加了东亚语言并针对文本编码进行了特定修复的较新的库。不过，旧的库应该也可以兼容。

从 21.03A1 版起，该驱动还支持新版的 IBM 二进制文件，而不仅仅是 SpeechWorks 二进制文件。另外还有针对该驱动程序的一组独立修复程序，考虑了其他语言和差异。支持额外的混合语音，安装语音后可以通过将采样率设置为 8 kHz 来使用。为获得最佳效果，请使用 ibmeci.dll 版本 7.0.0.0 的 2005 年 6 月版本，因为旧版本在快速接收文本时可能不稳定，例如，快速浏览列表项目。

## 安装
只需将其安装为NVDA插件即可。然后打开NVDA设置面板，并在IBMTTS类别中设置IBMTTS目录。
此外，您还可以将外部IBMTTS文件复制到插件中。

## 翻译贡献

*略*

## 打包
1.安装python，目前使用的是python 3.7，但是你可以使用更新的版本。
2. 安装 gettext，你可以在[这个链接](https://mlocati.github.io/articles/gettext-iconv-windows.html) 下载一个 windows 发行版。如果你使用 windows 64 位，我推荐[此版本](https://github.com/mlocati/gettext-iconv-windows/releases/download/v0.21-v1.16/gettext0.21-iconv1.16-shared-64.exe)。
3. （可选但推荐的步骤）创建一个用于管理 NVDA 附加组件的 python 虚拟环境。在控制台中，使用“python -m venv PAT TO FOLDER”。 PAT TO FOLDER 是虚拟环境所需路径的路径。
4. 如果您执行了第 3 步，请转到 PAT TO FOLDER 和内部脚本文件夹，执行“activate”。环境名称应显示在控制台提示中。
5. 在您想要的路径中克隆此存储库：“git clone https://github.com/davidacm/NVDA-IBMTTS-Driver.git”。
6. 在同一个控制台实例中，转到此 repo 的文件夹。
7. 安装所需： “pip install -r requirements.txt”。
8. 运行 scons 命令。如果没有错误，编译的插件将放置在此 repo 的根目录中。

关闭控制台后，虚拟环境会被停用。

### 将语音库打包为独立的插件

我们不建议将语音库包含在此驱动中。这是因为如果用户从[官方存储库](https://github.com/davidacm/NVDA-IBMTTS-Driver)获取并安装新版，旧版本会被删除，包括语音库。一种解决方案是将语音库安装在单独的插件中。
[点击此链接](https://github.com/davidacm/ECILibrariesTemplate)了解如何将语音库打包到单独的插件中。

## 注意 

* 如果本驱动使用了 [“eciLibraries”](https://github.com/davidacm/ECILibrariesTemplate)驱动会自动更新 ini 库路径。所以你可以在便携版 NVDA 中使用该驱动。
* 当您使用“将所依赖的语音文件复制到驱动目录”按钮时，会创建一个新的插件。因此，如果您想卸载 IBMTTS，您就需要卸载两个插件：“IBMTTS 驱动程序”和“Eci 库”。
* 此项目的scons和gettext工具只与python 3兼容。不适用于python 2.7。
* 您可以将另外的 IBMTTS所需文件放在插件中（仅供个人使用）。只需将它们复制到“addon\synthDrivers\ibmtts”文件夹中即可。如有必要，还可调整“settingsDB.py”中的默认库名称。

## 报告问题：

如果您发现某些与此驱动兼容的库存在安全问题，请不要在问题解决之前打开 github Issue 或在论坛上发贴。请通过[此表单](https://docs.google.com/forms/d/123gSqayOAsIQLx1NiI98fEqr46oiJRZ9nNq0_KIF9WU/edit) 提交。

如果问题不会导致驱动或屏幕阅读器崩溃，请在此处打开 [github Issue](https://github.com/davidacm/NVDA-IBMTTS-Driver/issues)

## 参考

此驱动程序基于 IBM tts sdk，文档位于：[此处](http://www.wizzardsoftware.com/docs/tts.pdf)

或者从[哥伦比亚大学](http://www1.cs.columbia.edu/~hgs/research/projects/simvoice/simvoice/docs/tts.pdf) 获取另一个副本。
还可以从 [这个repo](https://github.com/david-acm/NVDA-IBMTTS-Driver) 上获取备用副本。

[pyibmtts：由 Peter Parente 开发的用于 IBM TTS 的 Python 封装](https://sourceforge.net/projects/ibmtts-sdk/)

在此处查看备份文件：
[tts.pdf](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.pdf)
或 [tts.txt](https://cdn.jsdelivr.net/gh/davidacm/NVDA-IBMTTS-Driver/apiReference/tts.txt)
