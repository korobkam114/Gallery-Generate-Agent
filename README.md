# 🎨 Gallery Generate Agent

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

**基于 AI 的智能图片分类与作品集生成工具**

[特性](#-特性) • [安装](#-安装) • [使用](#-使用) • [配置](#-配置) • [贡献](#-贡献)

</div>

---

## 📖 简介

Gallery Generate Agent 是一个强大的桌面应用程序，它使用先进的 AI 模型（CLIP）自动识别和分类图片，将具有相似特征的图片归类，并生成精美的作品集。无论您是摄影师、设计师还是图片爱好者，这个工具都能帮助您快速整理和展示您的图片收藏。

### ✨ 特性

- 🤖 **智能识别**：使用 OpenAI CLIP 模型自动识别图片类别、构图和艺术特征
- 📊 **自动分类**：基于深度学习特征提取，智能聚类相似图片
- 🎯 **多种输出格式**：
  - 📄 HTML 网页（响应式设计）
  - 📑 PDF 文档（保持宽高比）
  - 📁 文件夹结构（按类别组织）
- 💻 **图形界面**：友好的 GUI，操作简单直观
- 🔧 **灵活配置**：支持自定义聚类数量、输出格式等
- 🚀 **高性能**：优化内存使用，支持批量处理大量图片
- 🛡️ **隐私保护**：完全本地运行，数据不上传

### 🎯 适用场景

- 📷 摄影师整理作品集
- 🎨 设计师分类素材库
- 🖼️ 艺术爱好者管理收藏
- 📚 图片库自动归档
- 🌍 旅行照片智能分类

---

## 🚀 快速开始

### 前置要求

- Python 3.8 或更高版本
- 4GB+ RAM（推荐 8GB）
- （可选）NVIDIA GPU 用于加速处理

### 📦 安装

1. **克隆仓库**

```bash
git clone https://github.com/yourusername/gallery-generate-agent.git
cd gallery-generate-agent
```

2. **创建虚拟环境（推荐）**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

> **注意**：首次运行时会自动下载 CLIP 模型（约 400MB），请确保网络连接正常。

---

## 💡 使用

### 启动程序

**方式一：直接运行脚本**
```bash
python main.py
```

**方式二：作为模块运行**
```bash
python -m gallery_generator
```

**方式三：安装后运行**
```bash
# 开发模式安装
pip install -e .

# 运行
gallery-generator
```

### 使用步骤

1. **选择文件夹**：点击"浏览"按钮，选择包含图片的文件夹
2. **配置参数**：
   - 设置聚类数量（或选择自动）
   - 选择输出格式（HTML/PDF/文件夹）
   - 指定输出目录（可选）
3. **开始处理**：点击"开始处理"按钮
4. **查看结果**：处理完成后，可以直接打开生成的作品集

### 示例

```
输入文件夹：
  ~/Pictures/vacation/
    - beach1.jpg
    - beach2.jpg
    - mountain1.jpg
    - city1.jpg
    ...

输出结果：
  outputs/gallery/
    ├── gallery.html        # HTML 网页作品集
    ├── gallery.pdf         # PDF 文档作品集
    └── folders/            # 分类文件夹
        ├── 海/
        ├── 山/
        └── 城市/
```

---

## ⚙️ 配置

编辑 `config.json` 文件以自定义配置：

```json
{
  "model": {
    "clip_model_name": "openai/clip-vit-base-patch32",
    "device": "auto",
    "batch_size": 32
  },
  "clustering": {
    "algorithm": "kmeans",
    "n_clusters": "auto",
    "auto_cluster_method": "elbow"
  },
  "output": {
    "default_output_dir": "outputs/gallery"
  }
}
```

### 配置选项说明

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `device` | 运行设备（`auto`/`cuda`/`cpu`） | `auto` |
| `batch_size` | 批处理大小 | `32` |
| `algorithm` | 聚类算法（`kmeans`/`dbscan`） | `kmeans` |
| `n_clusters` | 聚类数量（`auto` 或数字） | `auto` |

---

## 🛠️ 技术栈

- **GUI**: PyQt5
- **AI 模型**: CLIP (OpenAI)
- **深度学习**: PyTorch, Transformers
- **图像处理**: Pillow, OpenCV
- **聚类算法**: scikit-learn
- **模板引擎**: Jinja2
- **PDF 生成**: ReportLab

---

## 📊 项目结构

```
Gallery Generate Agent/
├── src/                        # 源代码目录
│   └── gallery_generator/      # 主包
│       ├── __init__.py
│       ├── __main__.py         # 主入口
│       ├── core/               # 核心功能
│       │   ├── image_analyzer.py
│       │   ├── feature_extractor.py
│       │   ├── classifier.py
│       │   └── gallery_generator.py
│       ├── gui/                # GUI 模块
│       │   ├── main_window.py
│       │   └── components/
│       └── models/             # AI 模型
│           └── clip_model.py
├── tests/                      # 测试目录
├── docs/                       # 文档目录
├── outputs/                    # 输出模板
│   ├── html_template.html
│   └── styles.css
├── main.py                     # 启动脚本
├── setup.py                    # 安装配置
├── pyproject.toml              # 项目配置
├── config.json                 # 运行配置
├── requirements.txt            # 依赖列表
└── README.md                   # 项目说明
```

---

## 🔍 支持的图片格式

- ✅ JPG / JPEG
- ✅ PNG
- ✅ WEBP
- ✅ BMP
- ✅ GIF

---

## ❓ 常见问题

<details>
<summary><b>首次运行为什么很慢？</b></summary>

首次运行需要下载 CLIP 模型（约 400MB），请耐心等待。模型会被缓存到本地，后续运行将直接使用缓存的模型。
</details>

<details>
<summary><b>如何提高处理速度？</b></summary>

- 使用 NVIDIA GPU（自动检测）
- 减小 batch_size 以降低内存占用
- 限制处理的图片数量
</details>

<details>
<summary><b>处理大量图片时内存不足怎么办？</b></summary>

程序已优化内存使用，默认限制最多处理 10000 张图片。您可以：
- 分批处理图片
- 增加系统内存
- 在配置中减小 batch_size
</details>

<details>
<summary><b>可以在没有网络的环境下使用吗？</b></summary>

可以！模型下载后会缓存到本地，后续使用无需网络连接。完全本地运行，保护您的隐私。
</details>

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 贡献方式

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📝 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解版本更新历史。

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🙏 致谢

- [OpenAI CLIP](https://github.com/openai/CLIP) - 强大的视觉-语言模型
- [Transformers](https://github.com/huggingface/transformers) - Hugging Face 的变换器库
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - Python GUI 框架

---

## 📧 联系

- 项目问题：[Issues](https://github.com/yourusername/gallery-generate-agent/issues)
- 功能建议：[Discussions](https://github.com/yourusername/gallery-generate-agent/discussions)

---

<div align="center">

**如果这个项目对您有帮助，请给一个 ⭐️ Star！**

Made with ❤️ by [Your Name]

</div>
