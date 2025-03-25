#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for the Inventory Management System
Initializes the database and launches the GUI application
"""

import os
import sys
import logging
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Import custom modules
from inventory_manager import InventoryDatabase
from gui_manager import InventoryManagementSystem

# Configure logging
def setup_logging():
    """Configure application logging"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f"inventory_app_{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger('InventoryApp')

# Check and initialize database
def initialize_database():
    """Check if database exists and initialize it if needed"""
    logger.info("Checking database...")
    db_file = "inventory.db"
    db_exists = os.path.exists(db_file)
    
    try:
        # Create database connection
        db_manager = InventoryDatabase(db_file)
        
        if not db_exists:
            logger.info("Database not found. Creating new database...")
            # Initialize database tables
            db_manager.create_tables()
            logger.info("Database initialized successfully.")
            
            # Add some default categories for Indian market
            default_categories = [
                "Groceries", "Electronics", "Clothing", "Stationery", 
                "Home Appliances", "Mobile Accessories", "Kitchen Items",
                "Beauty Products", "FMCG", "Hardware"
            ]
            for category in default_categories:
                db_manager.add_category(category)
            logger.info("Default categories added.")
        else:
            logger.info("Database already exists.")
        
        return db_manager
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        messagebox.showerror("Database Error", f"Failed to initialize database: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        sys.exit(1)

# Main function
def main():
    """Main entry point for the application"""
    try:
        # Initialize database
        db_manager = initialize_database()
        
        # Create root window
        root = tk.Tk()
        root.title("Inventory Management System")
        
        # Get screen dimensions and set window size to 80% of screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        
        # Center the window
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        
        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        
        # Create application instance
        app = InventoryManagementSystem(root, db_manager)
        
        logger.info("Application started successfully.")
        
        # Start the main loop
        root.mainloop()
        
    except Exception as e:
        logger.critical(f"Application failed to start: {e}", exc_info=True)
        messagebox.showerror("Critical Error", f"Application failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Setup logging
    logger = setup_logging()
    logger.info("Starting Inventory Management System...")
    
    # Run main function
    main()

