# 飞享无人机服务平台后端 API

这是飞享无人机服务平台的后端 API，使用 Python + Flask + MySQL 实现。

## 功能特点

- 用户认证与授权 (JWT)
- 商品管理 API
- 订单管理 API
- 数据库事务支持
- 错误处理和异常管理

## 技术栈

- **语言**: Python 3.9+
- **Web 框架**: Flask
- **数据库**: MySQL
- **认证**: JWT (JSON Web Tokens)

## 安装与设置

### 前提条件

- Python 3.9 或更高版本
- MySQL 数据库
- pip (Python 包管理器)

### 安装步骤

1. 克隆仓库或下载源代码

2. 进入项目目录
   ```
   cd backend
   ```

3. 安装依赖包
   ```
   pip install -r requirements.txt
   ```

4. 配置数据库
   
   编辑 `config.py` 文件，配置数据库连接信息：
   ```python
   DB_CONFIG = {
       'host': 'localhost',  # 数据库主机地址
       'user': 'root',       # 数据库用户名
       'password': 'your_password',  # 数据库密码
       'database': 'drone_shop'  # 数据库名称
   }
   ```

5. 初始化数据库
   
   在 MySQL 中运行 `database.sql` 文件创建所需的表结构和示例数据：
   ```
   mysql -u root -p < database.sql
   ```

6. 启动服务器
   ```
   python app.py
   ```
   
   默认情况下，API 服务器将在 http://localhost:5000 上运行

## API 文档

### 认证 API

- **注册新用户**: POST `/api/auth/register`
- **用户登录**: POST `/api/auth/login`
- **获取用户信息**: GET `/api/auth/profile` (需要认证)

### 商品 API

- **获取所有商品**: GET `/api/products`
- **获取商品详情**: GET `/api/products/<product_id>`
- **获取商品分类**: GET `/api/products/categories`
- **添加商品评价**: POST `/api/products/<product_id>/reviews` (需要认证)

### 订单 API

- **创建订单**: POST `/api/orders` (需要认证)
- **获取用户订单**: GET `/api/orders` (需要认证)
- **获取订单详情**: GET `/api/orders/<order_id>` (需要认证)
- **更新订单状态**: PUT `/api/orders/<order_id>/status` (需要认证)
- **取消订单**: POST `/api/orders/<order_id>/cancel` (需要认证)

## 部署说明

对于生产环境，建议使用 Gunicorn 或 uWSGI 等 WSGI 服务器，配合 Nginx 作为反向代理：

```
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

## 安全注意事项

在生产环境中部署时，请注意以下几点：

1. 更改 `config.py` 中的 JWT_SECRET 为强密码
2. 使用环境变量或配置文件存储敏感信息，而不是硬编码
3. 配置适当的 CORS 策略
4. 使用 HTTPS 保护 API 通信 