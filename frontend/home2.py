import tkinter as tk
import ttkbootstrap as tb
# Fix 1: Updated import path
from ttkbootstrap.tableview import Tableview 
from ttkbootstrap.constants import *
import requests
import os
#messagebox import
from tkinter import messagebox

#Font import
from tkinter import font




API_URL = "http://127.0.0.1:8000/api/items/"

class POSApp(tb.Window):
    def __init__(self):
        # Initialize the window first
        super().__init__(themename="cosmo", title="Modern POS System")
        self.geometry("1100x700")
        
        self.cart = []
        self.create_menu()
        
        # Fix 2: Ensure UI is built fully before calling load_items
        self.setup_ui()
        self.load_items()
        
    def create_menu(self):
        menubar = tk.Menu(self)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.menu_open)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit_app)
        menubar.add_cascade(label="File", menu=file_menu)

        # Report Menu
        report_menu = tk.Menu(menubar, tearoff=0)
        report_menu.add_command(label="Sales Report", command=self.menu_report)
        menubar.add_cascade(label="Report", menu=report_menu)

        # Exit Menu (optional as separate top-level)
        menubar.add_command(label="Exit", command=self.quit_app)

        self.config(menu=menubar)   
        
    def menu_open(self):
        messagebox.showinfo("Open", "Open File clicked")
        
    def quit_app(self):
        self.destroy()
        
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

        tb.Label(form_frame, text="Discount").grid(row=0, column=0, sticky="w")
        self.discount_entry = tb.Entry(form_frame)
        self.discount_entry.grid(row=0, column=1, sticky="ew", padx=5)

        tb.Label(form_frame, text="Delivery Charge").grid(row=0, column=2, sticky="w")
        self.delivery_entry = tb.Entry(form_frame)
        self.delivery_entry.grid(row=0, column=3, sticky="ew", padx=5)
        # Default values for discount and delivery
        self.discount_entry.insert(0, "0")
        self.delivery_entry.insert(0, "0")

        self.final_total_label = tb.Label(cart_frame, text="Final Total: $0.00", font=("Helvetica", 12, "bold"))
        self.final_total_label.grid(row=4, column=0, sticky="e", pady=5)

        # Description (FIXED → RESPONSIVE)
        self.description_entry = tk.Text(cart_frame, height=3, highlightthickness=2, highlightbackground="#131ae5", font=("Myanmar Text", 12)) 
        self.description_entry.grid(row=5, column=0, sticky="nsew", pady=5)
        # allow copy paste in description entry
        # self.description_entry.bind("<Control-c>", lambda e: self.description_entry.event_generate("<<Copy>>"))
        # self.description_entry.bind("<Control-v>", lambda e: self.description_entry.event_generate("<<Paste>>"))
        
        

        cart_frame.rowconfigure(5, weight=1)  # allow expand

        # Buttons
        action_frame = tb.Frame(cart_frame)
        action_frame.grid(row=6, column=0, sticky="ew", pady=5)

        action_frame.columnconfigure((0, 1, 2), weight=1)

        tb.Button(action_frame, text="Apply", bootstyle=INFO, command=self.apply_discount_delivery).grid(row=0, column=0, sticky="ew", padx=2)
        tb.Button(action_frame, text="Clear", bootstyle=DANGER, command=self.clear_cart_table).grid(row=0, column=1, sticky="ew", padx=2)
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
                # item_values add to cart table with the input quantity
                item_name = item_values[1]
                item_price = item_values[2]
                total_price = float(item_price.replace("", "")) * int(quantity)
                self.cart_table._build_table_rows(rowdata=[[item_name, item_price, quantity, f"{total_price:.2f}"]])
                # self.update_totals()
                
                input_entry.destroy()  # Remove the Entry widget after capturing input
            # print("Input Number is :", input_entry.get())
            input_entry.bind("<Return>", on_enter)
    
    def apply_discount_delivery(self):
        try:
            discount_percent = float(self.discount_entry.get())
            delivery_charge = float(self.delivery_entry.get())

            print(f"Applying Discount: {discount_percent}%, Delivery Charge: {delivery_charge:.2f}")

            total = 0.0

            # ✅ Correct way: loop through Treeview rows
            for item_id in self.cart_table.view.get_children():
                row = self.cart_table.view.item(item_id, "values")
                total += float(row[3].replace("", ""))

            print(f"Calculated Total: ${total:.2f}")

            # Apply discount
            # discount_amount = total * (discount_percent / 100)
            final_total = total - discount_percent + delivery_charge

            # Update UI
            self.total_label.config(text=f"Total: {total:.2f}")
            self.final_total_label.config(text=f"Final Total: {final_total:.2f}")

        except Exception as e:
            print(f"Error calculating totals: {e}")
    
    
    def clear_cart_table(self):
        # Clear all rows from the cart table
        for item_id in self.cart_table.view.get_children():
            self.cart_table.view.delete(item_id)
        # Reset totals
        self.total_label.config(text="Total: $0.00")
        self.final_total_label.config(text="Final Total: $0.00")
    
    #============================
    # Load Items from Backend API
    #============================
    def load_items(self):
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                data = response.json()
                
                # 1. Format the data into a list of tuples or lists
                rows = [[item['id'], item['name'], item['price'], item['stock']] for item in data]
                
                # 2. Use build_table_data to update the UI
                # You must provide the original columns (coldata) and the new rows
                self.table.build_table_data(coldata=[
                    {"text": "ID", "stretch": False},
                    {"text": "Item Name", "stretch": True},
                    {"text": "Price", "stretch": True},
                    {"text": "Quantity", "stretch": True}
                ], rowdata=rows)
                
            else:
                print(f"Backend returned error: {response.status_code}")
        except Exception as e:
            print(f"Error fetching items: {e}")
    
            
    #============================
    # Report Generation Logic
    #============================
    def menu_report(self):
        self.open_report_window()
    
    def open_report_window(self):
        report_win = tb.Toplevel(self)
        report_win.title("Sales Report")
        report_win.geometry("1000x600")

        report_frame = tb.Frame(report_win, padding=10)
        report_frame.pack(fill="both", expand=True)

        # Columns
        coldata = [
            {"text": "Invoice ID", "stretch": True},
            {"text": "Date", "stretch": True},
            {"text": "Total Amount", "stretch": True},
            {"text": "Discount", "stretch": True},
            {"text": "Final Total", "stretch": True},
        ]

        # Sample Data
        rowdata = [
            [101, "2024-01-01", "$100.00", "10%", "$90.00"],
            [102, "2024-01-02", "$150.00", "5%", "$142.50"],
            [103, "2024-01-03", "$200.00", "0%", "$200.00"],
        ]

        self.report_table = Tableview(
            master=report_frame,
            coldata=coldata,
            rowdata=rowdata,
            paginated=True,
            searchable=True,
            bootstyle=INFO,
        )

        self.report_table.pack(fill="both", expand=True)
            
            
            

        


if __name__ == "__main__":
    app = POSApp()
    
    
    app.mainloop()