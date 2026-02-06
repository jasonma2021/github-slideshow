# SME ERP Backend (FastAPI)

## 1. 项目目录结构
```
backend/
  app/
    api/
      deps.py
      routers/
        auth.py
        customers.py
        orders.py
        products.py
        reports.py
        stock.py
        users.py
    core/
      config.py
      constants.py
      database.py
      security.py
    models/
      base.py
      customer.py
      order.py
      product.py
      stock.py
      user.py
    repositories/
      customer_repo.py
      order_repo.py
      product_repo.py
      stock_repo.py
      user_repo.py
    schemas/
      auth.py
      customer.py
      order.py
      product.py
      stock.py
      user.py
    services/
      auth_service.py
      order_service.py
      stock_service.py
    main.py
  docs/
    schema.sql
  requirements.txt
```

## 2. 数据库表结构（SQL）
见 `docs/schema.sql`。

## 3. 核心模型
- User、Product、Customer、SalesOrder、StockBalance、StockDocument、StockLedger

## 4. 关键业务逻辑
- 下单：`services/order_service.py:create_order`
- 出库：`services/stock_service.py:stock_out_for_order`
- 扣库存：`services/stock_service.py` 中使用 `SELECT ... FOR UPDATE` 行级锁

## 5. 示例 API 接口定义

### 登录
**POST** `/api/v1/auth/login`

Request (form):
```
username=admin&password=secret
```
Response:
```
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

### 创建客户
**POST** `/api/v1/customers`

Request:
```
{
  "name": "ACME",
  "contact_name": "张三",
  "contact_phone": "13800000000",
  "address": "深圳市南山区"
}
```
Response:
```
{
  "id": 1,
  "name": "ACME",
  "contact_name": "张三",
  "contact_phone": "13800000000",
  "address": "深圳市南山区"
}
```

### 创建销售订单
**POST** `/api/v1/orders`

Request:
```
{
  "customer_id": 1,
  "items": [
    {"product_id": 1, "quantity": 2, "unit_price": 99.00}
  ]
}
```
Response:
```
{
  "id": 1,
  "order_no": "SO20240630120000",
  "customer_id": 1,
  "status": "created",
  "total_amount": 198.00,
  "items": [
    {"id": 1, "product_id": 1, "quantity": 2, "unit_price": 99.00, "line_amount": 198.00}
  ]
}
```

### 订单出库
**POST** `/api/v1/stock/out`

Request:
```
{
  "order_id": 1
}
```
Response:
```
{
  "id": 10,
  "doc_no": "SO20240630120500",
  "doc_type": "stock_out",
  "related_order_id": 1
}
```

## 6. 事务与异常处理
- 关键写操作使用 `with db.begin()` 启动事务。
- 库存扣减使用 `SELECT ... FOR UPDATE` 行级锁，保证并发安全。
- 库存不足或单据重复等异常通过 HTTP 400 返回。

## 运行方式
1. 创建 `.env` 文件：
```
DATABASE_URL=mysql+pymysql://user:password@127.0.0.1:3306/erp
JWT_SECRET_KEY=change-me
```
2. 安装依赖：
```
pip install -r requirements.txt
```
3. 启动服务：
```
uvicorn app.main:app --reload
```
