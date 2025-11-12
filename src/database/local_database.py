import sqlite3
from typing import Optional

from src.models.receipt import Receipt


class ReceiptDatabase:

    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        # Create receipts table with enhanced schema
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                transaction_id TEXT UNIQUE NOT NULL,
                customer_name TEXT,
                date TEXT NOT NULL,
                time TEXT,
                restaurant_name TEXT NOT NULL,
                restaurant_location TEXT,
                delivery_address TEXT NOT NULL,
                delivery_fee REAL NOT NULL,
                driver_name TEXT,
                driver_vehicle TEXT,
                distance TEXT,
                estimated_time TEXT,
                actual_delivery_time TEXT,
                pickup_time TEXT,
                payment_subtotal REAL NOT NULL,
                payment_delivery_fee REAL NOT NULL,
                payment_service_fee REAL,
                payment_discount REAL NOT NULL,
                payment_total REAL NOT NULL,
                payment_method TEXT NOT NULL,
                special_instructions TEXT,
                order_status TEXT,
                additional_info_thank_you TEXT,
                additional_info_environmental TEXT,
                additional_info_final_note TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create items table with enhanced schema
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS receipt_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receipt_id INTEGER NOT NULL,
                item_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_price REAL,
                notes TEXT,
                FOREIGN KEY (receipt_id) REFERENCES receipts (id) ON DELETE CASCADE
            )
        ''')
        
        # Create index on transaction_id for faster lookups
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_transaction_id ON receipts(transaction_id)
        ''')

        self.conn.commit()

    def insert_receipt(self, receipt_data: Receipt):
        # Insert receipt data with enhanced schema
        self.cursor.execute('''
            INSERT OR REPLACE INTO receipts (
                platform, transaction_id, customer_name, date, time,
                restaurant_name, restaurant_location,
                delivery_address, delivery_fee, driver_name, driver_vehicle,
                distance, estimated_time, actual_delivery_time, pickup_time,
                payment_subtotal, payment_delivery_fee, payment_service_fee,
                payment_discount, payment_total, 
                payment_method, 
                special_instructions, order_status,
                additional_info_thank_you, additional_info_environmental, additional_info_final_note
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            receipt_data.platform,
            receipt_data.transaction_id,
            receipt_data.customer_name,
            receipt_data.date,
            receipt_data.time,
            receipt_data.restaurant.name,
            receipt_data.restaurant.location,
            receipt_data.delivery.address,
            receipt_data.delivery.fee,
            receipt_data.delivery.driver_name,
            receipt_data.delivery.driver_vehicle,
            receipt_data.delivery.distance,
            receipt_data.delivery.estimated_time,
            receipt_data.delivery.actual_delivery_time,
            receipt_data.delivery.pickup_time,
            receipt_data.payment.subtotal,
            receipt_data.payment.delivery_fee,
            receipt_data.payment.service_fee,
            receipt_data.payment.discount,
            receipt_data.payment.total,
            receipt_data.payment.method,
            receipt_data.special_instructions,
            receipt_data.order_status,
            receipt_data.additional_info.thank_you_message if receipt_data.additional_info else None,
            receipt_data.additional_info.environmental_note if receipt_data.additional_info else None,
            receipt_data.additional_info.final_note if receipt_data.additional_info else None
        ))
        
        # Get the receipt ID
        receipt_id = self.cursor.lastrowid
        
        # If this was an update (INSERT OR REPLACE), get the existing receipt ID
        if receipt_id is None:
            self.cursor.execute('SELECT id FROM receipts WHERE transaction_id = ?', 
                         (receipt_data.transaction_id,))
            receipt_id = self.cursor.fetchone()[0]
            
            # Delete existing items for this receipt
            self.cursor.execute('DELETE FROM receipt_items WHERE receipt_id = ?', (receipt_id,))
        
        # Insert items with enhanced schema
        for item in receipt_data.items:
            self.cursor.execute('''
                INSERT INTO receipt_items (receipt_id, item_name, quantity, unit_price, total_price, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (receipt_id, item.name, item.quantity, item.unit_price, item.total_price, item.notes))
        
        self.conn.commit()
        
        print(f"Successfully inserted receipt {receipt_data.transaction_id} with {len(receipt_data.items)} items")
        return True

    def execute_query(self, query: str, params: tuple = ()):
        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        
        # Get column names from cursor description
        column_names = [description[0] for description in self.cursor.description]
        
        # Convert results to list of dictionaries
        dict_results = []
        for row in results:
            dict_results.append(dict(zip(column_names, row)))
        
        return dict_results

    def get_schema(self):
        # Get receipts table schema
        self.cursor.execute("PRAGMA table_info(receipts)")
        receipts_columns = self.cursor.fetchall()
        receipts_schema = {col[1]: col[2] for col in receipts_columns}  # {column_name: data_type}
        
        # Get receipt_items table schema
        self.cursor.execute("PRAGMA table_info(receipt_items)")
        items_columns = self.cursor.fetchall()
        items_schema = {col[1]: col[2] for col in items_columns}  # {column_name: data_type}
        
        return {
            'receipts': receipts_schema,
            'receipt_items': items_schema
        }
    
    def close(self):
        self.conn.close()
    