# 项目介绍和使用说明书

## 项目名称
**ttml_to_lys**

开发者是**[喵酱](https://github.com/MiaowCham)**，我将工具略作修改，写了一份配置文件，得以在 GitHub Issue 中使用

## 项目简介
ttml_to_lys 是一个工具，用于从 GitHub Issue 中获取歌词内容，将ttml格式歌词转换为lys，然后将处理后的结果以评论的形式附加到该 Issue 中。该工具通过 Python 实现，依赖于 GitHub API 和正则表达式技术，能够高效、智能地完成歌词内容的清理工作。

# [点击这里使用本工具](https://github.com/HKLHaoBin/ttml_to_lys/issues)
---

## 功能特点
 **GitHub 集成**：
   - 从指定 GitHub Issue 中提取内容。
   - 将修正后的结果以评论形式提交到相应的 Issue 中。

---

## 使用说明

脚本会自动从指定的 GitHub Issue 中读取内容，处理后将结果作为评论添加到 Issue 中。

---

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
