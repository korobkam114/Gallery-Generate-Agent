# 📦 详细安装指南

本文档提供 Gallery Generate Agent 的详细安装步骤和常见问题解决方案。

## 目录

- [系统要求](#系统要求)
- [安装步骤](#安装步骤)
- [验证安装](#验证安装)
- [常见问题](#常见问题)
- [卸载](#卸载)

---

## 系统要求

### 硬件要求

**最低配置**
- CPU: 双核处理器
- RAM: 4GB
- 硬盘: 2GB 可用空间

**推荐配置**
- CPU: 四核或更高
- RAM: 8GB 或更高
- GPU: NVIDIA GPU（可选，用于加速）
- 硬盘: 5GB 可用空间

### 软件要求

- **操作系统**: Windows 10+, macOS 10.14+, 或 Linux
- **Python**: 3.8 或更高版本
- **pip**: 最新版本

---

## 安装步骤

### 1. 安装 Python

#### Windows

1. 访问 [Python 官网](https://www.python.org/downloads/)
2. 下载 Python 3.8+ 安装程序
3. 运行安装程序，**勾选 "Add Python to PATH"**
4. 验证安装：
   ```cmd
   python --version
   ```

#### macOS

使用 Homebrew：
```bash
brew install python@3.9
```

或者从 [Python 官网](https://www.python.org/downloads/macos/) 下载安装程序。

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.9 python3-pip python3-venv
```

### 2. 克隆仓库

```bash
git clone https://github.com/yourusername/gallery-generate-agent.git
cd gallery-generate-agent
```

或者直接下载 ZIP 文件并解压。

### 3. 创建虚拟环境（推荐）

#### Windows

```cmd
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. 安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**注意**: 安装可能需要几分钟，请耐心等待。

### 5. GPU 支持（可选）

如果您有 NVIDIA GPU 并希望加速处理：

#### 安装 CUDA

1. 访问 [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
2. 下载并安装适合您系统的 CUDA 版本
3. 验证安装：
   ```bash
   nvidia-smi
   ```

#### 安装 PyTorch GPU 版本

```bash
# 卸载 CPU 版本
pip uninstall torch

# 安装 GPU 版本（根据您的 CUDA 版本选择）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## 验证安装

### 检查依赖

```bash
python -c "import PyQt5; import torch; import transformers; print('All dependencies OK')"
```

### 运行程序

```bash
python main.py
```

如果看到 GUI 窗口，说明安装成功！

---

## 常见问题

### 问题 1: `pip install` 失败

**错误信息**:
```
ERROR: Could not find a version that satisfies the requirement...
```

**解决方案**:
```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像源（如果在中国）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 2: PyQt5 安装失败

**Windows 解决方案**:
```cmd
# 安装 Visual C++ 构建工具
# 下载：https://visualstudio.microsoft.com/visual-cpp-build-tools/

# 或使用预编译版本
pip install PyQt5 --prefer-binary
```

**Linux 解决方案**:
```bash
# 安装系统依赖
sudo apt-get install python3-pyqt5
```

### 问题 3: 模型下载失败

**错误信息**:
```
Cannot download model files
```

**解决方案**:

1. **检查网络连接**
2. **配置代理**（如果需要）:
   ```bash
   export HTTP_PROXY=http://your-proxy:port
   export HTTPS_PROXY=http://your-proxy:port
   ```
3. **手动下载模型**:
   - 访问 [Hugging Face](https://huggingface.co/openai/clip-vit-base-patch32)
   - 下载所有文件到 `~/.cache/huggingface/hub/`

### 问题 4: CUDA 不可用

**检查 CUDA**:
```python
import torch
print(torch.cuda.is_available())  # 应该返回 True
```

**如果返回 False**:
1. 确认安装了 NVIDIA GPU
2. 安装正确版本的 CUDA Toolkit
3. 重新安装 PyTorch GPU 版本

### 问题 5: 内存不足

**解决方案**:
- 在 `config.json` 中减小 `batch_size`
- 关闭其他占用内存的程序
- 分批处理图片

---

## 更新

### 更新到最新版本

```bash
# 进入项目目录
cd gallery-generate-agent

# 拉取最新代码
git pull

# 更新依赖
pip install -r requirements.txt --upgrade
```

---

## 卸载

### 1. 删除虚拟环境

```bash
# 退出虚拟环境
deactivate

# 删除虚拟环境文件夹
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows
```

### 2. 删除项目文件

```bash
cd ..
rm -rf gallery-generate-agent  # Linux/macOS
rmdir /s gallery-generate-agent  # Windows
```

### 3. 清理缓存（可选）

删除下载的模型缓存：

```bash
# Linux/macOS
rm -rf ~/.cache/huggingface

# Windows
rmdir /s %USERPROFILE%\.cache\huggingface
```

---

## 需要帮助？

如果遇到其他问题，请：

1. 查看 [常见问题](../README.md#常见问题)
2. 搜索 [已有 Issues](https://github.com/yourusername/gallery-generate-agent/issues)
3. 创建新的 [Issue](https://github.com/yourusername/gallery-generate-agent/issues/new)
4. 加入我们的 [讨论区](https://github.com/yourusername/gallery-generate-agent/discussions)

