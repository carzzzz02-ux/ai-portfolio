#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 工具导航站 - 内容同步脚本
功能：将网站内容自动同步到各平台（小红书/知乎/抖音）
"""

import os
import json
from datetime import datetime

# 配置
CONFIG = {
    "xiaohongshu": {
        "enabled": True,
        "output_dir": "output/xiaohongshu",
    },
    "zhihu": {
        "enabled": True,
        "output_dir": "output/zhihu",
    },
    "douyin": {
        "enabled": True,
        "output_dir": "output/douyin",
    }
}

def read_markdown(filepath):
    """读取 Markdown 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def parse_xiaohongshu(content):
    """解析小红书文案"""
    posts = []
    current_post = {}
    
    lines = content.split('\n')
    for line in lines:
        if line.startswith('## 文案'):
            if current_post:
                posts.append(current_post)
            current_post = {'title': '', 'content': ''}
        elif line.startswith('**标题：**'):
            current_post['title'] = line.replace('**标题：**', '').strip()
        elif line.startswith('**正文：**'):
            continue
        elif current_post.get('title') and line.strip():
            current_post['content'] += line + '\n'
    
    if current_post:
        posts.append(current_post)
    
    return posts

def save_post(platform, title, content, index):
    """保存帖子到文件"""
    output_dir = CONFIG[platform]['output_dir']
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{output_dir}/post_{index:02d}_{datetime.now().strftime('%Y%m%d')}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"标题：{title}\n")
        f.write("=" * 50 + "\n\n")
        f.write(content)
    
    print(f"✓ 已保存：{filename}")

def sync_xiaohongshu():
    """同步小红书内容"""
    print("\n📱 同步小红书内容...")
    
    content = read_markdown('marketing/xiaohongshu.md')
    posts = parse_xiaohongshu(content)
    
    for i, post in enumerate(posts, 1):
        if post.get('title'):
            save_post('xiaohongshu', post['title'], post['content'], i)
    
    print(f"✓ 小红书内容同步完成，共 {len(posts)} 篇")

def sync_zhihu():
    """同步知乎内容"""
    print("\n📖 同步知乎内容...")
    
    content = read_markdown('marketing/zhihu.md')
    
    # 简单分割（每个回答以"## 回答"开头）
    answers = content.split('## 回答')
    
    for i, answer in enumerate(answers[1:], 1):  # 跳过第一个空块
        lines = answer.split('\n')
        title_line = lines[0].strip()
        title = title_line.replace(':', '').replace('？', '?')
        
        save_post('zhihu', f"回答{i}_{title}", answer, i)
    
    print(f"✓ 知乎内容同步完成，共 {len(answers)-1} 篇")

def sync_douyin():
    """同步抖音内容"""
    print("\n🎬 同步抖音内容...")
    
    content = read_markdown('marketing/douyin.md')
    
    # 简单分割（每个脚本以"## 脚本"开头）
    scripts = content.split('## 脚本')
    
    for i, script in enumerate(scripts[1:], 1):  # 跳过第一个空块
        lines = script.split('\n')
        title_line = lines[0].strip() if lines else f"脚本{i}"
        title = title_line.split('：')[0] if ':' in title_line else title_line
        
        save_post('douyin', f"脚本{i}_{title}", script, i)
    
    print(f"✓ 抖音内容同步完成，共 {len(scripts)-1} 个")

def generate_content_calendar():
    """生成内容发布日历"""
    print("\n📅 生成内容发布日历...")
    
    calendar = {
        "generated_at": datetime.now().isoformat(),
        "schedule": []
    }
    
    # 小红书 - 每周 3 篇
    for i in range(1, 11):
        calendar["schedule"].append({
            "platform": "xiaohongshu",
            "content": f"文案{i}",
            "week": (i - 1) // 3 + 1,
            "day": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][(i - 1) % 7],
            "time": ["8:00", "12:00", "20:00"][(i - 1) % 3]
        })
    
    # 知乎 - 每周 2 篇
    for i in range(1, 6):
        calendar["schedule"].append({
            "platform": "zhihu",
            "content": f"回答{i}",
            "week": (i - 1) // 2 + 1,
            "day": ["周三", "周日"][(i - 1) % 2],
            "time": "20:00"
        })
    
    # 抖音 - 每周 2 篇
    for i in range(1, 11):
        calendar["schedule"].append({
            "platform": "douyin",
            "content": f"脚本{i}",
            "week": (i - 1) // 2 + 1,
            "day": ["周一", "周三", "周五", "周六", "周日"][(i - 1) % 5],
            "time": ["12:00", "18:00", "20:00"][(i - 1) % 3]
        })
    
    # 保存日历
    os.makedirs('output', exist_ok=True)
    with open('output/content_calendar.json', 'w', encoding='utf-8') as f:
        json.dump(calendar, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 内容发布日历已生成：output/content_calendar.json")

def main():
    """主函数"""
    print("=" * 60)
    print("🤖 AI 工具导航站 - 内容同步脚本")
    print("=" * 60)
    
    # 同步各平台内容
    if CONFIG["xiaohongshu"]["enabled"]:
        sync_xiaohongshu()
    
    if CONFIG["zhihu"]["enabled"]:
        sync_zhihu()
    
    if CONFIG["douyin"]["enabled"]:
        sync_douyin()
    
    # 生成内容日历
    generate_content_calendar()
    
    print("\n" + "=" * 60)
    print("✅ 所有内容同步完成！")
    print("=" * 60)
    print("\n📂 输出目录：output/")
    print("📅 发布日历：output/content_calendar.json")
    print("\n💡 下一步：")
    print("1. 查看 output/ 目录中的内容文件")
    print("2. 按照 content_calendar.json 的安排发布")
    print("3. 记录各平台数据，优化内容策略")

if __name__ == "__main__":
    main()
