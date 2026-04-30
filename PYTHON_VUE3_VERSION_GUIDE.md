# Python + Vue3 版 GPT 图片生成工具开发指南（本地部署极简版）
基于原 React 纯前端项目的功能，实现前后端分离版本，仅用于本地部署使用，后端仅做请求转发解决跨域问题，所有数据仍存储在用户浏览器本地，功能完全对齐原项目，无额外扩展。

---

## 一、选型说明
### 1.1 前端选型（Vue3 生态）
| 技术 | 版本 | 选型理由 | 对应原项目技术 |
|------|------|----------|----------------|
| Vue3 | ^3.4.0 | 目前最主流的 Vue 版本，组合式 API 开发体验好 | React 19 |
| TypeScript | ^5.3.0 | 类型约束，减少错误，和原项目保持一致的类型安全 | TypeScript |
| Vite | ^5.0.0 | 构建速度快，开发体验好 | Vite |
| Pinia | ^2.1.0 | Vue3 官方推荐状态管理，轻量易用，对应原项目的 Zustand | Zustand |
| Element Plus | ^2.5.0 | 成熟的 Vue3 UI 组件库，快速搭建界面，减少自定义组件开发量 | 自定义 Tailwind 组件 |
| Tailwind CSS | ^3.4.0 | 和原项目保持一致的样式方案，快速实现自定义 UI | Tailwind CSS |
| Axios | ^1.6.0 |  HTTP 请求库，封装 API 请求 | 原生 fetch |
| localforage | ^1.10.0 | 浏览器端 IndexedDB 封装，实现本地存储，和原项目保持一致的本地存储能力 | 原生 IndexedDB |
| fflate | ^0.8.0 | 和原项目保持一致，实现 ZIP 导入导出 | fflate |

### 1.2 后端选型（Python 生态）
| 技术 | 版本 | 选型理由 |
|------|------|----------|
| FastAPI | ^0.109.0 | 轻量高性能，自动生成接口文档，开发简单 |
| Uvicorn | ^0.27.0 | ASGI 服务器，运行 FastAPI 应用 |
| Pydantic | ^2.5.0 | 数据验证，和前端类型自动对齐 |
| requests | ^2.31.0 | 转发请求到第三方 AI 接口 |
| python-multipart | ^0.0.6 | 处理参考图文件上传 |
| python-dotenv | ^1.0.0 | 环境变量配置，存储默认API密钥（可选） |

---

## 二、系统架构设计
### 2.1 整体架构
```
┌─────────────────┐    HTTP请求    ┌─────────────────┐    转发请求    ┌─────────────────┐
│   Vue3 前端     │ ◄────────────► │  FastAPI 后端   │ ◄────────────► │  第三方AI接口   │
│  (浏览器运行)   │                │  (本地运行)     │                │ (OpenAI/自定义) │
└─────────────────┘                └─────────────────┘                └─────────────────┘
          │
          ▼
┌─────────────────┐
│ IndexedDB 存储  │
│ (浏览器本地)    │
└─────────────────┘
```
> 后端仅做请求转发，不存储任何数据，所有任务记录、图片、配置都存储在用户浏览器本地，和原纯前端项目逻辑完全一致，仅解决跨域问题和API密钥安全问题。

### 2.2 数据流
```
用户输入提示词/上传参考图 + 选择接口路径 → 前端组装参数 → 发送请求到后端 → 后端转发请求到用户指定的AI接口（携带API密钥） → 后端接收AI接口返回 → 后端返回结果给前端 → 前端存储到本地IndexedDB → 前端展示结果
```

---

## 三、项目结构设计
### 3.1 完整项目目录
```
gpt-image-playground-py-vue/
├── frontend/                # Vue3 前端项目
├── backend/                 # FastAPI 后端项目
├── docker-compose.yml       # 一键部署配置
└── README.md                # 项目说明
```

### 3.2 前端目录结构（和原项目对齐）
```
frontend/
├── public/                  # 静态资源
├── src/
│   ├── components/          # UI组件（和原项目组件一一对应）
│   │   ├── Header.vue
│   │   ├── InputBar.vue
│   │   ├── TaskGrid.vue
│   │   ├── TaskCard.vue
│   │   ├── SettingsModal.vue
│   │   ├── SizePickerModal.vue
│   │   └── ... 其他组件
│   ├── stores/              # Pinia 状态管理
│   │   ├── app.ts           # 全局状态，对应原项目store.ts
│   │   └── settings.ts      # 设置状态
│   ├── api/                 # API 请求封装
│   │   └── index.ts         # 请求后端接口
│   ├── types/               # 全局类型定义，完全复用原项目types.ts
│   │   └── index.ts
│   ├── utils/               # 工具函数
│   │   ├── db.ts            # IndexedDB操作，复用原项目db.ts
│   │   ├── size.ts          # 尺寸计算，复用原项目size.ts
│   │   └── zip.ts           # ZIP导入导出，复用原项目逻辑
│   ├── App.vue
│   ├── main.ts
│   └── style.css
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

### 3.3 后端目录结构
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置文件（环境变量读取）
│   ├── schemas.py           # Pydantic 模型，和前端类型一一对应
│   ├── routes/              # 接口路由
│   │   ├── images.py        # 图片生成/编辑相关接口
│   │   └── health.py        # 健康检查接口
│   ├── services/            # 业务逻辑
│   │   └── ai_client.py     # 调用第三方AI接口的封装
│   └── models/              # 可选：数据库模型（使用SQLAlchemy时需要）
├── .env.example             # 环境变量示例
├── requirements.txt         # Python 依赖
└── Dockerfile               # 后端Docker构建文件
```

---

## 四、核心功能实现说明
### 4.1 类型对齐（前后端一致）
完全复用原项目的TypeScript类型，仅新增接口路径相关字段：

**前端types.ts（在原AppSettings基础上新增）：**
```typescript
export interface AppSettings {
  baseUrl: string
  apiKey: string
  model: string
  // 新增：接口路径下拉选项值
  generationPath: 'v1/images/generations' | string // 支持默认值和自定义路径
  editPath: 'v1/images/edits' | string // 支持默认值和自定义路径
  timeout: number
}

export interface TaskParams {
  size: string
  quality: 'auto' | 'low' | 'medium' | 'high'
  output_format: 'png' | 'jpeg' | 'webp'
  output_compression: number | null
  moderation: 'auto' | 'low'
  n: number
}
```

**后端schemas.py（对应上面的类型）：**
```python
from pydantic import BaseModel
from typing import Optional, List, Literal

class TaskParams(BaseModel):
    size: str
    quality: Literal['auto', 'low', 'medium', 'high']
    output_format: Literal['png', 'jpeg', 'webp']
    output_compression: Optional[int] = None
    moderation: Literal['auto', 'low']
    n: int = 1

class ImageGenerationRequest(BaseModel):
    prompt: str
    params: TaskParams
    input_images: Optional[List[str]] = None  # base64格式的参考图，或者文件ID
```

### 4.2 后端核心接口设计
#### 4.2.1 文本生成图片接口
```http
POST /api/v1/images/generate
Content-Type: application/json

请求体：
{
  "prompt": "一只可爱的猫咪",
  "params": {
    "size": "1024x1024",
    "quality": "high",
    "output_format": "png",
    "moderation": "auto",
    "n": 1
  },
  "api_base_url": "https://api.openai.com", // 前端传的API基础地址
  "api_path": "v1/images/generations", // 前端传的接口路径，可自定义
  "api_key": "sk-xxxx" // 前端传的API密钥，也可配置在后端环境变量
}

响应：
{
  "code": 0,
  "message": "success",
  "data": {
    "images": [
      "base64://xxx..."
    ]
  }
}
```

#### 4.2.2 图片编辑接口
```http
POST /api/v1/images/edit
Content-Type: multipart/form-data

字段：
- prompt: 字符串
- params: JSON字符串，序列化后的TaskParams
- api_base_url: 字符串，API基础地址
- api_path: 字符串，接口路径，可自定义
- api_key: 字符串，API密钥
- images: 多个文件字段，参考图

响应：
{
  "code": 0,
  "message": "success",
  "data": {
    "images": [
      "base64://xxx..."
    ]
  }
}
```

#### 4.2.3 后端请求转发实现示例（核心逻辑）
```python
# app/services/ai_client.py
import requests
from typing import List, Optional
from app.schemas import TaskParams

class AIClient:
    def __init__(self, timeout: int = 300):
        self.timeout = timeout

    def generate_image(
        self, 
        prompt: str, 
        params: TaskParams,
        api_base_url: str,
        api_path: str,
        api_key: str,
        model: str = "gpt-image-2"
    ) -> List[str]:
        """调用文本生图接口，参数全部由前端传入"""
        # 拼接完整请求地址
        if api_path.startswith(("http://", "https://")):
            url = api_path
        else:
            url = f"{api_base_url.rstrip('/')}/{api_path.lstrip('/')}"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "model": model,
            "prompt": prompt,
            "size": params.size,
            "quality": params.quality,
            "output_format": params.output_format,
            "moderation": params.moderation,
            "n": params.n
        }
        if params.output_format != "png" and params.output_compression:
            body["output_compression"] = params.output_compression

        response = requests.post(url, headers=headers, json=body, timeout=self.timeout)
        response.raise_for_status()
        result = response.json()
        return [item.get("b64_json") or item.get("url") for item in result["data"]]

    def edit_image(
        self, 
        prompt: str, 
        params: TaskParams,
        api_base_url: str,
        api_path: str,
        api_key: str,
        image_files: List,
        model: str = "gpt-image-2"
    ) -> List[str]:
        """调用图片编辑接口，参数全部由前端传入"""
        # 拼接完整请求地址
        if api_path.startswith(("http://", "https://")):
            url = api_path
        else:
            url = f"{api_base_url.rstrip('/')}/{api_path.lstrip('/')}"
        
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        form_data = {
            "model": model,
            "prompt": prompt,
            "size": params.size,
            "quality": params.quality,
            "output_format": params.output_format,
            "moderation": params.moderation
        }
        if params.output_format != "png" and params.output_compression:
            form_data["output_compression"] = str(params.output_compression)

        files = [("image", (f"input_{i}.png", img.file, img.content_type)) for i, img in enumerate(image_files)]
        response = requests.post(url, headers=headers, data=form_data, files=files, timeout=self.timeout)
        response.raise_for_status()
        result = response.json()
        return [item.get("b64_json") or item.get("url") for item in result["data"]]
```

### 4.3 前端修改说明
和原项目相比，只需要修改两处：请求路径改为后端接口，设置页面增加接口路径下拉选择：
1. 把原项目`src/lib/api.ts`里的直接请求第三方接口，改成请求自己的后端接口
2. 在设置弹窗里新增接口路径下拉选择（支持选默认值和自定义输入）
3. 解决了浏览器跨域问题，不需要用户配置CORS

#### 4.3.1 设置页面新增接口路径下拉选择
在原有的SettingsModal.vue组件里添加两个下拉选择框：
```vue
<!-- 文本生图接口选择 -->
<el-form-item label="文本生图接口">
  <el-select v-model="settings.generationPath" allow-create>
    <el-option label="默认接口" value="v1/images/generations" />
    <!-- 可扩展更多预设接口 -->
  </el-select>
  <span class="text-xs text-gray-500">支持输入自定义完整URL</span>
</el-form-item>

<!-- 图片编辑接口选择 -->
<el-form-item label="图片编辑接口">
  <el-select v-model="settings.editPath" allow-create>
    <el-option label="默认接口" value="v1/images/edits" />
    <!-- 可扩展更多预设接口 -->
  </el-select>
  <span class="text-xs text-gray-500">支持输入自定义完整URL</span>
</el-form-item>
```
> 用Element Plus的el-select组件，开启allow-create即可支持用户自定义输入任意接口路径。

#### 4.3.2 API请求修改示例
```typescript
// src/api/index.ts
import axios from 'axios'
import type { TaskParams, AppSettings } from '../types'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 300000
})

// 文本生图
export async function generateImage(
  prompt: string, 
  params: TaskParams, 
  settings: AppSettings
) {
  const res = await api.post('/images/generate', { 
    prompt, 
    params,
    api_base_url: settings.baseUrl,
    api_path: settings.generationPath,
    api_key: settings.apiKey,
    model: settings.model
  })
  return res.data.data
}

// 图片编辑
export async function editImage(
  prompt: string, 
  params: TaskParams, 
  settings: AppSettings,
  files: File[]
) {
  const formData = new FormData()
  formData.append('prompt', prompt)
  formData.append('params', JSON.stringify(params))
  formData.append('api_base_url', settings.baseUrl)
  formData.append('api_path', settings.editPath)
  formData.append('api_key', settings.apiKey)
  formData.append('model', settings.model)
  files.forEach((file, index) => {
    formData.append(`images`, file, `input_${index}.png`)
  })
  const res = await api.post('/images/edit', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return res.data.data
}
```

### 4.4 其他功能复用说明
- 所有UI组件逻辑和原项目完全一样，只是把JSX改成Vue的SFC格式
- 尺寸计算、本地存储、ZIP导入导出等工具逻辑完全复用原项目代码
- 状态管理逻辑和原项目一致，只是把Zustand改成Pinia的写法

---

## 五、本地部署快速开始
### 5.1 环境准备
- Node.js >= 18.0.0
- Python >= 3.10
- 仅本地使用，不需要公网部署

### 5.2 后端启动
```bash
# 进入后端目录
cd backend

# 安装依赖
pip install fastapi uvicorn pydantic requests python-multipart python-dotenv

# 启动服务（无需配置环境变量，所有参数前端传入）
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
后端启动后访问 http://127.0.0.1:8000/docs 可以看到自动生成的接口文档。

### 5.3 前端启动
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 配置Vite代理，转发/api请求到后端
// vite.config.ts中添加：
server: {
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true
    }
  }
}

# 启动开发服务器
npm run dev
```
前端启动后访问 http://localhost:5173 即可使用，所有配置（API地址、密钥、接口路径）都在前端设置页面填写即可。

### 5.4 本地长期使用
- 前端执行`npm run build`构建静态文件，用Nginx或任意静态文件服务托管
- 后端可以配置成系统服务开机自启，或者用nohup后台运行：`nohup uvicorn app.main:app --host 127.0.0.1 --port 8000 &`

---

## 六、和原纯前端版本对比
| 特性 | 原React纯前端版本 | 当前Python+Vue3本地版 |
|------|-------------------|-----------------|
| 部署难度 | 简单，纯静态 | 简单，本地启动两个服务即可 |
| API密钥安全性 | 存在浏览器内存中 | 前端传入后端使用，不会永久存储更安全 |
| 跨域问题 | 需要用户自己解决CORS或使用代理 | 无跨域问题，后端转发 |
| 数据存储 | 仅浏览器本地 | 和原版本一致，仅浏览器本地 |
| 自定义接口路径 | 支持 | 支持，下拉选择+自定义输入 |
| 功能 | 完全一致 | 完全对齐原项目所有功能 |

> 本版本适合本地个人使用，完美解决原版本的跨域问题，功能和使用体验和原项目完全一致，没有任何功能缩减。