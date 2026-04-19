# Git 与 GitHub 关系及服务器配置指南

## 1. Git 与 GitHub 的关系

### Git
- **分布式版本控制系统**：用于跟踪文件变更，支持多人协作开发
- **本地操作**：所有版本历史都存储在本地仓库中
- **核心功能**：提交(commit)、分支(branch)、合并(merge)、克隆(clone)等

### GitHub
- **基于 Git 的远程仓库托管平台**：提供云端存储和协作功能
- **集中式服务**：作为远程仓库中心，方便团队协作
- **附加功能**：Pull Request、Issues、Projects、Actions CI/CD 等

### 关系总结
- **Git 是工具**：版本控制的核心系统
- **GitHub 是平台**：基于 Git 的云端协作服务平台
- **类比**：Git 相当于 "本地文件系统"，GitHub 相当于 "云盘服务"

## 2. 当前服务器 Git 状态检查

### 2.1 Git 安装状态
- Git 已安装：版本 2.34.1
- 检查命令：`git --version`

### 2.2 Git 配置状态
- 基本配置存在，但未设置用户信息
- 检查命令：`git config --list`
- 当前配置：
  ```
  core.repositoryformatversion=0
  core.filemode=true
  core.bare=false
  core.logallrefupdates=true
  ```

### 2.3 SSH 密钥状态
- ~/.ssh 目录不存在，未配置 SSH 密钥
- 检查命令：`ls -la ~/.ssh/`

## 3. 服务器 Git 配置步骤

### 3.1 基础配置
```bash
# 设置全局用户名
git config --global user.name "你的用户名"

# 设置全局邮箱
git config --global user.email "你的邮箱@example.com"

# 验证配置
git config --list
```

### 3.2 SSH 密钥配置（推荐）

#### 1. 生成 SSH 密钥
```bash
ssh-keygen -t ed25519 -C "你的邮箱@example.com"
# 或使用 RSA
ssh-keygen -t rsa -b 4096 -C "你的邮箱@example.com"
```

#### 2. 查看公钥
```bash
cat ~/.ssh/id_ed25519.pub
# 或
cat ~/.ssh/id_rsa.pub
```

#### 3. 添加公钥到 GitHub
1. 登录 GitHub
    - 访问 GitHub
    - 点击右上角头像 → Settings
  2. 进入 SSH 设置页面
    - 左侧边栏点击 SSH and GPG keys
    - 点击绿色按钮 New SSH key
  3. 添加公钥
    - Title：填写一个描述性名称（如 "My Server"）
    - Key type：选择 "Authentication Key"
    - Key：粘贴上面的公钥内容（从 ssh-ed25519 到 gmail.com
   整行）
  4. 保存
    - 点击 Add SSH key 按钮
    
#### 4. 测试连接
```bash
ssh -T git@github.com
```

### 3.3 HTTPS 配置（备选）
```bash
# 使用个人访问令牌(PAT)代替密码
git config --global credential.helper store
# 首次推送时需要输入用户名和 PAT
```

## 4. 基本 Git 与 GitHub 工作流程

### 4.1 克隆远程仓库
```bash
git clone git@github.com:用户名/仓库名.git
# 或使用 HTTPS
git clone https://github.com/用户名/仓库名.git
```

### 4.2 本地开发流程
```bash
# 创建新分支
git checkout -b feature-branch

# 添加文件到暂存区
git add .

# 提交变更
git commit -m "提交说明"

# 推送到远程
git push origin feature-branch
```

### 4.3 协作流程
1. **Fork**：复制他人仓库到自己的 GitHub 账户
2. **Clone**：克隆到本地
3. **开发**：在自己的分支上开发
4. **Pull Request**：向原仓库提交合并请求
5. **Code Review**：代码审查
6. **Merge**：合并到主分支

## 5. 常用命令速查

### 本地操作
```bash
git init                    # 初始化仓库
git status                  # 查看状态
git add <file>              # 添加文件到暂存区
git commit -m "message"     # 提交
git log                     # 查看提交历史
git diff                    # 查看差异
```

### 分支操作
```bash
git branch                  # 查看分支
git checkout <branch>       # 切换分支
git merge <branch>          # 合并分支
git branch -d <branch>      # 删除分支
```

### 远程操作
```bash
git remote add origin <url> # 添加远程仓库
git push origin <branch>    # 推送到远程
git pull origin <branch>    # 从远程拉取
git fetch                   # 获取远程更新
```

## 6. 故障排除

### SSH 连接问题
```bash
# 检查 SSH 代理
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 测试连接详细日志
ssh -Tv git@github.com
```

### 权限问题
- 确保公钥已正确添加到 GitHub
- 检查仓库访问权限
- 使用 `git remote -v` 确认远程地址

### 配置重置
```bash
# 重置配置
git config --global --unset user.name
git config --global --unset user.email
```

## 7. 最佳实践建议

1. **分支策略**：使用主分支(main/master) + 功能分支(feature branches)
2. **提交规范**：使用清晰的提交信息，遵循 Conventional Commits
3. **频繁提交**：小步提交，便于回滚和代码审查
4. **定期同步**：经常拉取远程更新，避免冲突
5. **保护主分支**：使用 Pull Request 和代码审查机制

## 8. 参考资料

- [Git 官方文档](https://git-scm.com/doc)
- [GitHub 文档](https://docs.github.com/)
- [Pro Git 书籍](https://git-scm.com/book/)

---

*文档生成时间：2026-04-19*  
*当前服务器：Linux 5.15.0-173-generic*  
*Git 版本：2.34.1*