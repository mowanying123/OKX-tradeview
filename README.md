# OKX TradeView

OKX TradeView 是一个基于 Django 5.0 构建的加密货币交易管理平台，集成了多个功能模块，包括用户身份验证、数据展示、卡片管理、自动售货机支付等。该项目的核心模块 **Cryptoforward** 处理与加密货币交易相关的功能。

## 项目功能

项目按照功能模块化设计，每个模块负责不同的业务逻辑。以下是项目中的主要模块：

### 核心模块：`apps/cryptoforward`

`Cryptoforward` 模块是项目的核心功能，负责与加密货币相关的交易数据处理及展示。其功能包括：
- **消息格式化**：通过 `formatMsg.py` 对加密交易数据进行格式化，以便进行分析和展示。
- **交易数据处理**：通过 `models.py` 管理和存储交易相关的数据。
- **视图展示**：通过 `views.py` 实现交易相关页面的展示和数据更新。
- **URL 路由**：通过 `urls.py` 定义和处理与交易相关的路由。

### 其他重要模块
- **Authentication**：提供用户登录、注册、忘记密码等功能。
- **Dashboards**：展示数据分析仪表盘，帮助用户直观了解交易数据和系统状态。
- **Cards**：管理卡片数据，提供卡片样式的UI展示。
- **VendingMachine**：提供自动售货机相关功能，包括产品展示和支付。
- **UI & Layouts**：提供丰富的UI组件和布局模板，增强用户体验。

## 项目依赖

该项目依赖以下主要 Python 包，具体可查看 `requirements.txt` 文件：

```bash
asgiref==3.7.2
Django==5.0
gunicorn==21.2.0
packaging==23.1
python-dotenv==1.0.0
sqlparse==0.4.4
typing_extensions==4.7.1
whitenoise==6.5.0
django_q==1.3.9
redis==4.5.3
```

## 环境配置

1. 项目通过 `python-dotenv` 管理环境变量，需要创建 `.env` 文件并配置相应的环境变量。

   示例 `.env` 文件：
   ```bash
   SECRET_KEY=your-secret-key
   DEBUG=True
   DJANGO_ENVIRONMENT=local
   DATABASE_NAME=OKXTradeView
   DATABASE_USER=OKXTradeView
   DATABASE_PASSWORD=your-db-password
   ```

2. 确保本地安装 PostgreSQL 数据库并配置好连接信息。

## 部署步骤

以下是项目的部署步骤：

### 1. 克隆项目
```bash
git clone https://github.com/mowanying123/OKX-tradeview.git
cd OKX-tradeview
```

### 2. 创建并激活虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 数据库迁移
确保 PostgreSQL 数据库已运行，并在 `config/settings.py` 中正确配置了数据库连接。执行以下命令进行数据库迁移：
```bash
python manage.py migrate
```

### 5. 启动开发服务器
运行以下命令启动本地开发服务器：
```bash
python manage.py runserver
```

### 6. 部署到生产环境
生产环境推荐使用 `gunicorn` 作为 WSGI 服务器。可以使用以下命令启动生产服务器：
```bash
gunicorn --config gunicorn-cfg.py config.wsgi
```

至此，项目应已成功启动并运行。

## 任务队列设置

项目使用了 `Django Q` 和 Redis 处理异步任务。部署 Redis 并使用以下命令启动任务队列：
```bash
python manage.py qcluster
```

## 贡献

欢迎提交 Issues 和 Pull Requests。如果有任何问题或建议，请联系项目维护者。