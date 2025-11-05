# 更新日志

所有重要的项目更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 计划功能
- [ ] 支持视频文件预览
- [ ] 添加批量编辑功能
- [ ] 支持更多输出格式
- [ ] 多语言界面支持

---

## [1.0.0] - 2025-01-XX

### 🎉 首次发布

#### Added
- ✨ 基于 CLIP 模型的智能图片识别
- 📊 自动聚类分类功能（KMeans/DBSCAN）
- 🎨 三种输出格式（HTML/PDF/文件夹）
- 💻 友好的 PyQt5 图形界面
- ⚙️ 灵活的配置选项
- 📝 完整的项目文档

#### Features
- 支持批量处理大量图片（最多 10000 张）
- 内存优化，分批处理避免溢出
- 进度实时显示
- 支持取消长时间任务
- 首次运行友好提示
- PDF 输出保持图片宽高比
- 响应式 HTML 模板
- 按类别自动生成文件夹结构

#### Technical
- Python 3.8+ 支持
- GPU 加速（可选）
- 完全本地运行，保护隐私
- 跨平台支持（Windows/macOS/Linux）

---

## 版本说明

### [1.0.0] - 初始版本

这是 Gallery Generate Agent 的首个正式版本，包含所有核心功能：

**核心能力**
- 使用 OpenAI CLIP 模型进行图片特征提取
- 智能聚类算法自动分类
- 多格式输出支持

**用户体验**
- 简洁直观的图形界面
- 实时进度反馈
- 可取消长时间任务
- 友好的错误提示

**性能优化**
- 批处理优化内存使用
- GPU 自动加速
- 大数据集支持（10000+ 图片）

**质量保证**
- 线程安全设计
- 完善的错误处理
- 详细的日志输出

---

## 贡献指南

查看更多更新和贡献信息，请访问：
- [项目主页](https://github.com/yourusername/gallery-generate-agent)
- [问题反馈](https://github.com/yourusername/gallery-generate-agent/issues)
- [功能建议](https://github.com/yourusername/gallery-generate-agent/discussions)

