# 贡献指南

感谢您考虑为 Gallery Generate Agent 做出贡献！

## 🌟 如何贡献

### 报告 Bug

如果您发现了 bug，请：

1. 确认该 bug 尚未在 [Issues](https://github.com/yourusername/gallery-generate-agent/issues) 中报告
2. 创建一个新的 Issue，包含：
   - 清晰的标题和描述
   - 重现步骤
   - 预期行为 vs 实际行为
   - 屏幕截图（如适用）
   - 环境信息（操作系统、Python 版本等）

### 建议新功能

我们欢迎新功能建议！请：

1. 先在 [Discussions](https://github.com/yourusername/gallery-generate-agent/discussions) 中讨论
2. 如果获得积极反馈，创建一个 Feature Request Issue
3. 清楚说明功能的用途和价值

### 提交代码

1. **Fork 仓库**

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **编写代码**
   - 遵循现有代码风格
   - 添加必要的注释
   - 更新文档（如需要）

4. **测试**
   - 确保现有测试通过
   - 为新功能添加测试

5. **提交更改**
   ```bash
   git add .
   git commit -m "Add: your feature description"
   ```

   提交消息格式：
   - `Add:` 新功能
   - `Fix:` Bug 修复
   - `Update:` 更新
   - `Refactor:` 重构
   - `Docs:` 文档更新

6. **推送并创建 PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 代码规范

### Python 代码风格

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- 使用 4 个空格缩进
- 最大行长度 100 字符
- 使用类型注解（Type Hints）

### 命名约定

- 类名：`PascalCase`
- 函数/方法：`snake_case`
- 常量：`UPPER_CASE`
- 私有成员：`_leading_underscore`

### 文档字符串

```python
def example_function(param1: str, param2: int) -> bool:
    """
    简短描述函数功能
    
    Args:
        param1: 参数1的描述
        param2: 参数2的描述
        
    Returns:
        返回值描述
        
    Raises:
        Exception: 异常情况描述
    """
    pass
```

## 🧪 测试

在提交 PR 前，请确保：

- [ ] 代码通过 linting 检查
- [ ] 所有现有测试通过
- [ ] 新功能有相应的测试
- [ ] 文档已更新

运行测试：
```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
pytest tests/

# 代码风格检查
flake8 .
black --check .
```

## 📋 Pull Request 检查清单

- [ ] 代码遵循项目风格指南
- [ ] 自测通过所有功能
- [ ] 添加/更新了相关文档
- [ ] 添加/更新了测试用例
- [ ] 提交消息清晰明确
- [ ] PR 描述详细说明了更改内容

## 🤔 需要帮助？

- 查看 [文档](README.md)
- 在 [Discussions](https://github.com/yourusername/gallery-generate-agent/discussions) 提问
- 查看现有的 [Issues](https://github.com/yourusername/gallery-generate-agent/issues)

## 📜 行为准则

### 我们的承诺

为了营造开放和友好的环境，我们承诺：

- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

### 不可接受的行为

- 使用性化的语言或图像
- 发表侮辱性/贬损性评论
- 公开或私下骚扰
- 未经许可发布他人的私人信息
- 其他不道德或不专业的行为

## 🎉 贡献者

感谢所有贡献者的付出！

<!-- ALL-CONTRIBUTORS-LIST:START -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

---

再次感谢您的贡献！ 🙌

