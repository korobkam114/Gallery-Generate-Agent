# 📁 项目结构升级：迁移到 src/ 布局

## 🎯 为什么使用 src/ 布局？

### 标准 Python 项目结构

Gallery Generate Agent 现在采用了现代 Python 项目的推荐布局 —— **src/ layout**。

### ✅ 优势

1. **避免导入冲突**
   - 防止意外导入项目目录而非安装的包
   - 确保测试使用的是安装版本，而非源代码

2. **符合最佳实践**
   - [Python Packaging Authority (PyPA)](https://packaging.python.org/) 推荐
   - 大多数现代 Python 项目的标准
   - 支持 PEP 517/518 标准

3. **更好的打包支持**
   - 简化 PyPI 发布流程
   - 支持 wheel 打包
   - 兼容 `setuptools`, `flit`, `poetry` 等工具

4. **清晰的项目组织**
   - 明确区分源代码和其他文件
   - 更容易管理测试、文档、配置

---

## 🔄 项目结构变化

### 之前（旧结构）

```
Gallery Generate Agent/
├── core/
├── gui/
├── models/
├── main.py
├── config.json
└── requirements.txt
```

### 现在（新结构）

```
Gallery Generate Agent/
├── src/
│   └── gallery_generator/      # 所有代码在这里
│       ├── core/
│       ├── gui/
│       └── models/
├── tests/                       # 测试独立目录
├── docs/                        # 文档独立目录
├── main.py                      # 简单的启动脚本
├── setup.py                     # 安装配置
├── pyproject.toml               # 项目元数据
└── requirements.txt
```

---

## 🚀 使用方式

### 1. 开发模式（推荐）

```bash
# 安装为可编辑包
pip install -e .

# 方式 1: 命令行运行
gallery-generator

# 方式 2: 作为模块运行
python -m gallery_generator

# 方式 3: 使用启动脚本
python main.py
```

### 2. 正常安装

```bash
# 安装包
pip install .

# 运行
gallery-generator
```

### 3. 从源码运行（无需安装）

```bash
# 启动脚本会自动处理路径
python main.py
```

---

## 📦 打包和发布

### 构建分发包

```bash
# 安装构建工具
pip install build

# 构建
python -m build

# 生成的文件在 dist/ 目录:
# - gallery_generate_agent-1.0.0.tar.gz
# - gallery_generate_agent-1.0.0-py3-none-any.whl
```

### 发布到 PyPI

```bash
# 安装 twine
pip install twine

# 上传到 TestPyPI（测试）
twine upload --repository testpypi dist/*

# 上传到 PyPI（正式发布）
twine upload dist/*
```

---

## 🔧 导入语句变化

### 之前

```python
from core.image_analyzer import ImageAnalyzer
from models.clip_model import CLIPFeatureExtractor
```

### 现在

```python
from gallery_generator.core.image_analyzer import ImageAnalyzer
from gallery_generator.models.clip_model import CLIPFeatureExtractor
```

或使用顶层导入：

```python
from gallery_generator import ImageAnalyzer, CLIPFeatureExtractor
```

---

## 🧪 测试

### 运行测试

```bash
# 安装测试依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 带覆盖率
pytest --cov=gallery_generator --cov-report=html
```

### 测试结构

```
tests/
├── __init__.py
├── test_basic.py           # 基础测试
├── test_core/              # 核心模块测试
├── test_gui/               # GUI 测试
└── test_models/            # 模型测试
```

---

## 📝 关键文件说明

### pyproject.toml
- **用途**: 现代 Python 项目配置文件（PEP 518）
- **包含**: 构建系统、项目元数据、工具配置
- **优势**: 统一的配置格式，替代 setup.cfg

### setup.py
- **用途**: 安装配置脚本（向后兼容）
- **功能**: 定义包信息、依赖、入口点
- **保留**: 兼容旧工具和系统

### MANIFEST.in
- **用途**: 指定要包含/排除的额外文件
- **包含**: 模板文件、文档、许可证等

### src/gallery_generator/__init__.py
- **用途**: 包初始化和顶层 API
- **导出**: 主要类和函数供外部使用

### src/gallery_generator/__main__.py
- **用途**: 支持 `python -m gallery_generator` 运行
- **入口**: main() 函数

---

## 🎓 最佳实践

### 1. 始终使用虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 2. 开发模式安装

```bash
pip install -e ".[dev]"
```

这样代码更改会立即生效，无需重新安装。

### 3. 运行测试

在提交代码前：
```bash
pytest
black src tests
flake8 src tests
```

### 4. 更新版本号

在以下位置同步更新：
- `src/gallery_generator/__init__.py` 的 `__version__`
- `setup.py` 的 `version`
- `pyproject.toml` 的 `version`
- `CHANGELOG.md` 添加变更记录

---

## 🔍 常见问题

### Q: 为什么导入失败？

**A**: 确保已安装包：
```bash
pip install -e .
```

### Q: ModuleNotFoundError: No module named 'gallery_generator'

**A**: 有两种解决方案：
1. 安装包：`pip install -e .`
2. 使用 main.py（它会自动处理路径）

### Q: 测试找不到模块？

**A**: 安装开发依赖：
```bash
pip install -e ".[dev]"
```

### Q: 如何打包发布？

**A**: 参见上面的"打包和发布"部分

---

## 📚 参考资料

- [Python Packaging User Guide](https://packaging.python.org/)
- [PEP 517 - Build System](https://peps.python.org/pep-0517/)
- [PEP 518 - Build System Requirements](https://peps.python.org/pep-0518/)
- [Setuptools Documentation](https://setuptools.pypa.io/)
- [pytest Documentation](https://docs.pytest.org/)

---

## ✨ 总结

通过采用 src/ 布局，Gallery Generate Agent 现在：

✅ 符合 Python 社区最佳实践  
✅ 支持标准的打包和发布流程  
✅ 更容易进行测试和质量控制  
✅ 可以发布到 PyPI  
✅ 更专业和可维护  

这是一个重要的项目升级，为未来的发展奠定了坚实基础！

