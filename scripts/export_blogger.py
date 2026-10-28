#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音博主批量导出工具：一键下载博主全部视频 + 语音转写 + 生成Obsidian笔记
完全本地运行，不需要任何第三方API Key
"""
import argparse
import re
import subprocess
from pathlib import Path
from datetime import datetime

try:
    from faster_whisper import WhisperModel
except ImportError:
    print("请先安装依赖：pip install faster-whisper")
    exit(1)

def sanitize_filename(name: str) -> str:
    """清理文件名非法字符"""
    return re.sub(r'[\\/:*?"<>|]', '_', name)[:100]

def download_blogger_videos(blogger_url: str, tiktok_downloader_path: Path, output_dir: Path):
    """调用TikTokDownloader批量下载博主所有视频"""
    print(f"开始下载博主视频: {blogger_url}")
    # TikTokDownloader 命令行调用逻辑，后续适配
    # 这里先预留接口，后续可以直接调用它的Python API
    print("（预留：后续对接TikTokDownloader自动下载逻辑）")

def transcribe_video(video_path: Path, model: WhisperModel) -> str:
    """Whisper语音识别"""
    segments, info = model.transcribe(str(video_path), language="zh", beam_size=5)
    return "".join([seg.text for seg in segments]).strip()

def generate_obsidian_note(video_path: Path, transcript: str, output_dir: Path, blogger_name: str):
    """生成Obsidian格式笔记"""
    blogger_dir = output_dir / sanitize_filename(blogger_name)
    blogger_dir.mkdir(parents=True, exist_ok=True)

    title = sanitize_filename(video_path.stem)
    note_path = blogger_dir / f"{datetime.now().strftime('%Y-%m-%d')}-{title}.md"

    content = f"""---
title: {title}
author: {blogger_name}
create_time: {datetime.now().strftime('%Y-%m-%d')}
source: 抖音
tags: [抖音, 视频转写, {blogger_name}]
---

# {title}

## 完整口播文案

{transcript}
"""
    note_path.write_text(content, encoding='utf-8')
    return note_path

def main():
    parser = argparse.ArgumentParser(description='抖音博主批量导出工具')
    parser.add_argument('blogger_url', help='抖音博主主页链接')
    parser.add_argument('--blogger-name', required=True, help='博主名字，用于建文件夹')
    parser.add_argument('--video-dir', default='./output/videos', help='视频临时存放目录')
    parser.add_argument('--note-output', default=r'H:\知识库\抖音博主', help='Obsidian笔记输出目录')
    parser.add_argument('--whisper-model', default='small', help='Whisper模型大小')
    args = parser.parse_args()

    video_dir = Path(args.video_dir)
    note_dir = Path(args.note_output)
    video_dir.mkdir(parents=True, exist_ok=True)
    note_dir.mkdir(parents=True, exist_ok=True)

    # 第一步：下载博主视频
    download_blogger_videos(args.blogger_url, Path(r"H:\Tools\TikTokDownloader"), video_dir)

    # 第二步：加载Whisper模型
    print(f"加载Whisper模型: {args.whisper_model}...")
    model = WhisperModel(args.whisper_model, device="auto", compute_type="auto")

    # 第三步：批量转写
    videos = list(video_dir.glob("*.mp4"))
    print(f"共找到 {len(videos)} 个视频，开始转写...")

    success = 0
    for i, video in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}] 转写: {video.name}")
        try:
            transcript = transcribe_video(video, model)
            note_path = generate_obsidian_note(video, transcript, note_dir, args.blogger_name)
            print(f"  完成: {note_path.name}")
            success += 1
        except Exception as e:
            print(f"  失败: {e}")

    print(f"\n=== 全部完成 ===")
    print(f"成功转写 {success} 个视频")
    print(f"笔记位置: {note_dir / args.blogger_name}")

if __name__ == '__main__':
    main()
