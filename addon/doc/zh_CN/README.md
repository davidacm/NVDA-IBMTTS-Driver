# NVDA插件， IBMTTS 驱动程序

* 此插件实现了 NVDA 与 IBMTTS 合成器的兼容。

* 因为我们无法发布 IBMTTS 库，这只是一个驱动程序。
* 如果您想改进此驱动程序，请随时发送您的 Pull request 。

# 下载
最新版本可在[此链接下载](https://davidacm.github.io/getlatest/gh/davidacm/NVDA-IBMTTS-Driver)

## 特性:
* 支持语音，变体，速率，音高，变形和音量设置。
* 另外还支持额外的头部尺寸，粗糙度，呼吸参数设置。你可以创造属于你自己的声音！
* 能够启用或禁用反引号语音标签。禁用该选项可以保护自己免受那些恶意语音代码的干扰，启用该选项，可以使 NVDA 合成器做一些有趣的事情。
* 语速加倍。如果您认为合成器的语速不够快，那么启用该选项可以大幅提高语音速度。
* 完整过滤。该驱动程序包括一套完整的过滤器，用于修复合成器的崩溃和其他奇怪行为。
* 自动语言切换。让合成器以正确的语言朗读相应语种的文本。
* 词典支持。此驱动程序支持集成各种语言的特殊词、词根和缩写用户词典。现成的词典可以从[社区词典存储库](https://github.com/thunderdrop/IBMTTSDictionaries) 或 [mohamed00 的替代存储库（包含 IBM 合成器词典）](https://github.com/mohamed00/AltIBMTTSDictionaries)中获取。

## 要求

## NVDA
  您需要NVDA 2018.4或更高版本。此驱动程序与python 3兼容，因此您可以将其用于以后的 NVDA 版本。一旦发布了 python 3 版 NVDA，该驱动程序将不再兼容 python 2.7。请使用最新的NVDA版本。此插件完全免费！

## IBMTTS合成器库
* 这只是驱动程序，您必须从其他地方获取库。
*  此驱动程序支持添加东亚语言较新的库，并针对文本编码进行了特定的修复。不过，旧的库应该也可以工作。
*  从 21.01 版起，
*该驱动程序还支持新版的 IBM 二进制文件，而不仅仅是 SpeechWorks 二进制文件。另外还有针对该驱动程序的一组独立修复程序，考虑了其他语言和差异。目前仅支持格式化语音。感谢 @mohamed00 的工作。

## 安装
* 只需将其安装为NVDA插件即可。然后打开NVDA设置面板，并在IBMTTS类别中设置IBMTTS目录。
* 此外，您还可以将外部IBMTTS文件复制到插件中。

## 打包分发
* 打开命令行，切换到插件目录，并执行 scons 命令。如果没有错误，则创建的插件将放在根目录中。
* 如果合成器在插件内，驱动程序将自动更新ini库路径。因此，您也可以在NVDA便携版上使用。
* 当您使用“将所依赖的语音文件复制到驱动目录”按钮时，会创建一个新的插件。因此，如果要卸载 IBMTTS，则需要卸载两个插件：“IBMTTS 驱动程序”和“Eci 库”。

## 注意
* 此项目的scons和gettext工具只与python 3兼容。不适用于python 2.7。
* 您可以将另外的 IBMTTS所需文件放在插件中（仅供个人使用）。只需将它们复制到“addon\synthDrivers\ibmtts”文件夹中即可。如有必要，还可调整“settingsDB.py”中的默认库名称。
# 参考
此驱动程序基于 IBM tts sdk，文档位于：
[此链接](http://www.wizzardsoftware.com/docs/tts.pdf)
或者你也可以在 [t本仓库](https://github.com/david-acm/NVDA-IBMTTS-Driver) 上获得一份副本。
