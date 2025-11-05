# 🚀 快速开始

5 分钟快速上手 Gallery Generate Agent！

## 📋 前置要求

- ✅ Python 3.8+
- ✅ 4GB+ RAM

## ⚡ 三步开始

### 1️⃣ 安装

```bash
# 克隆项目
git clone https://github.com/yourusername/gallery-generate-agent.git
cd gallery-generate-agent

# 安装（开发模式）
pip install -e .

# 或只安装依赖
pip install -r requirements.txt
```

### 2️⃣ 运行

**方式一（推荐）：命令行**
```bash
gallery-generator
```

**方式二：Python 模块**
```bash
python -m gallery_generator
```

**方式三：启动脚本**
```bash
python main.py
```

### 3️⃣ 使用

1. 点击"浏览"选择图片文件夹
2. 点击"开始处理"
3. 等待完成，查看结果！

## 💡 提示

- 首次运行会下载模型（400MB），需要几分钟
- 推荐从少量图片开始测试（10-20 张）
- 查看 [完整文档](docs/USER_GUIDE.md) 了解更多

## 🔧 开发模式

如果你想修改代码：

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black src tests
```

## 🆘 遇到问题？

- [安装指南](docs/INSTALLATION.md)
- [常见问题](README.md#常见问题)
- [项目结构说明](SRC_LAYOUT_UPDATE.md)
- [提交 Issue](https://github.com/yourusername/gallery-generate-agent/issues)

---

**祝使用愉快！** 🎉
