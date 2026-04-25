"""
Logistics Portfolio - Sample Data Generator
============================================
Install required libraries:
    pip install faker numpy pandas

How to run:
    python generate_data.py

Output: CSV files will be generated in the 'data' folder
"""

import os
import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import date, timedelta

fake = Faker('en_US')
Faker.seed(42)
random.seed(42)
np.random.seed(42)

os.makedirs('data', exist_ok=True)

# ============================================================
# Configuration
# ============================================================
N_SUPPLIERS   = 30
N_PRODUCTS    = 80
N_WAREHOUSES  = 6
N_CUSTOMERS   = 200
N_PO          = 3000   # number of purchase orders
N_SO          = 8000   # number of sales orders
START_DATE    = date(2022, 1, 1)
END_DATE      = date(2024, 12, 31)

def rand_date(start=START_DATE, end=END_DATE):
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

# ============================================================
# 1. Supplier
# ============================================================
countries = ['Japan', 'China', 'South Korea', 'Vietnam', 'Thailand',
             'Germany', 'USA', 'Canada', 'India', 'Mexico']
regions_map = {
    'Japan': 'Asia', 'China': 'Asia', 'South Korea': 'Asia',
    'Vietnam': 'Asia', 'Thailand': 'Asia', 'Germany': 'Europe',
    'USA': 'North America', 'Canada': 'North America',
    'India': 'Asia', 'Mexico': 'North America'
}

suppliers = []
for i in range(1, N_SUPPLIERS + 1):
    country = random.choice(countries)
    suppliers.append({
        'supplier_id':   i,
        'supplier_name': fake.company(),
        'country':       country,
        'region':        regions_map[country],
        'contact_email': fake.company_email(),
        'phone':         fake.phone_number(),
        'created_at':    rand_date(date(2020,1,1), date(2021,12,31))
    })

df_suppliers = pd.DataFrame(suppliers)
df_suppliers.to_csv('data/Supplier.csv', index=False)
print(f"Supplier: {len(df_suppliers)} rows")

# ============================================================
# 2. Product
# ============================================================
categories = {
    'Electronics':    [('Laptop', 120000), ('Monitor', 45000), ('Keyboard', 8000),
                       ('Mouse', 3500), ('USB Hub', 4000), ('Webcam', 12000)],
    'Furniture':      [('Office Chair', 35000), ('Standing Desk', 60000),
                       ('Filing Cabinet', 22000), ('Bookshelf', 18000)],
    'Stationery':     [('Notebook', 500), ('Pen Set', 1200), ('Stapler', 1500),
                       ('Whiteboard', 8000), ('Paper Ream', 600)],
    'Industrial':     [('Safety Helmet', 3000), ('Work Gloves', 800),
                       ('Tool Kit', 15000), ('Storage Box', 2500)],
    'Packaging':      [('Cardboard Box S', 200), ('Cardboard Box M', 350),
                       ('Cardboard Box L', 500), ('Bubble Wrap Roll', 1500),
                       ('Packing Tape', 300)],
    'Food & Beverage':[('Coffee Beans 1kg', 2500), ('Green Tea 100g', 800),
                       ('Mineral Water 24pk', 1200), ('Energy Bar 12pk', 1800)],
}

products = []
pid = 1
for category, items in categories.items():
    for name, base_price in items:
        price = base_price * (1 + random.uniform(-0.1, 0.2))
        products.append({
            'product_id':   pid,
            'product_name': name,
            'category':     category,
            'unit':         'pcs' if category != 'Food & Beverage' else 'pack',
            'unit_price':   round(price, 2),
            'weight_kg':    round(random.uniform(0.1, 20.0), 2),
            'created_at':   rand_date(date(2020,1,1), date(2021,12,31))
        })
        pid += 1

# Pad to reach N_PRODUCTS total
while len(products) < N_PRODUCTS:
    cat = random.choice(list(categories.keys()))
    products.append({
        'product_id':   pid,
        'product_name': f'Product-{pid}',
        'category':     cat,
        'unit':         'pcs',
        'unit_price':   round(random.uniform(500, 50000), 2),
        'weight_kg':    round(random.uniform(0.1, 15.0), 2),
        'created_at':   rand_date(date(2020,1,1), date(2021,12,31))
    })
    pid += 1

df_products = pd.DataFrame(products)
df_products.to_csv('data/Product.csv', index=False)
print(f"Product: {len(df_products)} rows")

# ============================================================
# 3. Warehouse
# ============================================================
warehouses_data = [
    ('Tokyo DC',     'Tokyo',     'Japan',   10000, 'Tanaka Hiroshi'),
    ('Osaka DC',     'Osaka',     'Japan',    8000, 'Yamamoto Keiko'),
    ('Shanghai WH',  'Shanghai',  'China',   15000, 'Li Wei'),
    ('Seoul WH',     'Seoul',     'South Korea', 6000, 'Kim Jisoo'),
    ('Vancouver DC', 'Vancouver', 'Canada',   7000, 'Smith John'),
    ('LA DC',        'Los Angeles','USA',     9000, 'Garcia Maria'),
]

warehouses = []
for i, (name, loc, country, cap, mgr) in enumerate(warehouses_data, 1):
    warehouses.append({
        'warehouse_id':   i,
        'warehouse_name': name,
        'location':       loc,
        'country':        country,
        'capacity':       cap,
        'manager_name':   mgr,
        'created_at':     rand_date(date(2020,1,1), date(2021,6,30))
    })

df_warehouses = pd.DataFrame(warehouses)
df_warehouses.to_csv('data/Warehouse.csv', index=False)
print(f"Warehouse: {len(df_warehouses)} rows")

# ============================================================
# 4. Customer
# ============================================================
cust_countries = ['Japan', 'Canada', 'USA', 'Australia', 'UK', 'France', 'Germany']
cust_region_map = {
    'Japan': 'Asia', 'Canada': 'North America', 'USA': 'North America',
    'Australia': 'Oceania', 'UK': 'Europe', 'France': 'Europe', 'Germany': 'Europe'
}

customers = []
for i in range(1, N_CUSTOMERS + 1):
    country = random.choice(cust_countries)
    customers.append({
        'customer_id':   i,
        'customer_name': fake.company(),
        'region':        cust_region_map[country],
        'country':       country,
        'contact_email': fake.company_email(),
        'created_at':    rand_date(date(2021,1,1), date(2022,6,30))
    })

df_customers = pd.DataFrame(customers)
df_customers.to_csv('data/Customer.csv', index=False)
print(f"Customer: {len(df_customers)} rows")

# ============================================================
# 5. PurchaseOrder + Receiving
# ============================================================
po_statuses  = ['Ordered', 'In Transit', 'Received', 'Cancelled']
po_status_weights = [0.05, 0.10, 0.80, 0.05]

purchase_orders = []
receivings = []
rid = 1

for po_id in range(1, N_PO + 1):
    order_date    = rand_date()
    lead_days     = random.randint(7, 45)
    expected_date = order_date + timedelta(days=lead_days)
    status        = random.choices(po_statuses, po_status_weights)[0]
    supplier_id   = random.randint(1, N_SUPPLIERS)
    product_id    = random.randint(1, N_PRODUCTS)
    quantity      = random.randint(10, 500)
    unit_price    = df_products.loc[product_id - 1, 'unit_price']

    purchase_orders.append({
        'po_id':         po_id,
        'supplier_id':   supplier_id,
        'product_id':    product_id,
        'order_date':    order_date,
        'expected_date': expected_date,
        'quantity':      quantity,
        'unit_price':    unit_price,
        'status':        status,
        'created_at':    order_date
    })

    # Generate a receiving record if status is Received
    if status == 'Received':
        # Add random variance to lead time (includes delay scenarios)
        delay = int(np.random.normal(0, 5))
        received_date = expected_date + timedelta(days=delay)
        if received_date < order_date:
            received_date = order_date + timedelta(days=2)

        qty_received = quantity if random.random() > 0.05 else int(quantity * random.uniform(0.7, 0.99))
        quality = random.choices(['Passed', 'Failed', 'Partial'], [0.92, 0.03, 0.05])[0]

        receivings.append({
            'receiving_id':      rid,
            'po_id':             po_id,
            'warehouse_id':      random.randint(1, N_WAREHOUSES),
            'received_date':     received_date,
            'quantity_received': qty_received,
            'quality_check':     quality,
            'created_at':        received_date
        })
        rid += 1

df_po = pd.DataFrame(purchase_orders)
df_po.to_csv('data/PurchaseOrder.csv', index=False)
print(f"PurchaseOrder: {len(df_po)} rows")

df_receiving = pd.DataFrame(receivings)
df_receiving.to_csv('data/Receiving.csv', index=False)
print(f"Receiving: {len(df_receiving)} rows")

# ============================================================
# 6. Inventory
# ============================================================
inventory = []
inv_id = 1
for wh_id in range(1, N_WAREHOUSES + 1):
    # Each warehouse stocks 50-70 products
    n_products_in_wh = random.randint(50, 70)
    product_ids = random.sample(range(1, N_PRODUCTS + 1), n_products_in_wh)
    for prod_id in product_ids:
        # Use log-normal distribution to simulate realistic stock variance
        qty = int(np.random.lognormal(mean=4.5, sigma=1.2))
        qty = max(0, min(qty, 5000))
        inventory.append({
            'inventory_id':     inv_id,
            'warehouse_id':     wh_id,
            'product_id':       prod_id,
            'quantity_on_hand': qty,
            'reorder_point':    random.randint(20, 100),
            'last_updated':     rand_date(date(2024,10,1), END_DATE)
        })
        inv_id += 1

df_inventory = pd.DataFrame(inventory)
df_inventory.to_csv('data/Inventory.csv', index=False)
print(f"Inventory: {len(df_inventory)} rows")

# ============================================================
# 7. SalesOrder + SalesOrderDetail + Shipment
# ============================================================
so_statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
so_weights  = [0.03, 0.05, 0.10, 0.78, 0.04]
carriers    = ['Yamato Transport', 'Sagawa Express', 'Japan Post',
               'FedEx', 'DHL', 'UPS', 'Canada Post']

sales_orders   = []
so_details     = []
shipments      = []
detail_id = 1
ship_id   = 1

for so_id in range(1, N_SO + 1):
    order_date  = rand_date()
    customer_id = random.randint(1, N_CUSTOMERS)
    status      = random.choices(so_statuses, so_weights)[0]

    # Each order contains 1-4 line items
    n_items     = random.randint(1, 4)
    item_prods  = random.sample(range(1, N_PRODUCTS + 1), n_items)
    total       = 0

    for prod_id in item_prods:
        qty   = random.randint(1, 50)
        price = df_products.loc[prod_id - 1, 'unit_price']
        total += qty * price
        so_details.append({
            'detail_id':  detail_id,
            'so_id':      so_id,
            'product_id': prod_id,
            'quantity':   qty,
            'unit_price': price,
        })
        detail_id += 1

    sales_orders.append({
        'so_id':        so_id,
        'customer_id':  customer_id,
        'order_date':   order_date,
        'status':       status,
        'total_amount': round(total, 2),
        'created_at':   order_date
    })

    # Generate a shipment record for Shipped / Delivered orders
    if status in ('Shipped', 'Delivered'):
        scheduled = order_date + timedelta(days=random.randint(1, 5))
        # Approximately 15% of shipments are delayed
        if random.random() < 0.15:
            actual = scheduled + timedelta(days=random.randint(1, 10))
            ship_status = 'Delayed' if status == 'Shipped' else 'Delivered'
        else:
            actual = scheduled + timedelta(days=random.randint(-1, 2))
            actual = max(actual, scheduled)
            ship_status = status

        shipments.append({
            'shipment_id':    ship_id,
            'so_id':          so_id,
            'warehouse_id':   random.randint(1, N_WAREHOUSES),
            'scheduled_date': scheduled,
            'actual_date':    actual,
            'carrier':        random.choice(carriers),
            'tracking_no':    fake.bothify(text='??-########'),
            'status':         ship_status,
            'created_at':     scheduled
        })
        ship_id += 1

df_so = pd.DataFrame(sales_orders)
df_so.to_csv('data/SalesOrder.csv', index=False)
print(f"SalesOrder: {len(df_so)} rows")

df_detail = pd.DataFrame(so_details)
df_detail.to_csv('data/SalesOrderDetail.csv', index=False)
print(f"SalesOrderDetail: {len(df_detail)} rows")

df_ship = pd.DataFrame(shipments)
df_ship.to_csv('data/Shipment.csv', index=False)
print(f"Shipment: {len(df_ship)} rows")

# ============================================================
# Summary
# ============================================================
print("\n=== Generation complete ===")
total_rows = sum([
    len(df_suppliers), len(df_products), len(df_warehouses),
    len(df_customers), len(df_po), len(df_receiving),
    len(df_inventory), len(df_so), len(df_detail), len(df_ship)
])
print(f"Total rows: {total_rows:,}")
print("CSV files saved to the 'data' folder")