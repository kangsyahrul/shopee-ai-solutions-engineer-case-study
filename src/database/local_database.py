import sqlite3

from src.models.receipt import Receipt


class ReceiptDatabase:

    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        # Create receipts table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                transaction_id TEXT UNIQUE NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                restaurant_name TEXT NOT NULL,
                restaurant_location TEXT,
                delivery_address TEXT NOT NULL,
                delivery_fee REAL NOT NULL,
                payment_subtotal REAL NOT NULL,
                payment_delivery_fee REAL NOT NULL,
                payment_service_fee REAL,
                payment_discount REAL NOT NULL,
                payment_total REAL NOT NULL,
                payment_method TEXT NOT NULL,
                special_instructions TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create items table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS receipt_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receipt_id INTEGER NOT NULL,
                item_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                FOREIGN KEY (receipt_id) REFERENCES receipts (id) ON DELETE CASCADE
            )
        ''')
        
        # Create index on transaction_id for faster lookups
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_transaction_id ON receipts(transaction_id)
        ''')
        self.conn.commit()

    def insert_receipt(self, receipt_data: Receipt):
        # Insert receipt data
        self.cursor.execute('''
            INSERT OR REPLACE INTO receipts (
                platform, transaction_id, date, time,
                restaurant_name, restaurant_location,
                delivery_address, delivery_fee,
                payment_subtotal, payment_delivery_fee, payment_service_fee,
                payment_discount, payment_total, payment_method,
                special_instructions
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            receipt_data.platform,
            receipt_data.transaction_id,
            receipt_data.date,
            receipt_data.time,
            receipt_data.restaurant.name,
            receipt_data.restaurant.location,
            receipt_data.delivery.address,
            receipt_data.delivery.fee,
            receipt_data.payment.subtotal,
            receipt_data.payment.delivery_fee,
            receipt_data.payment.service_fee,
            receipt_data.payment.discount,
            receipt_data.payment.total,
            receipt_data.payment.method,
            receipt_data.special_instructions
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
        
        # Insert items
        for item in receipt_data.items:
            self.cursor.execute('''
                INSERT INTO receipt_items (receipt_id, item_name, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (receipt_id, item.name, item.quantity, item.price))
        
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

    def close(self):
        self.conn.close()
    