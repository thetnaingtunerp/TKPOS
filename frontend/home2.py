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
        # Main Frame
        mainframe = tb.Frame(self, padding=10)
        mainframe.grid(row=0, column=0, sticky="nsew")

        # Make window responsive
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        mainframe.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=2)  # Items
        mainframe.columnconfigure(1, weight=1)  # Cart

        # =========================
        # LEFT: ITEM TABLE
        # =========================
        coldata = [
            {"text": "ID", "stretch": False},
            {"text": "Item Name", "stretch": True},
            {"text": "Price", "stretch": True},
            {"text": "Quantity", "stretch": True},
        ]

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
        self.table.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.table.view.bind("<Double-1>", self.on_double_click)

        # =========================
        # RIGHT: CART
        # =========================
        cart_frame = tb.Frame(mainframe, padding=10)
        cart_frame.grid(row=0, column=1, sticky="nsew")

        cart_frame.rowconfigure(0, weight=1)  # table grows
        for i in range(1, 7):
            cart_frame.rowconfigure(i, weight=0)

        cart_frame.columnconfigure(0, weight=1)

        # tb.Label(cart_frame, text="Cart", font=("Helvetica", 16, "bold")).grid(
        #     row=0, column=0, sticky="w", pady=5
        # )

        # Cart Table
        cart_coldata = [
            {"text": "Item Name", "stretch": True},
            {"text": "Price", "stretch": True},
            {"text": "Quantity", "stretch": True},
            {"text": "Total", "stretch": True},
        ]

        self.cart_table = Tableview(
            master=cart_frame,
            coldata=cart_coldata,
            rowdata=[],
            paginated=False,
            searchable=False,
            bootstyle=SUCCESS,
        )
        self.cart_table.grid(row=1, column=0, sticky="nsew", pady=5)

        # TOTALS
        self.total_label = tb.Label(cart_frame, text="Total: $0.00", font=("Helvetica", 12, "bold"))
        self.total_label.grid(row=2, column=0, sticky="e", pady=5)

        # Discount + Delivery (Responsive row)
        form_frame = tb.Frame(cart_frame)
        form_frame.grid(row=3, column=0, sticky="ew", pady=5)

        form_frame.columnconfigure((0, 1, 2, 3), weight=1)

        tb.Label(form_frame, text="Discount %").grid(row=0, column=0, sticky="w")
        self.discount_entry = tb.Entry(form_frame)
        self.discount_entry.grid(row=0, column=1, sticky="ew", padx=5)

        tb.Label(form_frame, text="Delivery $").grid(row=0, column=2, sticky="w")
        self.delivery_entry = tb.Entry(form_frame)
        self.delivery_entry.grid(row=0, column=3, sticky="ew", padx=5)

        self.final_total_label = tb.Label(cart_frame, text="Final Total: $0.00", font=("Helvetica", 12, "bold"))
        self.final_total_label.grid(row=4, column=0, sticky="e", pady=5)

        # Description (FIXED → RESPONSIVE)
        self.description_entry = tk.Text(cart_frame, height=3)
        self.description_entry.grid(row=5, column=0, sticky="nsew", pady=5)

        cart_frame.rowconfigure(5, weight=1)  # allow expand

        # Buttons
        action_frame = tb.Frame(cart_frame)
        action_frame.grid(row=6, column=0, sticky="ew", pady=5)

        action_frame.columnconfigure((0, 1, 2), weight=1)

        tb.Button(action_frame, text="Apply", bootstyle=INFO).grid(row=0, column=0, sticky="ew", padx=2)
        tb.Button(action_frame, text="Clear", bootstyle=DANGER).grid(row=0, column=1, sticky="ew", padx=2)
        tb.Button(action_frame, text="Print", bootstyle=DARK).grid(row=0, column=2, sticky="ew", padx=2)
            
            
        
        
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