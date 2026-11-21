# 更新日志

本文件记录对外可见的版本变化。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

## [0.1.0] - 2026-11-21

### 新增

- 提供番剧领域插件，通过 `sr.plugins` 入口注册为 `anime`，支持 `structured-renamer >=0.2.0,<0.3.0`。
- 提供 `anime:bangumi_search`，根据作品标题查询 Bangumi，返回中文名和放送日期；优先选择标题精确匹配的条目。
- 提供 `anime:file_resolution`，读取本地视频流的实际宽高，输出宽度、高度及 `宽x高` 格式的尺寸文本。
- 提供番剧重命名示例规则，结合宿主的字段解析、分组借值和加工能力，组合中文名、年份、集号及视频高度等信息。
- 提供安装说明、能力输入输出文档及规则示例，说明 Bangumi 网络访问和 `ffprobe` 等运行依赖。
