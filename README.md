# sr-plugin-anime

[structured-renamer](https://github.com/zaixiamomo/structured-renamer) 的插件，提供番剧领域相关能力。

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> 0.x alpha：插件能力与宿主 API 可能变化。

- `anime:bangumi_search`：查询作品中文名和放送日期。
- `anime:file_resolution`：读取视频实际宽高。

输入输出、规则示例及使用限制见[插件能力说明](docs/extenders.md)。

## 安装

需要 Python 3.10+、Git 和 uv。准备主项目与本插件的源码：

```powershell
git config --global core.longpaths true
git clone https://github.com/zaixiamomo/structured-renamer.git
git clone https://github.com/zaixiamomo/sr-plugin-anime.git
uv tool install ".\structured-renamer" --with ".\sr-plugin-anime"
sr --version
```

两个包安装在同一个工具环境中，之后通过 `sr` 使用插件。

## Demo

规则位于 [demo/rule.yaml](demo/rule.yaml)，演示文件位于 `demo/examples`。
需要可访问 Bangumi API，PATH 中有 `ffprobe`，且视频可被正常读取。

```powershell
sr --dir ./demo/examples --rule ./demo/rule.yaml --dry-out
sr --dir ./demo/examples --rule ./demo/rule.yaml
sr --dir ./demo/examples --undo
```

先核对预览再执行，处理自己的文件时替换 `--dir`。
现有规则按同目录集号或标题关联视频和字幕；剧集固定 `s01`，电影省略季集号。
不同作品同集号不应混放一个目录；发布组和字幕语言需在规则中配置映射。

## License

[MIT](LICENSE)
