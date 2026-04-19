#!/usr/bin/env python3
"""
PDF图片批量提取工具
从PDF文件中提取所有嵌入的图片，保存为高清图片文件
命名格式：PDF文件名_图片序号.扩展名
"""

import os
import sys
import fitz  # PyMuPDF
from PIL import Image
import argparse
import traceback

def extract_images_from_pdf(pdf_path, output_dir=None, quality=95):
    """
    从PDF文件中提取所有图片

    参数:
        pdf_path: PDF文件路径
        output_dir: 输出目录，默认为PDF文件所在目录
        quality: JPEG图片质量（1-100），仅对JPEG格式有效
    """
    if not os.path.exists(pdf_path):
        print(f"错误: PDF文件不存在: {pdf_path}")
        return False

    # 确定输出目录
    if output_dir is None:
        output_dir = os.path.dirname(pdf_path)
        if output_dir == "":
            output_dir = "."

    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    # 获取PDF文件名（不含扩展名）
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # 打开PDF文件
    try:
        pdf_document = fitz.open(pdf_path)
    except Exception as e:
        print(f"错误: 无法打开PDF文件: {e}")
        return False

    total_images = 0
    extracted_count = 0

    print(f"正在处理: {pdf_path}")
    print(f"PDF总页数: {len(pdf_document)}")

    # 遍历所有页面
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]

        # 获取页面中的所有图片
        image_list = page.get_images(full=True)

        if image_list:
            print(f"  第 {page_num + 1} 页: 找到 {len(image_list)} 张图片")

        # 提取每张图片
        for img_index, img_info in enumerate(image_list):
            total_images += 1

            try:
                # 获取图片的xref
                xref = img_info[0]

                # 提取图片
                base_image = pdf_document.extract_image(xref)

                if base_image:
                    # 获取图片数据
                    image_data = base_image["image"]
                    image_ext = base_image["ext"]
                    image_width = base_image["width"]
                    image_height = base_image["height"]

                    # 确定图片格式和扩展名
                    ext_map = {
                        "jpeg": "jpg",
                        "jpg": "jpg",
                        "png": "png",
                        "gif": "gif",
                        "bmp": "bmp",
                        "tiff": "tiff",
                        "jp2": "jp2"
                    }

                    # 使用映射中的扩展名，否则使用原始扩展名
                    file_ext = ext_map.get(image_ext.lower(), image_ext.lower())

                    # 生成输出文件名
                    output_filename = f"{pdf_name}_{total_images:03d}.{file_ext}"
                    output_path = os.path.join(output_dir, output_filename)

                    # 保存图片
                    with open(output_path, "wb") as img_file:
                        img_file.write(image_data)

                    # 如果是JPEG格式且指定了质量，使用Pillow重新保存以控制质量
                    if file_ext in ["jpg", "jpeg"] and quality < 100:
                        try:
                            img = Image.open(output_path)
                            img.save(output_path, "JPEG", quality=quality, optimize=True)
                        except Exception as e:
                            print(f"      警告: 无法优化JPEG质量: {e}")

                    extracted_count += 1
                    print(f"      已保存: {output_filename} ({image_width}x{image_height})")

            except Exception as e:
                print(f"      错误: 提取图片失败 (第{total_images}张): {e}")

    pdf_document.close()

    print(f"\n处理完成!")
    print(f"  总共找到图片: {total_images} 张")
    print(f"  成功提取: {extracted_count} 张")
    print(f"  输出目录: {output_dir}")

    return extracted_count > 0

def batch_extract_from_directory(input_dir, output_dir=None, quality=95):
    """
    批量处理目录中的所有PDF文件

    参数:
        input_dir: 输入目录，包含PDF文件
        output_dir: 输出目录
        quality: JPEG图片质量
    """
    if not os.path.exists(input_dir):
        print(f"错误: 输入目录不存在: {input_dir}")
        return False

    pdf_files = []
    for file in os.listdir(input_dir):
        if file.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(input_dir, file))

    if not pdf_files:
        print(f"错误: 在目录中没有找到PDF文件: {input_dir}")
        return False

    print(f"找到 {len(pdf_files)} 个PDF文件")

    success_count = 0
    for pdf_file in pdf_files:
        print(f"\n{'='*50}")
        success = extract_images_from_pdf(pdf_file, output_dir, quality)
        if success:
            success_count += 1

    print(f"\n{'='*50}")
    print(f"批量处理完成!")
    print(f"  成功处理: {success_count}/{len(pdf_files)} 个PDF文件")

    return success_count > 0

def main():
    parser = argparse.ArgumentParser(
        description="从PDF文件中提取所有嵌入的图片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 提取单个PDF文件中的图片
  python pdf_image_extractor.py document.pdf

  # 提取PDF文件中的图片到指定目录
  python pdf_image_extractor.py document.pdf -o ./images/

  # 批量提取目录中的所有PDF文件
  python pdf_image_extractor.py -d ./pdf_files/

  # 设置JPEG图片质量
  python pdf_image_extractor.py document.pdf -q 90
        """
    )

    # 主参数组
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("pdf_file", nargs="?", help="PDF文件路径")
    group.add_argument("-d", "--directory", help="包含PDF文件的目录路径")

    # 可选参数
    parser.add_argument("-o", "--output", help="输出目录路径")
    parser.add_argument("-q", "--quality", type=int, default=95,
                       help="JPEG图片质量 (1-100, 默认: 95)")
    parser.add_argument("-v", "--version", action="version",
                       version="PDF图片提取工具 v1.0")

    args = parser.parse_args()

    try:
        if args.directory:
            # 批量处理目录
            success = batch_extract_from_directory(
                args.directory, args.output, args.quality
            )
            sys.exit(0 if success else 1)
        else:
            # 处理单个文件
            success = extract_images_from_pdf(
                args.pdf_file, args.output, args.quality
            )
            sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"程序发生错误: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()