import tkinter as tk
import ttkbootstrap as tb
# Fix 1: Updated import path
from ttkbootstrap.tableview import Tableview 
from ttkbootstrap.constants import *
import requests
import os
#messagebox import
from tkinter import messagebox


class POSApp(tb.Window):
    def __init__(self):
        # Initialize the window first
        super().__init__(themename="cosmo", title="Modern POS System")
        self.geometry("1100x700")
        
        self.cart = []
        
        # Fix 2: Ensure UI is built fully before calling load_items
        self.setup_ui()
        # self.load_items()
    def setup_ui(self):
        # --- row 1 ---
        mainframe = tb.Frame(self, padding=20)
        mainframe.grid(row=0, column=0, rowspan=2, columnspan=3, sticky="nsew")
        # column 1
        # --- Item Table ---
        coldata = [
            {"text": "ID", "stretch": False},
            {"text": "Item Name", "stretch": True},
            {"text": "Price", "stretch": True},
            {"text": "Quantity", "stretch": True},
        ]
        #sample row data with input field for quantity
        rowdata = [
            [1, "Item A", "$10.00", "1"],
            [2, "Item B", "$15.00", "1"],
            [3, "Item C", "$20.00", "1"],
            [4, "Item D", "$25.00", "1"],
        ]
        
        self.table = Tableview(
            master=mainframe,
            coldata=coldata,
            rowdata=rowdata,
            paginated=False,
            searchable=True,
            bootstyle=PRIMARY,
        )
        self.table.grid(row=0, column=0, sticky="nsew")
        
        # Bind Double Click to view Entry widget in the selected row
        self.table.view.bind("<Double-1>", self.on_double_click)
        
        # column 2
        # --- Cart Area ---
        cart_frame = tb.Frame(mainframe, padding=10)
        cart_frame.grid(row=0, column=1, sticky="nsew")
        tb.Label(cart_frame, text="Cart", font=("Helvetica", 16, "bold")).grid(row=0, column=0, pady=10)    
        # Cart Table
        cart_coldata = [
            {"text": "Item Name", "stretch": True},
            {"text": "Price", "stretch": True},
            {"text": "Quantity", "stretch": True},
            {"text": "Total", "stretch": True},
        ]
        
        #sample row data for cart
        cart_rowdata = [
            ["Item A", "$10.00", "1", "$10.00"],
            ["Item B", "$15.00", "2", "$30.00"],
            ["Item B", "$15.00", "2", "$30.00"],
            ["Item B", "$15.00", "2", "$30.00"],
            ["Item B", "$15.00", "2", "$30.00"],
            ["Item B", "$15.00", "2", "$30.00"],
            ["Item B", "$15.00", "2", "$30.00"],
            ["Item B", "$15.00", "2", "$30.00"],
            ["Item B", "$15.00", "2", "$30.00"],
            ["Item B", "$15.00", "2", "$30.00"],
            ["Item B", "$15.00", "2", "$30.00"],
            ["Item B", "$15.00", "2", "$30.00"],
            ["Item B", "$15.00", "2", "$30.00"],
            ["Item d", "$15.00", "2", "$30.00"],
        ]
        
        self.cart_table = Tableview(
            master=cart_frame,
            coldata=cart_coldata,
            rowdata=cart_rowdata,
            paginated=False,
            searchable=False,
            bootstyle=SUCCESS,
        )
        self.cart_table.grid(row=0, column=0, sticky="nsew")
        
        # Total Price Label
        self.total_label = tb.Label(cart_frame, text="Total: $0.00", font=("Helvetica", 14, "bold"))
        self.total_label.grid(row=1, column=0, pady=10, sticky="e")
        
        # Discount Entry
        discount_frame = tb.Frame(cart_frame)
        discount_frame.grid(row=2, column=0, pady=10, sticky="e")
        tb.Label(discount_frame, text="Discount (%):").pack(side=LEFT)
        self.discount_entry = tk.Entry(discount_frame, width=10)
        self.discount_entry.pack(side=LEFT, padx=5)
        
        # Delivery Charge Entry
        delivery_frame = tb.Frame(cart_frame)
        delivery_frame.grid(row=3, column=0, pady=10, sticky="e")
        tb.Label(delivery_frame, text="Delivery Charge ($):").pack(side=LEFT)
        self.delivery_entry = tk.Entry(delivery_frame, width=10)
        self.delivery_entry.pack(side=LEFT, padx=5)
        
        # Total - After Discount and Delivery Charge Label
        self.final_total_label = tb.Label(cart_frame, text="Final Total: $0.00", font=("Helvetica", 14, "bold"))
        self.final_total_label.grid(row=4, column=0, pady=10, sticky="e")
        
        
        # Description Entry
        description_frame = tb.Frame(cart_frame)
        description_frame.grid(row=5, column=0, pady=10, sticky="e")
        tb.Label(description_frame, text="Description:").pack(side=LEFT)
        self.description_entry = tk.Text(description_frame, width=100, height=4)
        self.description_entry.pack(side=LEFT, padx=5)
        
        # Action Buttons : Apply Discount, Clear Cart, Print Invoice
        action_frame = tb.Frame(cart_frame)
        action_frame.grid(row=6, column=0, pady=10, sticky="e")
        tb.Button(action_frame, text="Apply Discount & Delivery", bootstyle=INFO).pack(side=LEFT, padx=5)
        tb.Button(action_frame, text="Clear Cart", bootstyle=DANGER).pack(side=LEFT, padx=5)
        tb.Button(action_frame, text="Print Invoice", bootstyle=DARK).pack(side=LEFT, padx=5)
        
        
        
        
        
        
    def on_double_click(self, event):
        # Get Item Id from the selected row
        selected_item = self.table.view.focus()
        item_values = self.table.view.item(selected_item, "values")
        if item_values:
            item_id = item_values[0]  # Assuming ID is in the first column
            print(f"Double-clicked on Item ID: {item_id}")
            # Entry Widget can be created here to input quantity for the selected item
            input_entry = tk.Entry(self.table.view)
            input_entry.insert(0, "1")  # Default quantity
            input_entry.focus()
            # Place the Entry widget over the selected row
            bbox = self.table.view.bbox(selected_item, column=3)  # Get bounding box of the fourth column
            if bbox:
                x, y, width, height = bbox
                input_entry.place(x=x, y=y, width=width, height=height)
            
            #When the user presses Enter, we can capture the input and print it
            def on_enter(event):
                quantity = input_entry.get()
                print(f"Input Quantity for Item ID {item_id}: {quantity}")
                input_entry.destroy()  # Remove the Entry widget after capturing input
            # print("Input Number is :", input_entry.get())
            input_entry.bind("<Return>", on_enter)
            
            
            

        


if __name__ == "__main__":
    app = POSApp()
    
    app.mainloop()