# douyin-batch-exporter

一键批量导出抖音博主全部视频口播文案，完全本地运行，不需要任何第三方API Key。

## 功能
- 输入博主主页链接，自动批量下载所有视频
- 本地 Whisper 语音识别，把视频口播转成完整文字
- 自动生成 Obsidian 格式笔记，归档到本地知识库
- 数据完全本地存储，不依赖任何第三方云服务

## 依赖
- Python 3.10+
- faster-whisper
- TikTokDownloader（用于批量下载抖音视频）

## 使用方法
```bash
python scripts/export_blogger.py "https://www.douyin.com/user/xxx" --blogger-name "博主名字"
```

## 目录结构
```
douyin-batch-exporter/
├── scripts/
│   └── export_blogger.py    # 主脚本
├── output/                  # 视频临时存放目录
├── config/                  # 配置文件
└── README.md
```

## 后续路线图
- [ ] 自动对接 TikTokDownloader API，无需手动交互
- [ ] 本地 Ollama 自动总结知识点、提炼金句
- [ ] 支持批量导出自己的收藏夹内容
- [ ] 自动同步到 Obsidian 知识库
