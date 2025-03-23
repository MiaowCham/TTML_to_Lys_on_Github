# TTML to Lys on Github
###### **TTML to Lyricify Syllable Tool** 本地脚本已迁移至单独仓库 [点我前往](https://github.com/MiaowCham/TTML_to_Lyricify_Syllable_Tool)
**TTML to Lys on Github** 主要用于实现从 GitHub Issue 中获取歌词内容，将 ttml 格式歌词转换为 lys，然后将处理后的结果以评论的形式附加到该 Issue 中。该工具通过 Python 实现，依赖于 GitHub API 和正则表达式技术，能够高效、智能地完成歌词内容的清理工作。

### > [点击这里使用本工具](https://github.com/HKLHaoBin/ttml_to_lys/issues/new/choose) <

### **使用方法：**
1. 新建`issue 议题`，选择`TTML歌词转Lys`模板
3. 将需要转换的 **ttml** 格式的歌词复制到`Description 描述`中
4. 发送 **issue** 并等待脚本转换
**转换完成后 Github-actions 会将结果回复在该 issue 下**
###### 没了，就这么简单（乐
### **用前须知：**
- 尽量将标题改为文件名或歌曲名，以便区分
- issue 的`Label 标签`必需是`ttml_to_lys`才会触发转换
- 转换没有对唱的歌词，歌词属性可能会出现 `[0]` `[3]` `[6]`，属于正常情况
---
**已知问题：**
对唱歌词的背景人声对唱属性错误，始终为 `[7]`。预计下个版本修复

### 功能特点
 **GitHub 集成**：
   - 从指定 GitHub Issue 中提取内容。
   - 将修正后的结果以评论形式提交到相应的 Issue 中。

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
