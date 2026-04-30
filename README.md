# GPT 图片生成工具（Python + Vue3 本地版）
基于 FastAPI + Vue3 的本地图片生成工具，完美解决跨域问题，所有数据存储在浏览器本地，功能完全对齐原纯前端版本。

## 技术栈
### 前端
- Vue 3.4 + TypeScript
- Pinia 状态管理
- Element Plus UI 组件库
- Tailwind CSS
- Vite 构建工具

### 后端
- FastAPI
- Uvicorn ASGI 服务器
- Pydantic 数据验证
- Requests 请求转发

## 快速开始
### 1. 启动后端
```bash
cd backend
# 建议使用虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip3 install -r requirements.txt

# 启动服务
python3 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
后端接口文档：http://127.0.0.1:8000/docs

### 2. 启动前端
```bash
cd frontend
npm install
npm run dev
```
前端访问地址：http://localhost:5174

### 3. Docker 一键启动
```bash
docker-compose up -d
```
访问：http://localhost:5174

## 功能特性
- ✅ 文本生成图片
- ✅ 参考图编辑图片
- ✅ 自定义 API 地址和接口路径
- ✅ 本地 IndexedDB 存储任务记录和图片
- ✅ 任务历史管理
- ✅ 批量导出/导入任务
- ✅ 无跨域问题，本地运行安全

## 配置说明
所有配置都可以在前端设置页面填写，不需要修改后端代码，后端仅做请求转发，不存储任何数据。

### 后端环境配置
复制 `.env.example` 为 `.env` 可自定义后端配置：
```bash
cd backend
cp .env.example .env
```
支持配置：
- `DEFAULT_API_BASE_URL`：默认API基础地址
- `DEFAULT_API_KEY`：默认API密钥
- `REQUEST_TIMEOUT`：请求超时时间（秒）

## 常见问题
### 1. 后端启动报错 `uvicorn: command not found`
使用完整命令启动：
```bash
python3 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 2. 后端启动报错 `SyntaxError: non-default argument follows default argument`
代码已修复，直接拉取最新版本即可正常运行。

### 3. 前端页面空白
- 确保后端服务已正常启动在 8000 端口
- 按 `Cmd+Shift+R` 强制刷新浏览器清除缓存
- 确认访问地址为 http://localhost:5174

### 4. 接口请求404
后端路由已统一为 `/api` 前缀，无需额外配置，前端代理已默认设置。
