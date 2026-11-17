# 洪城漫游 · 南昌旅游自定义路线地图工具

> 中期可演示版本：主流程已跑通（地图浏览 → 筛选 → 点位详情 → 添加待选清单 → 生成路线 → 查看路线）。
> 本说明介绍项目环境、启动步骤与常见问题，按步骤操作即可在本地运行。

## 一、项目简介

洪城漫游是一款面向南昌城市短途旅游的轻量化路线规划工具，采用前后端分离架构，浏览器直接访问，免安装、免登录。核心链路为：

```
地图浏览选点 → 一键生成路线 → 路线管理
```

点位分 4 类，以不同颜色与图标区分：

| 类型 | 标识 | 颜色 | 能否加入路线 |
| --- | --- | --- | --- |
| 景点 spot | 星标 | 蓝 | 可以 |
| 正餐美食 food | 餐具 | 橙 | 可以 |
| 休闲市集小店 leisure | 购物袋 | 绿 | 可以 |
| 配套服务 facility | 信息 i | 灰 | 仅可浏览，不能加入 |

中期版本使用自制模拟地图，数据库默认使用 SQLite，无需额外安装数据库服务。

## 二、技术栈

- 前端：Vue 3 + Vite 5 + Vue Router（手写 CSS，不引入重型组件库）
- 后端：Python + FastAPI + Uvicorn + SQLAlchemy + Pydantic
- 数据库：SQLite（默认）/ MySQL（保留配置，可切换）
- 地图：中期为模拟地图；后续接入高德地图 JS API（需 Key）

## 三、环境要求

| 软件 | 版本要求 | 说明 |
| --- | --- | --- |
| Node.js | 18 及以上（开发环境为 v22） | 含 npm |
| Python | 3.10 及以上（开发环境为 3.13） | 建议使用虚拟环境 |
| 浏览器 | Edge / Chrome / Safari / Firefox 近两年版本 | 需启用 JavaScript |

## 四、快速开始

项目分为 `backend`（后端）与 `frontend`（前端）两个目录，需要分别启动。以下命令在 PowerShell 中执行。

### 1. 启动后端

```powershell
cd backend

# 创建并激活虚拟环境（首次）
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 安装依赖（首次）
pip install -r requirements.txt

# 初始化数据库（首次，写入 16 个点位）
python scripts\init_data.py

# 启动后端服务
uvicorn app.main:app --reload
```

后端启动后：

- 接口地址：`http://127.0.0.1:8000`
- 在线接口文档：`http://127.0.0.1:8000/docs`

### 2. 启动前端

另开一个 PowerShell 窗口：

```powershell
cd frontend

# 安装依赖（首次）
npm install

# 启动开发服务
npm run dev
```

前端启动后，浏览器访问：`http://127.0.0.1:5173`

前端已配置代理，`/api` 请求会自动转发到后端 `http://127.0.0.1:8000`，无需额外处理跨域。

## 五、演示主流程

1. 打开 `http://127.0.0.1:5173`，在地图上浏览 16 个点位。
2. 点击左侧「筛选」选择行政区与点位类型，地图实时更新；点击「标记」可只看自己标记的点位。
3. 点击任意点位，右侧弹出详情卡片，查看简介、开放时间、停留时长、门票或消费。
4. 点击「添加到路线」，点位进入左侧待选清单；同一点位不能重复添加。
5. 切换到底部「规划」页，选择顺路最优 / 清单顺序、驾车 / 步行，点击「一键生成路线」。
6. 在右侧路线卡片中点击展开，查看迷你地图、连线与行程顺序，可重命名、复制、删除。

## 六、配置说明

### 数据库

默认使用 SQLite，连接串为 `sqlite:///./nanchang_trip.sqlite3`，数据库文件位于 `backend` 目录下，零配置即可使用。

如需切换 MySQL：

1. 复制 `backend/.env.example` 为 `backend/.env`。
2. 修改 `DATABASE_URL`，填入实际密码与库名：

```
DATABASE_URL=mysql+pymysql://root:你的密码@127.0.0.1:3306/nanchang_trip?charset=utf8mb4
```

3. 需提前创建 `nanchang_trip` 数据库，再执行 `python scripts\init_data.py`。

### 高德地图 Key

中期模拟地图不需要 Key。后续接入真实地图时，在 `.env` 中填写 `AMAP_KEY` 与 `AMAP_SECRET`。

## 七、目录结构

```
洪城漫游/
├── README.md
├── 代码说明书.md
├── backend/
│   ├── requirements.txt        # 后端依赖
│   ├── .env.example            # 环境变量模板
│   ├── scripts/init_data.py    # 初始化数据
│   └── app/
│       ├── main.py             # 应用入口
│       ├── core/               # 配置、数据库连接
│       ├── models/             # ORM 模型（7 张表）
│       ├── schemas/            # 数据校验
│       ├── services/           # 路线算法
│       └── api/                # 点位、路线接口
└── frontend/
    ├── vite.config.js          # 含 /api 代理
    └── src/
        ├── App.vue
        ├── api/                # 接口封装
        ├── stores/             # 全局状态与本地持久化
        ├── utils/              # 投影与模拟地图布局
        ├── styles/             # 设计 Token 与全局样式
        ├── components/         # 8 个组件
        └── views/              # 地图页、规划页
```

## 八、常见问题

**1. 前端页面能打开，但数据加载失败？**
请确认后端已在 `8000` 端口启动，并访问 `http://127.0.0.1:8000/docs` 检查。

**2. 执行 PowerShell 脚本提示无法加载脚本？**
可执行 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` 后重试，或不激活虚拟环境，直接用 `.\.venv\Scripts\python.exe` 与 `.\.venv\Scripts\uvicorn.exe` 运行。

**3. 重新初始化时报主键或数据错误？**
删除 `backend\nanchang_trip.sqlite3` 后重新执行 `python scripts\init_data.py` 即可。

**4. 玻璃模糊效果不显示？**
部分旧浏览器不支持 `backdrop-filter`，系统会自动降级为半透明纯色，功能不受影响。

**5. npm install 速度慢？**
可切换国内镜像：`npm config set registry https://registry.npmmirror.com`。
