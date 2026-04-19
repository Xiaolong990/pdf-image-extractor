# PDF图片批量提取工具

一个Python脚本，用于从PDF文件中批量提取所有嵌入的图片，并以高清质量保存到本地目录。

## 功能特性

- ✅ 从PDF文件中提取所有嵌入的图片
- ✅ 批量处理目录中的所有PDF文件
- ✅ 自动识别图片格式（JPEG、PNG、GIF、BMP、TIFF等）
- ✅ 图片命名格式：`PDF文件名_图片序号.扩展名`
- ✅ 支持JPEG图片质量调整
- ✅ 错误处理和进度显示

## 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install PyMuPDF Pillow
```

## 使用方法

### 1. 提取单个PDF文件中的图片

```bash
python pdf_image_extractor.py document.pdf
```

### 2. 提取图片到指定目录

```bash
python pdf_image_extractor.py document.pdf -o ./images/
```

### 3. 批量提取目录中的所有PDF文件

```bash
python pdf_image_extractor.py -d ./pdf_files/
```

### 4. 设置JPEG图片质量

```bash
python pdf_image_extractor.py document.pdf -q 90
```

### 5. 查看帮助

```bash
python pdf_image_extractor.py -h
```

## 参数说明

| 参数 | 缩写 | 说明 |
|------|------|------|
| `pdf_file` | 无 | PDF文件路径（必需，除非使用`-d`参数） |
| `-d`, `--directory` | `-d` | 包含PDF文件的目录路径 |
| `-o`, `--output` | `-o` | 输出目录路径（默认：PDF文件所在目录） |
| `-q`, `--quality` | `-q` | JPEG图片质量（1-100，默认：95） |
| `-h`, `--help` | `-h` | 显示帮助信息 |
| `-v`, `--version` | `-v` | 显示版本信息 |

## 输出文件命名规则

提取的图片文件将按照以下格式命名：
```
PDF文件名_图片序号.扩展名
```

例如：
- `research_paper_001.jpg`
- `research_paper_002.png`
- `thesis_001.jpeg`

图片序号从001开始递增，跨页面连续编号。

## 示例工作流程

1. 准备PDF文件：
   ```bash
   # 假设有多个PDF文件
   ls *.pdf
   # document1.pdf
   # document2.pdf
   ```

2. 批量提取图片：
   ```bash
   python pdf_image_extractor.py -d ./
   ```

3. 查看提取的图片：
   ```bash
   ls *.jpg *.png *.gif
   # document1_001.jpg
   # document1_002.png
   # document2_001.jpeg
   ```

## 技术细节

- 使用 **PyMuPDF (fitz)** 库解析PDF文件并提取嵌入的图片
- 使用 **Pillow (PIL)** 库处理JPEG图片质量优化
- 支持多种图片格式：JPEG、PNG、GIF、BMP、TIFF、JP2等
- 自动创建输出目录（如果不存在）
- 提供详细的处理进度和错误报告

## 常见问题

### Q: 提取的图片质量如何？
A: 工具直接提取PDF中嵌入的原始图片数据，质量与原PDF中的图片一致。对于JPEG格式，可以指定质量参数进行优化。

### Q: 是否支持加密的PDF文件？
A: 支持，但需要提供密码。当前版本不支持密码保护的PDF。

### Q: 提取的图片尺寸是多少？
A: 图片尺寸与PDF中嵌入的原始尺寸一致，工具会显示每张图片的宽度和高度。

### Q: 是否支持矢量图形？
A: 不支持。工具仅提取位图图片，不提取矢量图形（如SVG）。

### Q: 处理大型PDF文件时内存不足？
A: 工具逐页处理PDF文件，内存占用较低。但如果PDF中包含超大图片，可能需要较多内存。

## 错误处理

- 如果PDF文件不存在或无法打开，会显示错误信息
- 如果图片提取失败，会跳过该图片并继续处理
- 如果输出目录不可写，会显示权限错误
- 所有错误都会显示详细的错误信息以便调试

## 许可证

本项目使用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交Issue和Pull Request！

## 更新日志

### v1.0 (2026-04-20)
- 初始版本发布
- 支持单个PDF文件图片提取
- 支持批量目录处理
- 支持JPEG质量调整
- 详细的进度和错误报告