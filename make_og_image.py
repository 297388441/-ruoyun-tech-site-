#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成若云科技 Open Graph 预览图（1200x630），裁掉底部水印并叠加品牌文字。"""
from PIL import Image, ImageDraw, ImageFont
import os

SRC = "/Users/a123456/WorkBuddy/2026-08-11-00-08-08/site/images/Professional_B2B_digital_marke_2026-08-21T13-43-00.png"
OUT = "/Users/a123456/WorkBuddy/2026-08-11-00-08-08/site/images/ruoyun-og-2026.png"
FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"

# 品牌色
NAVY = "#081830"
ORANGE = "#ff6a13"
WHITE = "#ffffff"
CYAN = "#37c2e0"

def hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return (r, g, b, alpha)

def main():
    img = Image.open(SRC).convert("RGBA")
    w, h = img.size
    print(f"源图尺寸: {w}x{h}")

    # 目标 1200x630 (1.91:1)。源图 1536x1024，先按目标比例从顶部裁切，排除底部水印。
    target_ratio = 1200 / 630  # ≈1.9048
    crop_h = int(w / target_ratio)  # 1536 / 1.9048 ≈ 806
    crop_box = (0, 0, w, crop_h)
    cropped = img.crop(crop_box)
    print(f"裁切区域: {crop_box}")

    # 缩放到 1200x630
    og = cropped.resize((1200, 630), Image.Resampling.LANCZOS)

    # 加半透明暗色渐变遮罩（左侧文字区更易读）
    overlay = Image.new("RGBA", og.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    # 从左侧到右侧的渐变：左 60% 较深，右 40% 透明
    for x in range(og.width):
        alpha = int(max(0, 140 - (x / og.width) * 180))
        draw.line([(x, 0), (x, og.height)], fill=(8, 24, 48, alpha), width=1)

    og = Image.alpha_composite(og, overlay)
    draw = ImageDraw.Draw(og)

    # 字体
    font_title = ImageFont.truetype(FONT_PATH, 64)
    font_line1 = ImageFont.truetype(FONT_PATH, 42)
    font_line2 = ImageFont.truetype(FONT_PATH, 36)
    font_note = ImageFont.truetype(FONT_PATH, 24)

    # 文字内容
    title = "东莞市若云科技有限公司"
    line1 = "工厂抖音获客代运营"
    line2 = "GEO 让AI也推荐你"
    note = "抖音「小赖的运营笔记」运营主体"

    x_left = 60
    y_title = 120
    y_line1 = y_title + 90
    y_line2 = y_line1 + 70
    y_note = y_line2 + 90

    # 主标题（白）
    draw.text((x_left, y_title), title, font=font_title, fill=WHITE)
    # 业务线（橙）
    draw.text((x_left, y_line1), line1, font=font_line1, fill=ORANGE)
    # GEO 线（青）
    draw.text((x_left, y_line2), line2, font=font_line2, fill=CYAN)
    # 小字（白半透明）
    draw.text((x_left, y_note), note, font=font_note, fill=(255, 255, 255, 220))

    # 保存为 PNG
    og = og.convert("RGB")
    og.save(OUT, "PNG", optimize=True)
    print(f"已保存: {OUT}, 尺寸: {og.size}")

if __name__ == "__main__":
    main()
