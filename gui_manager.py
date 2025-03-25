#!/usr/bin/env python3
"""
Inventory Management System GUI

A comprehensive inventory management application with a GUI interface designed for small businesses
in the Indian market. This module provides the graphical interface for the inventory management
system, building on the database functionality provided by inventory_manager.py.

Features include:
- Product management (add/edit/delete products)
- Inventory management (stock updates)
- Supplier management
- Reports (low stock, sales, etc.)
- GST calculation and billing
- Modern, user-friendly interface

Author: AI Assistant
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from tkcalendar import DateEntry  # You might need to install this: pip install tkcalendar
import datetime
from PIL import Image, ImageTk  # You might need to install this: pip install pillow
import matplotlib.pyplot as plt  # You might need to install this: pip install matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd  # You might need to install this: pip install pandas

# Import from inventory_manager.py
from inventory_manager import InventoryDatabase

class InventoryManagementSystem:
    """Main application class for the Inventory Management System GUI."""
    
    def __init__(self, master, db_manager):
        """Initialize the application GUI.
        
        Args:
            master: The root Tkinter window
            db_manager: The database manager instance
        """
        self.master = master
        self.db = db_manager
        
        # Configure the main window
        self.master.title("Inventory Management System")
        self.master.geometry("1200x700")
        self.master.minsize(1000, 600)
        self.master.configure(bg="#f0f0f0")
        
        # Set application icon (if available)
        try:
            self.master.iconbitmap("inventory_icon.ico")
        except:
            pass
        
        # Create main UI components
        self.create_menu()
        self.create_main_frame()
        self.create_sidebar()
        self.create_statusbar()
        
        # Show dashboard by default
        self.show_dashboard()
    
    def create_menu(self):
        """Create the application main menu bar."""
        self.menu_bar = tk.Menu(self.master)
        
        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Backup Database", command=self.backup_database)
        file_menu.add_command(label="Restore Database", command=self.restore_database)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Preferences", command=self.show_preferences)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        # Reports menu
        reports_menu = tk.Menu(self.menu_bar, tearoff=0)
        reports_menu.add_command(label="Low Stock Report", command=lambda: self.show_reports("low_stock"))
        reports_menu.add_command(label="Sales Report", command=lambda: self.show_reports("sales"))
        reports_menu.add_command(label="Purchase Report", command=lambda: self.show_reports("purchase"))
        reports_menu.add_command(label="GST Report", command=lambda: self.show_reports("gst"))
        self.menu_bar.add_cascade(label="Reports", menu=reports_menu)
        
        # Help menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="User Guide", command=self.show_user_guide)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        
        self.master.config(menu=self.menu_bar)
    
    def create_main_frame(self):
        """Create the main content frame."""
        # Main frame to hold content
        self.main_frame = ttk.Frame(self.master, padding="10")
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Content frame will be replaced based on which section is active
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
    
    def create_sidebar(self):
        """Create the sidebar navigation menu."""
        # Sidebar frame
        self.sidebar = ttk.Frame(self.master, width=200, padding="10")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Style for the buttons
        style = ttk.Style()
        style.configure("Sidebar.TButton", font=("Arial", 11), padding=10, width=20)
        
        # Add sidebar buttons
        ttk.Label(self.sidebar, text="NAVIGATION", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        self.sidebar_buttons = []
        
        # Dashboard button
        dashboard_btn = ttk.Button(self.sidebar, text="Dashboard", style="Sidebar.TButton", 
                                  command=self.show_dashboard)
        dashboard_btn.pack(fill=tk.X, pady=5)
        self.sidebar_buttons.append(dashboard_btn)
        
        # Products button
        products_btn = ttk.Button(self.sidebar, text="Products", style="Sidebar.TButton", 
                                 command=self.show_products)
        products_btn.pack(fill=tk.X, pady=5)
        self.sidebar_buttons.append(products_btn)
        
        # Inventory button
        inventory_btn = ttk.Button(self.sidebar, text="Inventory", style="Sidebar.TButton", 
                                  command=self.show_inventory)
        inventory_btn.pack(fill=tk.X, pady=5)
        self.sidebar_buttons.append(inventory_btn)
        
        # Suppliers button
        suppliers_btn = ttk.Button(self.sidebar, text="Suppliers", style="Sidebar.TButton", 
                                  command=self.show_suppliers)
        suppliers_btn.pack(fill=tk.X, pady=5)
        self.sidebar_buttons.append(suppliers_btn)
        
        # Reports button
        reports_btn = ttk.Button(self.sidebar, text="Reports", style="Sidebar.TButton", 
                                command=lambda: self.show_reports("default"))
        reports_btn.pack(fill=tk.X, pady=5)
        self.sidebar_buttons.append(reports_btn)
        
        # Sales & Billing button
        billing_btn = ttk.Button(self.sidebar, text="Sales & Billing", style="Sidebar.TButton", 
                               command=self.show_billing)
        billing_btn.pack(fill=tk.X, pady=5)
        self.sidebar_buttons.append(billing_btn)
        
        # Settings button
        settings_btn = ttk.Button(self.sidebar, text="Settings", style="Sidebar.TButton", 
                                command=self.show_settings)
        settings_btn.pack(fill=tk.X, pady=5)
        self.sidebar_buttons.append(settings_btn)
        
        # Add logo or branding at the bottom
        ttk.Separator(self.sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(self.sidebar, text="IMS v1.0", font=("Arial", 8)).pack(side=tk.BOTTOM, pady=10)
    
    def create_statusbar(self):
        """Create the status bar at the bottom of the window."""
        self.status_bar = ttk.Frame(self.master, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_bar, text="Ready", padding=(5, 2))
        self.status_label.pack(side=tk.LEFT)
        
        # Display current date and time
        self.time_label = ttk.Label(self.status_bar, padding=(5, 2))
        self.time_label.pack(side=tk.RIGHT)
        self.update_time()
    
    def update_time(self):
        """Update the time display in the status bar."""
        current_time = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        self.time_label.config(text=current_time)
        # Update every second
        self.master.after(1000, self.update_time)
    
    def clear_content_frame(self):
        """Clear the content frame to prepare for new content."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def update_status(self, message):
        """Update the status bar message.
        
        Args:
            message (str): Status message to display
        """
        self.status_label.config(text=message)
    
    # Navigation methods
    def show_dashboard(self):
        """Display the dashboard screen."""
        self.clear_content_frame()
        self.update_status("Dashboard")
        
        # Dashboard title
        title_label = ttk.Label(self.content_frame, text="Dashboard", font=("Arial", 16, "bold"))
        title_label.pack(pady=10, anchor=tk.W)
        
        # Create dashboard content with multiple frames
        top_frame = ttk.Frame(self.content_frame)
        top_frame.pack(fill=tk.X, expand=False, pady=10)
        
        # Summary cards
        card_style = ttk.Style()
        card_style.configure("Card.TFrame", background="#ffffff", relief=tk.RAISED)
        
        # Total products card
        products_card = ttk.Frame(top_frame, style="Card.TFrame", padding=15)
        products_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Get product count from database
        product_count = len(self.db.get_all_products())
        
        ttk.Label(products_card, text="Total Products", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        ttk.Label(products_card, text=str(product_count), font=("Arial", 24)).pack(pady=10)
        
        # Low stock card
        lowstock_card = ttk.Frame(top_frame, style="Card.TFrame", padding=15)
        lowstock_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Get low stock count
        low_stock_count = len(self.db.get_low_stock_products())
        
        ttk.Label(lowstock_card, text="Low Stock Items", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        ttk.Label(lowstock_card, text=str(low_stock_count), font=("Arial", 24)).pack(pady=10)
        
        # Charts frame
        charts_frame = ttk.Frame(self.content_frame)
        charts_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # For demonstration, create a simple chart
        try:
            # Get all products
            products = self.db.get_all_products()
            
            # Create two chart frames
            left_chart_frame = ttk.Frame(charts_frame)
            left_chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            right_chart_frame = ttk.Frame(charts_frame)
            right_chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            # Product categories chart (left)
            ttk.Label(left_chart_frame, text="Products by Category", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=5)
            
            # Group by category (simplified for demo)
            categories = {}
            for product in products:
                category = product.get('category', 'Uncategorized')
                if category in categories:
                    categories[category] += 1
                else:
                    categories[category] = 1
            
            fig1, ax1 = plt.subplots(figsize=(5, 4))
            ax1.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            
            canvas1 = FigureCanvasTkAgg(fig1, left_chart_frame)
            canvas1.draw()
            canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Stock levels chart (right)
            ttk.Label(right_chart_frame, text="Stock Levels", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=5)
            
            # Take top 5 products by stock level
            products.sort(key=lambda x: x.get('quantity', 0), reverse=True)
            top_products = products[:5]
            
            fig2, ax2 = plt.subplots(figsize=(5, 4))
            ax2.bar([p.get('name', 'Unknown')[:10] for p in top_products], 
                   [p.get('quantity', 0) for p in top_products])
            ax2.set_xlabel('Products')
            ax2.set_ylabel('Quantity')
            ax2.set_title('Top 5 Products by Stock Level')
            plt.xticks(rotation=45)
            
            canvas2 = FigureCanvasTkAgg(fig2, right_chart_frame)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            ttk.Label(charts_frame, text=f"Error loading charts: {e}").pack()
        
        # Recent activities section
        activities_frame = ttk.Frame(self.content_frame)
        activities_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Label(activities_frame, text="Recent Activities", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=5)
        
        # Create a treeview for recent transactions
        columns = ('date', 'type', 'product', 'quantity')
        tree = ttk.Treeview(activities_frame, columns=columns, show='headings')
        
        # Define headings
        tree.heading('date', text='Date')
        tree.heading('type', text='Transaction Type')
        tree.heading('product', text='Product')
        tree.heading('quantity', text='Quantity')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(activities_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Sample data (in a real app, this would come from the database)
        sample_data = [
            (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "Purchase", "Laptop", "5"),
            (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "Sale", "Mobile Phone", "2"),
            (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "Stock Update", "Headphones", "10"),
        ]
        
        # Insert the data
        for item in sample_data:
            tree.insert('', tk.END, values=item)
    
    def show_products(self):
        """Display the products screen."""
        self.clear_content_frame()
        self.update_status("Products Management")
        
        # Products title
        title_label = ttk.Label(self.content_frame, text="Products Management", font=("Arial", 16, "bold"))
        title_label.pack(pady=10, anchor=tk.W)
        
        # Add product button
        add_button = ttk.Button(self.content_frame, text="Add New Product", command=self.add_product)
        add_button.pack(anchor=tk.W, pady=10)
        
        # Products table
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create Treeview with scrollbar
        columns = ('id', 'name', 'category', 'price', 'stock', 'reorder_level', 'gst_rate')
        self.products_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Define headings
        self.products_tree.heading('id', text='ID')
        self.products_tree.heading('name', text='Product Name')
        self.products_tree.heading('category', text='Category')
        self.products_tree.heading('price', text='Price (₹)')
        self.products_tree.heading('stock', text='Stock')
        self.products_tree.heading('reorder_level', text='Reorder Level')
        self.products_tree.heading('gst_rate', text='GST Rate (%)')
        
        # Define columns
        self.products_tree.column('id', width=50)
        self.products_tree.column('name', width=200)
        self.products_tree.column('category', width=150)
        self.products_tree.column('price', width=100)
        self.products_tree.column('stock', width=100)
        self.products_tree.column('reorder_level', width=100)
        self.products_tree.column('gst_rate', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind event for double click
        self.products_tree.bind("<Double-1>", self.edit_product)
        
        # Load products from database
        self.load_products()
    
    def show_inventory(self):
        """Display the inventory screen."""
        self.clear_content_frame()
        self.update_status("Inventory Management")
        
        # Placeholder implementation
        title_label = ttk.Label(self.content_frame, text="Inventory Management", font=("Arial", 16, "bold"))
        title_label.pack(pady=10, anchor=tk.W)
        
        ttk.Label(self.content_frame, text="This section will include inventory reports, stock adjustment, and inventory history.").pack(pady=20)
    
    def show_suppliers(self):
        """Display the suppliers screen."""
        self.clear_content_frame()
        self.update_status("Supplier Management")
        
        # Placeholder implementation
        title_label = ttk.Label(self.content_frame, text="Supplier Management", font=("Arial", 16, "bold"))
        title_label.pack(pady=10, anchor=tk.W)
        
        ttk.Label(self.content_frame, text="This section will include supplier information, purchase orders, and supplier contacts.").pack(pady=20)
    
    def show_billing(self):
        """Display the sales and billing screen."""
        self.clear_content_frame()
        self.update_status("Sales & Billing")
        
        # Placeholder implementation
        title_label = ttk.Label(self.content_frame, text="Sales & Billing", font=("Arial", 16, "bold"))
        title_label.pack(pady=10, anchor=tk.W)
        
        ttk.Label(self.content_frame, text="This section will include sales entry, GST invoice generation, and sales history.").pack(pady=20)
    
    def show_settings(self):
        """Display the settings screen."""
        self.clear_content_frame()
        self.update_status("Settings")
        
        # Placeholder implementation
        title_label = ttk.Label(self.content_frame, text="Settings", font=("Arial", 16, "bold"))
        title_label.pack(pady=10, anchor=tk.W)
        
        ttk.Label(self.content_frame, text="This section will include application settings, user preferences, and configuration options.").pack(pady=20)
    
    def backup_database(self):
        """Backup the database to a file"""
        backup_file = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")],
            title="Backup Database"
        )
        if backup_file:
            try:
                import shutil
                shutil.copy2('inventory.db', backup_file)
                messagebox.showinfo("Success", "Database backup created successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create backup: {e}")

    def restore_database(self):
        """Restore the database from a backup file"""
        backup_file = filedialog.askopenfilename(
            filetypes=[("Database files", "*.db"), ("All files", "*.*")],
            title="Restore Database"
        )
        if backup_file:
            try:
                self.db.close()  # Close current connection
                import shutil
                shutil.copy2(backup_file, 'inventory.db')
                messagebox.showinfo("Success", "Database restored successfully!")
                messagebox.showinfo("Restart Required", "Please restart the application to complete restoration.")
                self.master.quit()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to restore backup: {e}")

    def show_preferences(self):
        """Show preferences dialog"""
        preferences_window = tk.Toplevel(self.master)
        preferences_window.title("Preferences")
        preferences_window.geometry("400x300")
        
        # Add some sample preferences
        ttk.Label(preferences_window, text="Application Preferences", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(preferences_window, text="Currently no configurable preferences", font=("Arial", 10)).pack(pady=20)

    def show_reports(self, report_type="default"):
        """Show reports window
        
        Args:
            report_type (str): Type of report to show
        """
        reports_window = tk.Toplevel(self.master)
        reports_window.title(f"Reports - {report_type.title()}")
        reports_window.geometry("600x400")
        
        # Add report content based on type
        if report_type == "low_stock":
            self.show_low_stock_report(reports_window)
        elif report_type == "sales":
            self.show_sales_report(reports_window)
        elif report_type == "purchase":
            self.show_purchase_report(reports_window)
        elif report_type == "gst":
            self.show_gst_report(reports_window)
        else:
            self.show_default_report(reports_window)

    def show_user_guide(self):
        """Show user guide window"""
        guide_window = tk.Toplevel(self.master)
        guide_window.title("User Guide")
        guide_window.geometry("600x400")
        
        # Add user guide content
        text = tk.Text(guide_window, wrap=tk.WORD, padx=10, pady=10)
        text.pack(fill=tk.BOTH, expand=True)
        
        guide_content = """
        Inventory Management System User Guide

        1. Dashboard
           - View summary of inventory status
           - Check low stock alerts
           - View recent activities

        2. Products
           - Add new products
           - Edit existing products
           - Delete products
           - Manage product categories

        3. Inventory
           - Update stock levels
           - View stock history
           - Set reorder levels

        4. Reports
           - Generate various reports
           - Export data
           - View sales and purchase history

        5. GST Handling
           - Set GST rates
           - Generate GST reports
           - Track GST payments
        """
        
        text.insert(tk.END, guide_content)
        text.config(state=tk.DISABLED)

    def show_about(self):
        """Show about dialog"""
        about_text = """
        Inventory Management System
        Version 1.0

        A comprehensive inventory management solution
        designed for small businesses in the Indian market.

        Features:
        - Product Management
        - Stock Tracking
        - GST Handling
        - Sales and Purchase Management
        - Reports and Analytics

        © 2024 All rights reserved.
        """
        messagebox.showinfo("About", about_text)

    # Helper methods for the report windows
    def show_low_stock_report(self, parent_window):
        """Show low stock report content in the given window"""
        ttk.Label(parent_window, text="Low Stock Report", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Get low stock products
        low_stock_products = self.db.get_low_stock_products()
        
        if not low_stock_products:
            ttk.Label(parent_window, text="No low stock items found").pack(pady=20)
            return
            
        # Create treeview
        columns = ('id', 'name', 'current_stock', 'reorder_level')
        tree = ttk.Treeview(parent_window, columns=columns, show='headings')
        
        tree.heading('id', text='ID')
        tree.heading('name', text='Product Name')
        tree.heading('current_stock', text='Current Stock')
        tree.heading('reorder_level', text='Reorder Level')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Insert data
        for product in low_stock_products:
            tree.insert('', tk.END, values=(
                product.get('id', ''),
                product.get('name', ''),
                product.get('quantity', 0),
                product.get('reorder_level', 0)
            ))
            
    def show_sales_report(self, parent_window):
        """Show sales report in the given window"""
        ttk.Label(parent_window, text="Sales Report", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(parent_window, text="Sales report will be implemented here").pack(pady=20)
        
    def show_purchase_report(self, parent_window):
        """Show purchase report in the given window"""
        ttk.Label(parent_window, text="Purchase Report", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(parent_window, text="Purchase report will be implemented here").pack(pady=20)
        
    def show_gst_report(self, parent_window):
        """Show GST report in the given window"""
        ttk.Label(parent_window, text="GST Report", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(parent_window, text="GST report will be implemented here").pack(pady=20)

    def show_default_report(self, parent_window):
        """Show default report selection screen"""
        ttk.Label(parent_window, text="Reports", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Create buttons for different reports
        ttk.Button(parent_window, text="Low Stock Report", 
                command=lambda: self.show_low_stock_report(parent_window)).pack(pady=5)
        ttk.Button(parent_window, text="Sales Report", 
                command=lambda: self.show_sales_report(parent_window)).pack(pady=5)
        ttk.Button(parent_window, text="Purchase Report", 
                command=lambda: self.show_purchase_report(parent_window)).pack(pady=5)
        ttk.Button(parent_window, text="GST Report", 
                command=lambda: self.show_gst_report(parent_window)).pack(pady=5)

    def load_products(self):
        """Load products into the products treeview"""
        # Clear existing items
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Get products from database
        products = self.db.get_all_products()
        
        # Insert products into treeview
        for product in products:
            self.products_tree.insert('', tk.END, values=(
                product.get('id', ''),
                product.get('name', ''),
                product.get('category', ''),
                product.get('selling_price', ''),
                product.get('quantity', 0),
                10,  # Default reorder level
                product.get('gst_percentage', 18)
            ))

    def add_product(self):
        """Show dialog to add a new product"""
        dialog = tk.Toplevel(self.master)
        dialog.title("Add New Product")
        dialog.geometry("400x500")
        dialog.transient(self.master)
        dialog.grab_set()
        
        # Create and pack widgets
        ttk.Label(dialog, text="Add New Product", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Product details frame
        details_frame = ttk.Frame(dialog)
        details_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Product Name
        ttk.Label(details_frame, text="Product Name:").pack(anchor=tk.W)
        name_entry = ttk.Entry(details_frame)
        name_entry.pack(fill=tk.X, pady=5)
        
        # Category
        ttk.Label(details_frame, text="Category:").pack(anchor=tk.W)
        category_combo = ttk.Combobox(details_frame)
        categories = [cat['name'] for cat in self.db.get_all_categories()]
        category_combo['values'] = categories
        category_combo.pack(fill=tk.X, pady=5)
        
        # Cost Price
        ttk.Label(details_frame, text="Cost Price (₹):").pack(anchor=tk.W)
        cost_entry = ttk.Entry(details_frame)
        cost_entry.pack(fill=tk.X, pady=5)
        
        # Selling Price
        ttk.Label(details_frame, text="Selling Price (₹):").pack(anchor=tk.W)
        price_entry = ttk.Entry(details_frame)
        price_entry.pack(fill=tk.X, pady=5)
        
        # GST Rate
        ttk.Label(details_frame, text="GST Rate (%):").pack(anchor=tk.W)
        gst_entry = ttk.Entry(details_frame)
        gst_entry.insert(0, "18")  # Default GST rate
        gst_entry.pack(fill=tk.X, pady=5)
        
        # Initial Stock
        ttk.Label(details_frame, text="Initial Stock:").pack(anchor=tk.W)
        stock_entry = ttk.Entry(details_frame)
        stock_entry.insert(0, "0")
        stock_entry.pack(fill=tk.X, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Button(button_frame, text="Cancel", 
                command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Add Product", 
                command=lambda: self.save_new_product(
                    name_entry.get(),
                    category_combo.get(),
                    cost_entry.get(),
                    price_entry.get(),
                    gst_entry.get(),
                    stock_entry.get(),
                    dialog
                )).pack(side=tk.RIGHT, padx=5)

    def save_new_product(self, name, category, cost_price, selling_price, gst_rate, initial_stock, dialog):
        """Save a new product to the database"""
        try:
            # Validate inputs
            if not all([name, category, cost_price, selling_price, gst_rate, initial_stock]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            cost_price = float(cost_price)
            selling_price = float(selling_price)
            gst_rate = float(gst_rate)
            initial_stock = int(initial_stock)
            
            # Add product to database
            product_id = self.db.add_product(
                name=name,
                description="",  # Empty description for now
                category_id=1,  # Get proper category ID in real implementation
                supplier_id=1,  # Get proper supplier ID in real implementation
                cost_price=cost_price,
                selling_price=selling_price,
                gst_percentage=gst_rate,
                hsn_code="",  # Empty HSN code for now
                initial_stock=initial_stock
            )
            
            if product_id:
                messagebox.showinfo("Success", "Product added successfully!")
                self.load_products()  # Refresh products list
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to add product")
                
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numbers for prices, GST rate, and stock")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {e}")

    def edit_product(self, event):
        """Handle double-click event on product in treeview"""
        item = self.products_tree.selection()[0]
        product_id = self.products_tree.item(item)['values'][0]
        # Get product details and show edit dialog
        product = self.db.get_product(product_id)
        if product:
            self.show_edit_product_dialog(product)
