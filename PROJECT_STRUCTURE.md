# 📁 项目结构说明

本文档详细说明 Gallery Generate Agent 的项目结构和文件组织。

## 目录树

```
Gallery Generate Agent/
├── .github/                        # GitHub 配置
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md          # Bug 报告模板
│   │   └── feature_request.md     # 功能请求模板
│   └── pull_request_template.md   # PR 模板
│
├── docs/                           # 文档目录
│   ├── INSTALLATION.md            # 安装指南
│   └── USER_GUIDE.md              # 用户手册
│
├── src/                            # 源代码目录（标准 Python 结构）
│   └── gallery_generator/         # 主包
│       ├── __init__.py            # 包初始化
│       ├── __main__.py            # 主入口
│       │
│       ├── gui/                   # 图形界面模块
│       │   ├── __init__.py
│       │   ├── main_window.py     # 主窗口
│       │   └── components/        # UI 组件
│       │       ├── __init__.py
│       │       ├── folder_selector.py
│       │       ├── progress_dialog.py
│       │       └── preview_panel.py
│       │
│       ├── core/                  # 核心功能模块
│       │   ├── __init__.py
│       │   ├── image_analyzer.py  # 图片分析主类
│       │   ├── feature_extractor.py
│       │   ├── classifier.py
│       │   └── gallery_generator.py
│       │
│       └── models/                # AI 模型模块
│           ├── __init__.py
│           └── clip_model.py
│
├── tests/                          # 测试目录
│   ├── __init__.py
│   └── test_basic.py              # 基础测试
│
├── outputs/                        # 输出模板
│   ├── html_template.html         # HTML 模板
│   └── styles.css                 # CSS 样式
│
├── .gitignore                      # Git 忽略文件
├── CHANGELOG.md                    # 更新日志
├── config.json                     # 配置文件
├── CONTRIBUTING.md                 # 贡献指南
├── LICENSE                         # MIT 许可证
├── main.py                         # 启动脚本
├── MANIFEST.in                     # 打包清单
├── PROJECT_STRUCTURE.md            # 本文件
├── pyproject.toml                  # 项目配置（PEP 518）
├── README.md                       # 项目说明
├── requirements.txt                # Python 依赖
└── setup.py                        # 安装配置
```

---

## 核心模块说明

### 1. GUI 模块 (`gui/`)

#### `main_window.py`
- **功能**: 主窗口界面
- **类**: 
  - `MainWindow`: 主窗口类
  - `ProcessingThread`: 处理线程
- **职责**: 
  - 协调整个 GUI 流程
  - 管理用户交互
  - 调用核心功能

#### `components/`
- **folder_selector.py**: 文件夹选择组件
- **progress_dialog.py**: 进度显示对话框（含取消功能）
- **preview_panel.py**: 结果预览面板

### 2. 核心模块 (`core/`)

#### `image_analyzer.py`
- **功能**: 图片分析主控制器
- **主要方法**:
  - `scan_images()`: 扫描文件夹
  - `analyze_and_cluster()`: 分析和聚类
  - `generate_gallery()`: 生成作品集
  - `process_folder()`: 完整处理流程

#### `feature_extractor.py`
- **功能**: 提取图片特征
- **主要方法**:
  - `extract_image_features()`: 提取 CLIP 特征
  - `_extract_metadata()`: 提取元数据
  - `analyze_composition()`: 分析构图

#### `classifier.py`
- **功能**: 图片分类和聚类
- **主要方法**:
  - `cluster_images()`: 聚类图片
  - `_kmeans_cluster()`: KMeans 算法
  - `_dbscan_cluster()`: DBSCAN 算法
  - `_generate_cluster_names()`: 生成类别名称

#### `gallery_generator.py`
- **功能**: 生成作品集
- **主要方法**:
  - `generate_html()`: 生成 HTML 网页
  - `generate_pdf()`: 生成 PDF 文档
  - `generate_folder_structure()`: 生成文件夹结构

### 3. 模型模块 (`models/`)

#### `clip_model.py`
- **功能**: CLIP 模型封装
- **主要方法**:
  - `_load_model()`: 加载模型
  - `extract_features()`: 提取特征
  - `extract_features_from_paths()`: 从路径提取特征
  - `get_text_features()`: 提取文本特征

---

## 配置文件

### `config.json`

```json
{
  "api": {
    "openai_api_key": "",
    "google_vision_api_key": "",
    "use_online_api": false
  },
  "model": {
    "clip_model_name": "openai/clip-vit-base-patch32",
    "device": "auto",
    "batch_size": 32
  },
  "clustering": {
    "algorithm": "kmeans",
    "n_clusters": "auto",
    "auto_cluster_method": "elbow",
    "min_samples": 5
  },
  "output": {
    "html_template": "outputs/html_template.html",
    "styles": "outputs/styles.css",
    "default_output_dir": "outputs/gallery"
  },
  "supported_formats": [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"]
}
```

---

## 文档结构

### GitHub 特定文件

#### `.github/ISSUE_TEMPLATE/`
- **bug_report.md**: Bug 报告模板
- **feature_request.md**: 功能请求模板

#### `.github/pull_request_template.md`
- PR 提交模板

### 项目文档

#### `README.md`
- 项目主页
- 快速开始
- 特性介绍

#### `CONTRIBUTING.md`
- 贡献指南
- 代码规范
- PR 流程

#### `CHANGELOG.md`
- 版本历史
- 更新记录

#### `LICENSE`
- MIT 许可证

#### `docs/INSTALLATION.md`
- 详细安装步骤
- 常见问题解决

#### `docs/USER_GUIDE.md`
- 完整用户手册
- 高级用法
- 最佳实践

---

## 数据流

```
用户输入（文件夹）
    ↓
ImageAnalyzer.scan_images()
    ↓
ImageFeatureExtractor.extract_image_features()
    ↓
CLIPFeatureExtractor.extract_features_from_paths()
    ↓
ImageClassifier.cluster_images()
    ↓
GalleryGenerator.generate_all()
    ├→ generate_html()
    ├→ generate_pdf()
    └→ generate_folder_structure()
    ↓
输出（作品集文件）
```

---

## 依赖关系

```
main.py
  └── gui/main_window.py
      └── core/image_analyzer.py
          ├── core/feature_extractor.py
          │   └── models/clip_model.py
          ├── core/classifier.py
          │   └── models/clip_model.py
          └── core/gallery_generator.py
```

---

## 输出结构

### HTML 输出

```
outputs/gallery/
├── gallery.html
├── styles.css
└── images/
    ├── cluster_0_image1.jpg
    ├── cluster_0_image2.jpg
    └── ...
```

### PDF 输出

```
outputs/gallery/
└── gallery.pdf
```

### 文件夹输出

```
outputs/gallery/folders/
├── 类别1/
│   ├── image1.jpg
│   └── image2.jpg
├── 类别2/
│   └── ...
└── 类别3/
    └── ...
```

---

## 开发指南

### 添加新功能

1. **新的 GUI 组件**: 在 `gui/components/` 添加
2. **新的处理算法**: 在 `core/` 对应模块添加
3. **新的 AI 模型**: 在 `models/` 添加
4. **新的输出格式**: 在 `core/gallery_generator.py` 添加方法

### 修改现有功能

1. 找到对应的模块文件
2. 修改相应的类或方法
3. 更新文档
4. 添加测试

---

## 注意事项

### 模块化设计

- 每个模块职责单一
- 模块间低耦合
- 便于测试和维护

### 可扩展性

- 支持添加新的聚类算法
- 支持添加新的输出格式
- 支持添加新的 AI 模型

### 性能优化

- 批处理减少内存占用
- GPU 加速支持
- 多线程处理

---

## 相关链接

- [README](README.md)
- [安装指南](docs/INSTALLATION.md)
- [用户手册](docs/USER_GUIDE.md)
- [贡献指南](CONTRIBUTING.md)
- [更新日志](CHANGELOG.md)

