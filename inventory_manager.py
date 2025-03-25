#!/usr/bin/env python3
"""
Inventory Management System

A comprehensive inventory management application designed for small businesses in the Indian market.
Features include product management, stock tracking, supplier management, and GST handling.

Author: AI Assistant
"""

import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

class InventoryDatabase:
    """Handles all database operations for the inventory management system."""
    
    def __init__(self, db_file="inventory.db"):
        """Initialize database connection and create tables if they don't exist.
        
        Args:
            db_file (str): Path to SQLite database file
        """
        self.db_file = db_file
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establish connection to SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
            print(f"Connected to database: {self.db_file}")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
    
    def create_tables(self):
        """Create necessary tables if they don't exist."""
        # Categories table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )
        ''')
        
        # Suppliers table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            gstin TEXT UNIQUE  -- GST Identification Number
        )
        ''')
        
        # Products table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            category_id INTEGER,
            supplier_id INTEGER,
            cost_price REAL NOT NULL,
            selling_price REAL NOT NULL,
            gst_percentage REAL DEFAULT 18.0,
            hsn_code TEXT,  -- Harmonized System Nomenclature code for GST
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id),
            FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
        )
        ''')
        
        # Inventory table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            quantity INTEGER DEFAULT 0,
            reorder_level INTEGER DEFAULT 10,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
        ''')
        
        # Transactions table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            type TEXT CHECK (type IN ('purchase', 'sale', 'adjustment')),
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
        ''')
        
        # Initialize with default categories for Indian market
        default_categories = [
            (1, "Groceries & Staples", "Rice, Dal, Flour, etc."),
            (2, "Electronics", "Mobile phones, Laptops, Appliances"),
            (3, "Clothing", "Men's, Women's and Children's apparel"),
            (4, "Home & Kitchen", "Utensils, Cookware"),
            (5, "Beauty & Personal Care", "Cosmetics, Toiletries"),
            (6, "Stationery", "Books, Office supplies"),
            (7, "Snacks & Beverages", "Biscuits, Soft drinks"),
            (8, "Dairy Products", "Milk, Curd, Paneer")
        ]
        
        # Insert default categories if they don't exist
        self.cursor.executemany('''
        INSERT OR IGNORE INTO categories (id, name, description) VALUES (?, ?, ?)
        ''', default_categories)
        
        self.conn.commit()
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
    
    # Product management methods
    def add_product(self, name, description, category_id, supplier_id, cost_price, 
                   selling_price, gst_percentage, hsn_code, initial_stock=0):
        """Add a new product to the database.
        
        Args:
            name (str): Product name
            description (str): Product description
            category_id (int): Category ID
            supplier_id (int): Supplier ID
            cost_price (float): Cost price
            selling_price (float): Selling price
            gst_percentage (float): GST percentage
            hsn_code (str): HSN code for GST
            initial_stock (int, optional): Initial stock quantity
            
        Returns:
            int: Product ID if successful, None otherwise
        """
        try:
            # Insert product
            self.cursor.execute('''
            INSERT INTO products (name, description, category_id, supplier_id, 
                                cost_price, selling_price, gst_percentage, hsn_code)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, description, category_id, supplier_id, cost_price, 
                 selling_price, gst_percentage, hsn_code))
            
            product_id = self.cursor.lastrowid
            
            # Initialize inventory
            self.cursor.execute('''
            INSERT INTO inventory (product_id, quantity)
            VALUES (?, ?)
            ''', (product_id, initial_stock))
            
            # Record as transaction if initial stock > 0
            if initial_stock > 0:
                self.cursor.execute('''
                INSERT INTO transactions (type, product_id, quantity, notes)
                VALUES (?, ?, ?, ?)
                ''', ('purchase', product_id, initial_stock, 'Initial stock'))
            
            self.conn.commit()
            return product_id
        except sqlite3.Error as e:
            print(f"Error adding product: {e}")
            self.conn.rollback()
            return None
    
    def update_product(self, product_id, **kwargs):
        """Update product details.
        
        Args:
            product_id (int): Product ID to update
            **kwargs: Field-value pairs to update
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Build update query dynamically based on provided fields
            if not kwargs:
                return False
                
            update_fields = []
            values = []
            
            for field, value in kwargs.items():
                update_fields.append(f"{field} = ?")
                values.append(value)
            
            query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = ?"
            values.append(product_id)
            
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating product: {e}")
            self.conn.rollback()
            return False
    
    def delete_product(self, product_id):
        """Delete a product and its inventory records.
        
        Args:
            product_id (int): Product ID to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Delete from inventory first
            self.cursor.execute("DELETE FROM inventory WHERE product_id = ?", (product_id,))
            # Delete from transactions
            self.cursor.execute("DELETE FROM transactions WHERE product_id = ?", (product_id,))
            # Delete the product
            self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting product: {e}")
            self.conn.rollback()
            return False
    
    def get_product(self, product_id):
        """Get product details by ID.
        
        Args:
            product_id (int): Product ID
            
        Returns:
            dict: Product details or None if not found
        """
        try:
            self.cursor.execute('''
            SELECT p.id, p.name, p.description, p.category_id, c.name as category_name,
                   p.supplier_id, s.name as supplier_name, p.cost_price, p.selling_price,
                   p.gst_percentage, p.hsn_code, i.quantity
            FROM products p
            JOIN categories c ON p.category_id = c.id
            LEFT JOIN suppliers s ON p.supplier_id = s.id
            LEFT JOIN inventory i ON p.id = i.product_id
            WHERE p.id = ?
            ''', (product_id,))
            
            row = self.cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'category_id': row[3],
                    'category_name': row[4],
                    'supplier_id': row[5],
                    'supplier_name': row[6],
                    'cost_price': row[7],
                    'selling_price': row[8],
                    'gst_percentage': row[9],
                    'hsn_code': row[10],
                    'quantity': row[11]
                }
            return None
        except sqlite3.Error as e:
            print(f"Error retrieving product: {e}")
            return None
    
    def get_all_products(self):
        """Get all products with their current inventory levels.
        
        Returns:
            list: List of product dictionaries
        """
        try:
            self.cursor.execute('''
            SELECT p.id, p.name, p.description, c.name as category_name,
                   s.name as supplier_name, p.cost_price, p.selling_price,
                   p.gst_percentage, i.quantity
            FROM products p
            JOIN categories c ON p.category_id = c.id
            LEFT JOIN suppliers s ON p.supplier_id = s.id
            LEFT JOIN inventory i ON p.id = i.product_id
            ORDER BY p.name
            ''')
            
            products = []
            for row in self.cursor.fetchall():
                products.append({
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'category': row[3],
                    'supplier': row[4],
                    'cost_price': row[5],
                    'selling_price': row[6],
                    'gst_percentage': row[7],
                    'quantity': row[8]
                })
            return products
        except sqlite3.Error as e:
            print(f"Error retrieving products: {e}")
            return []
    
    # Inventory management methods
    def update_stock(self, product_id, quantity_change, transaction_type, notes=""):
        """Update stock level for a product.
        
        Args:
            product_id (int): Product ID
            quantity_change (int): Quantity to add (positive) or remove (negative)
            transaction_type (str): 'purchase', 'sale', or 'adjustment'
            notes (str, optional): Transaction notes
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get current quantity
            self.cursor.execute("SELECT quantity FROM inventory WHERE product_id = ?", 
                              (product_id,))
            row = self.cursor.fetchone()
            
            if row is None:
                # Create inventory record if it doesn't exist
                self.cursor.execute('''
                INSERT INTO inventory (product_id, quantity, last_updated)
                VALUES (?, ?, datetime('now'))
                ''', (product_id, quantity_change))
            else:
                # Update existing inventory
                current_quantity = row[0]
                new_quantity = current_quantity + quantity_change
                
                if new_quantity < 0:
                    print(f"Error: Stock cannot be negative. Current: {current_quantity}, Change: {quantity_change}")
                    return False
                
                self.cursor.execute('''
                UPDATE inventory 
                SET quantity = ?, last_updated = datetime('now')
                WHERE product_id = ?
                ''', (new_quantity, product_id))
            
            # Record transaction
            self.cursor.execute('''
            INSERT INTO transactions (type, product_id, quantity, notes)
            VALUES (?, ?, ?, ?)
            ''', (transaction_type, product_id, quantity_change, notes))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating stock: {e}")
            self.conn.rollback()
            return False
    
    def get_low_stock_products(self, threshold=None):
        """Get products with stock below their reorder level.
        
        Args:
            threshold (int, optional): Override default reorder level
            
        Returns:
            list: List of low stock products
        """
        try:
            if threshold is not None:
                query = '''
                SELECT p.id, p.name, i.quantity, i.reorder_level
                FROM products p
                JOIN inventory i ON p.id = i.product_id
                WHERE i.quantity <= ?
                ORDER BY i.quantity
                '''
                self.cursor.execute(query, (threshold,))
            else:
                query = '''
                SELECT p.id, p.name, i.quantity, i.reorder_level
                FROM products p
                JOIN inventory i ON p.id = i.product_id
                WHERE i.quantity <= i.reorder_level
                ORDER BY i.quantity
                '''
                self.cursor.execute(query)
            
            low_stock = []
            for row in self.cursor.fetchall():
                low_stock.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2],
                    'reorder_level': row[3]
                })
            return low_stock
        except sqlite3.Error as e:
            print(f"Error getting low stock products: {e}")
            return []
    
    # Category management methods
    def get_all_categories(self):
        """Get all product categories.
        
        Returns:
            list: List of category dictionaries
        """
        try:
            self.cursor.execute("SELECT id, name, description FROM categories ORDER BY name")
            
            categories = []
            for row in self.cursor.fetchall():
                categories.append({
                    'id': row[0],
                    'name': row[1],
                    'description': row[2]
                })
            return categories
        except sqlite3.Error as e:
            print(f"Error retrieving categories: {e}")
            return []
    
    def add_category(self, name, description=""):
        """Add a new product category.
        
        Args:
            name (str): Category name
            description (str, optional): Category description
            
        Returns:
            int: Category ID if successful, None otherwise
        """
        try:
            self.cursor.execute('''
            INSERT INTO categories (name, description)
            VALUES (?, ?)
            ''', (name, description))
            
            category_id = self.cursor.lastrowid
            self.conn.commit()
            return category_id
        except sqlite3.Error as e:
            print(f"Error adding category: {e}")
            self.conn.rollback()
            return None
