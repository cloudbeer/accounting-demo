# Todo List 应用

这是一个使用现代技术栈构建的待办事项管理应用。

## 技术栈

### 后端
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

### 前端
- Vue.js 3
- TypeScript
- Vite

## 项目结构

```
.
├── backend/           # 后端项目目录
│   ├── app/          # 应用主目录
│   │   ├── crud/     # 数据库操作
│   │   ├── models/   # 数据库模型
│   │   └── schemas/  # Pydantic 模型
│   └── run.py        # 应用入口
└── frontend/         # 前端项目目录
    ├── src/          # 源代码目录
    │   ├── views/    # 页面组件
    │   ├── types/    # TypeScript 类型定义
    │   └── services/ # API 服务
    └── public/       # 静态资源
```

## 开始使用

### 后端设置

1. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate  # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 启动服务器：
```bash
cd backend
python run.py
```

### 前端设置

1. 安装依赖：
```bash
cd frontend
npm install
```

2. 启动开发服务器：
```bash
npm run dev
```

## 贡献指南

欢迎提交 Pull Request 和 Issue。在提交之前，请确保：

1. 代码符合项目的编码规范
2. 所有测试都已通过
3. 提交信息清晰明了

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。