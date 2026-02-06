CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  full_name VARCHAR(100) NOT NULL,
  role ENUM('admin', 'staff') NOT NULL DEFAULT 'staff',
  hashed_password VARCHAR(255) NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE customers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  contact_name VARCHAR(50) NOT NULL,
  contact_phone VARCHAR(30) NOT NULL,
  address VARCHAR(255) NOT NULL,
  created_by INT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_customers_created_by (created_by)
) ENGINE=InnoDB;

CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  sku VARCHAR(50) NOT NULL UNIQUE,
  unit_price DECIMAL(12,2) NOT NULL,
  created_by INT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_products_created_by (created_by)
) ENGINE=InnoDB;

CREATE TABLE sales_orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_no VARCHAR(30) NOT NULL UNIQUE,
  customer_id INT NOT NULL,
  status ENUM('created', 'confirmed', 'shipped', 'cancelled') NOT NULL DEFAULT 'created',
  total_amount DECIMAL(12,2) NOT NULL,
  created_by INT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_sales_orders_customer_id (customer_id),
  INDEX idx_sales_orders_created_by (created_by),
  CONSTRAINT fk_sales_orders_customers FOREIGN KEY (customer_id) REFERENCES customers(id)
) ENGINE=InnoDB;

CREATE TABLE sales_order_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  unit_price DECIMAL(12,2) NOT NULL,
  line_amount DECIMAL(12,2) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_sales_order_items_order_id (order_id),
  CONSTRAINT fk_sales_order_items_orders FOREIGN KEY (order_id) REFERENCES sales_orders(id),
  CONSTRAINT fk_sales_order_items_products FOREIGN KEY (product_id) REFERENCES products(id)
) ENGINE=InnoDB;

CREATE TABLE stock_balances (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL UNIQUE,
  quantity INT NOT NULL DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_stock_balances_products FOREIGN KEY (product_id) REFERENCES products(id)
) ENGINE=InnoDB;

CREATE TABLE stock_documents (
  id INT AUTO_INCREMENT PRIMARY KEY,
  doc_no VARCHAR(30) NOT NULL UNIQUE,
  doc_type ENUM('stock_in', 'stock_out') NOT NULL,
  related_order_id INT NULL,
  created_by INT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_stock_documents_order_id (related_order_id),
  CONSTRAINT fk_stock_documents_orders FOREIGN KEY (related_order_id) REFERENCES sales_orders(id)
) ENGINE=InnoDB;

CREATE TABLE stock_ledgers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  stock_doc_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  unit_cost DECIMAL(12,2) NOT NULL,
  created_by INT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_stock_ledgers_doc_id (stock_doc_id),
  CONSTRAINT fk_stock_ledgers_docs FOREIGN KEY (stock_doc_id) REFERENCES stock_documents(id),
  CONSTRAINT fk_stock_ledgers_products FOREIGN KEY (product_id) REFERENCES products(id)
) ENGINE=InnoDB;
