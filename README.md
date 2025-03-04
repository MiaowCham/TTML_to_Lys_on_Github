# TTML to Lyricify Syllable tool
**一个适用于 AMLL TTML 文件转 Lyricify Syllable 的小工具**

开发者是[**喵锵**](https://github.com/MiaowCham)，初始版本由 DeepSeek 构建。
现在[**浩彬**](https://github.com/HKLHaoBin)将工具进行了修改，得以在 GitHub Issue 中使用

TTML 是 AMLL 使用的歌词文件，但很不幸的是：他们并不兼容。并且使用 AMLL TTML Tool 输出的 Lys 格式及其不规范，TTML to Lyricify Syllable tool 就是为了解决这个问题而诞生的。

现在，一拖、一按，即可完成规范化转换！甚至可以提取翻译并单独输出。

### 使用说明
   - 直接将待转换的 ttml 文件拖入工具图标或命令行窗口即可完成转换
   - 默认输出目录为`output`文件夹,具体输出路径可自行修改
   - 本工具需要 Python 3.x 以上环境（实际仅在3.11和3.12测试）
   - 在`log\log.set`文件中输入"log_on:True"即可开启日志输出

## TTML to Lys on Github
TTML to Lys on Github 主要用于实现从 GitHub Issue 中获取歌词内容，将ttml格式歌词转换为lys，然后将处理后的结果以评论的形式附加到该 Issue 中。该工具通过 Python 实现，依赖于 GitHub API 和正则表达式技术，能够高效、智能地完成歌词内容的清理工作。

### [点击这里使用本工具](https://github.com/HKLHaoBin/ttml_to_lys/issues)

### 功能特点
 **GitHub 集成**：
   - 从指定 GitHub Issue 中提取内容。
   - 将修正后的结果以评论形式提交到相应的 Issue 中。

### 使用说明

脚本会自动从指定的 GitHub Issue 中读取内容，处理后将结果作为评论添加到 Issue 中。

## 示例
假设 Issue 内容为：
```
<span begin="00:03.694" end="00:04.078">English </span><span begin="00:04.078" end="00:04.410">version </span><span begin="00:04.410" end="00:04.799">one</span>
<span begin="00:03.694" end="00:04.078">English</span> <span begin="00:04.078" end="00:04.410">version</span> <span begin="00:04.410" end="00:04.799">one</span>
```

脚本处理后会生成以下结果并作为评论提交：
```
Processed Lyrics:
[4]English (3694,384)version (4078,332)one(4410,389)
```

## 注意事项
 输入文本格式应与工具的处理逻辑相匹配，以确保修正效果最佳。

## 许可证
此项目使用 MIT 许可证。
