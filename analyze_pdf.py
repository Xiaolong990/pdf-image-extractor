#!/usr/bin/env python3
"""
分析PDF结构，识别带"Figure n"图注的图片
"""

import fitz  # PyMuPDF
import sys
import os

def analyze_pdf_structure(pdf_path):
    """分析PDF结构，查找图片和附近文本"""
    if not os.path.exists(pdf_path):
        print(f"错误: PDF文件不存在: {pdf_path}")
        return

    print(f"分析PDF文件: {pdf_path}")

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"无法打开PDF文件: {e}")
        return

    total_pages = len(doc)
    print(f"总页数: {total_pages}")

    # 分析每页
    for page_num in range(total_pages):
        page = doc[page_num]

        # 获取页面文本和位置信息
        text_dict = page.get_text("dict")

        # 获取所有图片
        image_list = page.get_images(full=True)

        if image_list:
            print(f"\n=== 第 {page_num + 1} 页 ===")
            print(f"  找到 {len(image_list)} 张图片")

            # 分析页面文本块
            blocks = text_dict.get("blocks", [])
            text_blocks = []

            for block in blocks:
                if block.get("type") == 0:  # 文本块
                    text = block.get("lines", [])
                    block_text = ""
                    for line in text:
                        for span in line.get("spans", []):
                            block_text += span.get("text", "")
                    if block_text.strip():
                        bbox = block.get("bbox", (0, 0, 0, 0))
                        text_blocks.append({
                            "text": block_text.strip(),
                            "bbox": bbox,
                            "page": page_num
                        })

            # 打印所有文本块（包含Figure的）
            figure_texts = []
            for tb in text_blocks:
                text_lower = tb["text"].lower()
                if "figure" in text_lower or "fig." in text_lower:
                    figure_texts.append(tb)
                    print(f"  发现图注文本: '{tb['text']}' 位置: {tb['bbox']}")

            # 分析每张图片
            for img_idx, img_info in enumerate(image_list):
                xref = img_info[0]

                try:
                    # 提取图片信息
                    base_image = doc.extract_image(xref)
                    if base_image:
                        width = base_image["width"]
                        height = base_image["height"]

                        # 获取图片在页面中的位置（近似）
                        # 注意：PyMuPDF中图片位置信息不直接可用，需要从渲染中推断
                        # 这里使用简单的大小过滤

                        print(f"  图片 {img_idx + 1}: {width}x{height} px")

                        # 判断是否为可能的小图标
                        is_small = width < 100 or height < 100
                        is_medium = 100 <= width <= 500 and 100 <= height <= 500
                        is_large = width > 500 or height > 500

                        size_category = "大图" if is_large else ("中图" if is_medium else "小图/图标")

                        # 检查附近是否有Figure文本
                        has_figure_nearby = False
                        if figure_texts:
                            # 简单判断：如果图片是大图且页面有Figure文本，可能相关
                            if is_large:
                                print(f"    → 可能是正文图片 ({size_category})")
                                has_figure_nearby = True

                        if is_small:
                            print(f"    → 可能是小图标 ({size_category})")
                        elif not has_figure_nearby and is_large:
                            print(f"    → 大图但未检测到Figure文本 ({size_category})")

                except Exception as e:
                    print(f"  图片 {img_idx + 1} 分析失败: {e}")

    doc.close()
    print("\n分析完成")

def analyze_extracted_images(image_dir):
    """分析已提取的图片"""
    if not os.path.exists(image_dir):
        print(f"错误: 图片目录不存在: {image_dir}")
        return

    print(f"\n分析已提取的图片目录: {image_dir}")

    import glob
    image_files = glob.glob(os.path.join(image_dir, "*.*"))

    # 按扩展名分类
    from collections import defaultdict
    by_ext = defaultdict(list)

    for img_path in image_files:
        ext = os.path.splitext(img_path)[1].lower()
        by_ext[ext].append(img_path)

    print(f"总计图片: {len(image_files)} 张")
    for ext, files in by_ext.items():
        print(f"  {ext}: {len(files)} 张")

    # 分析图片尺寸（需要PIL）
    try:
        from PIL import Image

        size_stats = []
        for img_path in image_files[:20]:  # 只分析前20张
            try:
                with Image.open(img_path) as img:
                    width, height = img.size
                    size_stats.append((width, height, img_path))
            except Exception as e:
                print(f"  无法读取图片 {os.path.basename(img_path)}: {e}")

        if size_stats:
            print("\n图片尺寸分析:")
            # 按面积排序
            size_stats.sort(key=lambda x: x[0]*x[1], reverse=True)

            print("  最大图片:")
            for i, (w, h, path) in enumerate(size_stats[:5]):
                area = w * h
                filename = os.path.basename(path)
                print(f"    {filename}: {w}x{h} (面积: {area:,})")

            print("\n  最小图片:")
            for i, (w, h, path) in enumerate(size_stats[-5:]):
                area = w * h
                filename = os.path.basename(path)
                print(f"    {filename}: {w}x{h} (面积: {area:,})")

    except ImportError:
        print("  需要Pillow库进行图片尺寸分析")

if __name__ == "__main__":
    pdf_file = "demo.pdf"
    image_dir = "demo_images"

    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]

    analyze_pdf_structure(pdf_file)

    if os.path.exists(image_dir):
        analyze_extracted_images(image_dir)

    # 提供改进建议
    print("\n" + "="*60)
    print("改进建议:")
    print("1. 基于尺寸过滤: 过滤掉宽度或高度小于100px的小图标")
    print("2. 基于面积过滤: 设置最小面积阈值 (如 10,000 像素)")
    print("3. 基于宽高比过滤: 正文图片通常有特定宽高比")
    print("4. 结合页面文本分析: 查找图片附近的'Figure'文本")
    print("5. 位置过滤: 正文图片通常不在页面边缘")