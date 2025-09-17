# Sunmao 发布指南

本指南将帮助你将 sunmao 项目推送到 GitHub、发布到 PyPI，并设置 ReadTheDocs 文档托管。

## 1. 准备工作

### 1.1 安装必要工具

```bash
# 安装 Poetry（如果还没有）
curl -sSL https://install.python-poetry.org | python3 -

# 安装项目依赖
poetry install

# 安装额外工具
pip install twine sphinx sphinx-rtd-theme myst-parser
```

### 1.2 配置 Git

```bash
# 设置用户信息
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 2. 推送到 GitHub

### 2.1 初始化 Git 仓库

```bash
# 初始化仓库
make setup-git

# 或者手动执行
git init
git add .
git commit -m "Initial commit"
```

### 2.2 创建 GitHub 仓库

1. 访问 [GitHub](https://github.com) 并登录
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 填写仓库信息：
   - Repository name: `sunmao`
   - Description: `A flexible subplot layout library for matplotlib`
   - 选择 Public
   - 不要初始化 README、.gitignore 或 license（我们已经有了）

### 2.3 连接并推送

```bash
# 使用 GitHub CLI（推荐）
make setup-github

# 或者手动执行
git remote add origin https://github.com/seqyuan/sunmao.git
git branch -M main
git push -u origin main
```

## 3. 发布到 PyPI

### 3.1 配置 PyPI 账户

1. 访问 [PyPI](https://pypi.org) 并注册账户
2. 生成 API token：
   - 进入 Account Settings → API tokens
   - 点击 "Add API token"
   - 选择 "Create new token"
   - 设置 Scope 为 "Entire account"
   - 复制生成的 token

### 3.2 配置 Poetry

```bash
# 配置 PyPI token
poetry config pypi-token.pypi your-api-token-here
```

### 3.3 构建和发布

```bash
# 运行测试和检查
make check

# 构建包
make build

# 发布到 PyPI
make publish

# 或者使用发布脚本
python scripts/release.py
```

## 4. 设置 ReadTheDocs

### 4.1 创建 ReadTheDocs 项目

1. 访问 [ReadTheDocs](https://readthedocs.org) 并登录
2. 点击 "Import a Project"
3. 选择 "Import manually"
4. 填写项目信息：
   - Project name: `sunmao`
   - Repository URL: `https://github.com/seqyuan/sunmao`
   - Repository type: `Git`
   - Default branch: `main`
   - Configuration file: `readthedocs.yaml`

### 4.2 配置构建设置

1. 进入项目设置页面
2. 在 "Build" 标签页中：
   - Python configuration file: `readthedocs.yaml`
   - Requirements file: `docs/requirements.txt`
   - Enable "Install your project inside a virtualenv"

### 4.3 触发构建

```bash
# 推送文档更新
git add docs/
git commit -m "Add documentation"
git push origin main
```

ReadTheDocs 会自动检测到更新并开始构建。

## 5. GitHub Actions 配置

### 5.1 设置 Secrets

在 GitHub 仓库设置中添加以下 secrets：

- `PYPI_API_TOKEN`: 你的 PyPI API token

### 5.2 启用 Actions

GitHub Actions 工作流已经配置在 `.github/workflows/ci.yml` 中，会自动：

- 在每次 push 和 PR 时运行测试
- 在发布新版本时自动构建和发布到 PyPI

## 6. 发布新版本

### 6.1 使用发布脚本（推荐）

```bash
python scripts/release.py
```

脚本会引导你完成：
- 版本号更新
- 运行测试
- 构建包
- 提交和标签
- 推送到 GitHub
- 发布到 PyPI

### 6.2 手动发布

```bash
# 1. 更新版本号
# 编辑 pyproject.toml 中的 version

# 2. 运行测试
make test

# 3. 构建包
make build

# 4. 提交更改
git add pyproject.toml
git commit -m "Release version X.X.X"
git tag -a vX.X.X -m "Release version X.X.X"

# 5. 推送
git push origin main
git push origin --tags

# 6. 发布到 PyPI
make publish
```

## 7. 验证发布

### 7.1 验证 PyPI 发布

```bash
# 安装发布的包
pip install sunmao

# 测试导入
python -c "import sunmao; print(sunmao.__version__)"
```

### 7.2 验证文档

访问 https://sunmao.readthedocs.io 查看文档是否正常显示。

## 8. 常见问题

### 8.1 PyPI 发布失败

- 检查 API token 是否正确
- 确保版本号没有重复
- 检查包名是否可用

### 8.2 ReadTheDocs 构建失败

- 检查 `readthedocs.yaml` 配置
- 确保 `docs/requirements.txt` 存在
- 查看构建日志中的错误信息

### 8.3 GitHub Actions 失败

- 检查 secrets 是否正确设置
- 查看 Actions 日志中的错误信息
- 确保工作流文件语法正确

## 9. 维护

### 9.1 更新文档

```bash
# 编辑文档
vim docs/quickstart.rst

# 构建本地文档
make docs

# 查看文档
make docs-serve
# 访问 http://localhost:8000
```

### 9.2 添加新功能

1. 创建功能分支
2. 实现功能并添加测试
3. 更新文档
4. 创建 Pull Request
5. 合并后发布新版本

## 10. 参考资源

- [Poetry 文档](https://python-poetry.org/docs/)
- [PyPI 发布指南](https://packaging.python.org/tutorials/packaging-projects/)
- [ReadTheDocs 文档](https://docs.readthedocs.io/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
