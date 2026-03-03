# database.py (SQLite LOCAL)
import os
import sqlite3
import random

DB_PATH = os.path.join(os.path.dirname(__file__), "quickeats.db")

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            price REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

def generate_customer_id():
    conn = connect_db()
    cur = conn.cursor()
    while True:
        customer_id = random.randint(100000, 999999)
        cur.execute("SELECT 1 FROM customers WHERE id = ?", (customer_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return customer_id

def create_customer(name):
    customer_id = generate_customer_id()
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO customers (id, name) VALUES (?, ?)", (customer_id, name))
        conn.commit()
        return customer_id
    except sqlite3.IntegrityError:
        # name already exists, fetch existing id
        cur.execute("SELECT id FROM customers WHERE name = ?", (name,))
        row = cur.fetchone()
        return row["id"] if row else None
    finally:
        cur.close()
        conn.close()

def insert_order(customer_name, item_name, price):
    init_db()
    conn = connect_db()
    cur = conn.cursor()
    try:
        # find customer
        cur.execute("SELECT id FROM customers WHERE name = ?", (customer_name,))
        row = cur.fetchone()

        if row:
            customer_id = row["id"]
        else:
            customer_id = create_customer(customer_name)
            if not customer_id:
                return False

        cur.execute(
            "INSERT INTO orders (customer_id, item_name, price, status) VALUES (?, ?, ?, 'Pending')",
            (customer_id, item_name, float(price))
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ SQLite Error (insert_order): {e}")
        return False
    finally:
        cur.close()
        conn.close()

def fetch_orders():
    init_db()
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT
                orders.id AS order_id,
                customers.name AS customer_name,
                orders.item_name,
                orders.price,
                COALESCE(orders.status, 'Pending') AS status
            FROM orders
            JOIN customers ON orders.customer_id = customers.id
            ORDER BY orders.id DESC
        """)
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"❌ SQLite Error (fetch_orders): {e}")
        return []
    finally:
        cur.close()
        conn.close()

def update_order_status(order_id, status):
    init_db()
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ SQLite Error (update_order_status): {e}")
        return False
    finally:
        cur.close()
        conn.close()

def delete_order(order_id):
    init_db()
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ SQLite Error (delete_order): {e}")
        return False
    finally:
        cur.close()
        conn.close()

def clear_completed_orders():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM orders WHERE status = 'Completed'")
            conn.commit()
            print("✅ Completed orders cleared!")
        except mysql.connector.Error as err:
            print(f"❌ Query Error: {err}")
        finally:
            cursor.close()
            conn.close()

def clear_all_orders(reset_auto_increment=True):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM orders")
            if reset_auto_increment:
                cursor.execute("ALTER TABLE orders AUTO_INCREMENT = 1")
            conn.commit()
            print("✅ All orders cleared!")
        except mysql.connector.Error as err:
            print(f"❌ Query Error: {err}")
        finally:
            cursor.close()
            conn.close()