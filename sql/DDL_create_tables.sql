-- ============================================================
-- Logistics Portfolio Database - DDL Script
-- Database: logistics-db (Azure SQL Database)
-- ============================================================

-- ============================================================
-- MASTER TABLES
-- ============================================================

CREATE TABLE Supplier (
    supplier_id   INT           IDENTITY(1,1) PRIMARY KEY,
    supplier_name NVARCHAR(100) NOT NULL,
    country       NVARCHAR(50)  NOT NULL,
    region        NVARCHAR(50),
    contact_email NVARCHAR(100),
    phone         NVARCHAR(30),
    created_at    DATETIME2     DEFAULT GETDATE()
);

CREATE TABLE Product (
    product_id   INT           IDENTITY(1,1) PRIMARY KEY,
    product_name NVARCHAR(100) NOT NULL,
    category     NVARCHAR(50)  NOT NULL,
    unit         NVARCHAR(20)  NOT NULL,
    unit_price   DECIMAL(10,2) NOT NULL,
    weight_kg    DECIMAL(8,2),
    created_at   DATETIME2     DEFAULT GETDATE()
);

CREATE TABLE Warehouse (
    warehouse_id   INT           IDENTITY(1,1) PRIMARY KEY,
    warehouse_name NVARCHAR(100) NOT NULL,
    location       NVARCHAR(100) NOT NULL,
    country        NVARCHAR(50)  NOT NULL,
    capacity       INT           NOT NULL,
    manager_name   NVARCHAR(100),
    created_at     DATETIME2     DEFAULT GETDATE()
);

CREATE TABLE Customer (
    customer_id   INT           IDENTITY(1,1) PRIMARY KEY,
    customer_name NVARCHAR(100) NOT NULL,
    region        NVARCHAR(50)  NOT NULL,
    country       NVARCHAR(50)  NOT NULL,
    contact_email NVARCHAR(100),
    created_at    DATETIME2     DEFAULT GETDATE()
);

-- ============================================================
-- TRANSACTION TABLES
-- ============================================================

CREATE TABLE PurchaseOrder (
    po_id         INT           IDENTITY(1,1) PRIMARY KEY,
    supplier_id   INT           NOT NULL,
    product_id    INT           NOT NULL,
    order_date    DATE          NOT NULL,
    expected_date DATE          NOT NULL,
    quantity      INT           NOT NULL,
    unit_price    DECIMAL(10,2) NOT NULL,
    status        NVARCHAR(20)  NOT NULL
                  CHECK (status IN ('Ordered','In Transit','Received','Cancelled')),
    created_at    DATETIME2     DEFAULT GETDATE(),
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id),
    FOREIGN KEY (product_id)  REFERENCES Product(product_id)
);

CREATE TABLE Receiving (
    receiving_id      INT       IDENTITY(1,1) PRIMARY KEY,
    po_id             INT       NOT NULL,
    warehouse_id      INT       NOT NULL,
    received_date     DATE      NOT NULL,
    quantity_received INT       NOT NULL,
    quality_check     NVARCHAR(20) DEFAULT 'Passed'
                      CHECK (quality_check IN ('Passed','Failed','Partial')),
    created_at        DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (po_id)          REFERENCES PurchaseOrder(po_id),
    FOREIGN KEY (warehouse_id)   REFERENCES Warehouse(warehouse_id)
);

CREATE TABLE Inventory (
    inventory_id     INT       IDENTITY(1,1) PRIMARY KEY,
    warehouse_id     INT       NOT NULL,
    product_id       INT       NOT NULL,
    quantity_on_hand INT       NOT NULL DEFAULT 0,
    reorder_point    INT       NOT NULL DEFAULT 50,
    last_updated     DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (warehouse_id) REFERENCES Warehouse(warehouse_id),
    FOREIGN KEY (product_id)   REFERENCES Product(product_id),
    CONSTRAINT uq_warehouse_product UNIQUE (warehouse_id, product_id)
);

CREATE TABLE SalesOrder (
    so_id       INT          IDENTITY(1,1) PRIMARY KEY,
    customer_id INT          NOT NULL,
    order_date  DATE         NOT NULL,
    status      NVARCHAR(20) NOT NULL
                CHECK (status IN ('Pending','Processing','Shipped','Delivered','Cancelled')),
    total_amount DECIMAL(12,2),
    created_at  DATETIME2    DEFAULT GETDATE(),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

CREATE TABLE SalesOrderDetail (
    detail_id  INT           IDENTITY(1,1) PRIMARY KEY,
    so_id      INT           NOT NULL,
    product_id INT           NOT NULL,
    quantity   INT           NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    subtotal   AS (quantity * unit_price),
    FOREIGN KEY (so_id)      REFERENCES SalesOrder(so_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

CREATE TABLE Shipment (
    shipment_id    INT          IDENTITY(1,1) PRIMARY KEY,
    so_id          INT          NOT NULL,
    warehouse_id   INT          NOT NULL,
    scheduled_date DATE         NOT NULL,
    actual_date    DATE,
    carrier        NVARCHAR(50) NOT NULL,
    tracking_no    NVARCHAR(50),
    status         NVARCHAR(20) NOT NULL
                   CHECK (status IN ('Preparing','In Transit','Delivered','Delayed','Failed')),
    created_at     DATETIME2    DEFAULT GETDATE(),
    FOREIGN KEY (so_id)        REFERENCES SalesOrder(so_id),
    FOREIGN KEY (warehouse_id) REFERENCES Warehouse(warehouse_id)
);

-- ============================================================
-- INDEXES (for analytical query performance)
-- ============================================================

CREATE INDEX idx_po_order_date      ON PurchaseOrder(order_date);
CREATE INDEX idx_po_status          ON PurchaseOrder(status);
CREATE INDEX idx_receiving_date     ON Receiving(received_date);
CREATE INDEX idx_inventory_wh       ON Inventory(warehouse_id);
CREATE INDEX idx_so_order_date      ON SalesOrder(order_date);
CREATE INDEX idx_so_status          ON SalesOrder(status);
CREATE INDEX idx_shipment_status    ON Shipment(status);
CREATE INDEX idx_shipment_dates     ON Shipment(scheduled_date, actual_date);
