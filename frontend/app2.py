import tkinter as tk
import ttkbootstrap as tb
# Fix 1: Updated import path
from ttkbootstrap.tableview import Tableview 
from ttkbootstrap.constants import *
import requests
import os

API_URL = "http://127.0.0.1:8000/api/items/"

class POSApp(tb.Window):
    def __init__(self):
        # Initialize the window first
        super().__init__(themename="cosmo", title="Modern POS System")
        self.geometry("1100x700")
        
        self.cart = []
        
        # Fix 2: Ensure UI is built fully before calling load_items
        self.setup_ui()
        self.load_items()

    def setup_ui(self):
        # --- Sidebar / CRUD Form ---
        sidebar = tb.Frame(self, padding=20, width=200)
        sidebar.pack(side=LEFT, fill=Y)

        tb.Label(sidebar, text="Manage Inventory", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # tb.Label(sidebar, text="Item Name:").pack(anchor=W)
        # self.name_ent = tb.Entry(sidebar)
        # self.name_ent.pack(fill=X, pady=5)

        # tb.Label(sidebar, text="Price:").pack(anchor=W)
        # self.price_ent = tb.Entry(sidebar)
        # self.price_ent.pack(fill=X, pady=5)

        # tb.Label(sidebar, text="Stock:").pack(anchor=W)
        # self.stock_ent = tb.Entry(sidebar)
        # self.stock_ent.pack(fill=X, pady=5)

        # tb.Button(sidebar, text="Add Item", bootstyle=SUCCESS, command=self.add_item).pack(fill=X, pady=10)
        
        # --- Main Table Area ---
        main_frame = tb.Frame(self, padding=20)
        main_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Define columns for Tableview
        coldata = [
            {"text": "ID", "stretch": False},
            {"text": "Item Name", "stretch": True},
            {"text": "Price", "stretch": True},
            {"text": "Stock", "stretch": True},
        ]
        
        # Fix 3: Standard initialization of Tableview
        self.table = Tableview(
            master=main_frame,
            coldata=coldata,
            rowdata=[],
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
        )
        self.table.pack(fill=BOTH, expand=True)
        
        # Action Buttons
        btn_frame = tb.Frame(main_frame)
        btn_frame.pack(fill=X, pady=10)
        tb.Button(btn_frame, text="Add to Cart", bootstyle=INFO, command=self.add_to_cart).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Print Invoice", bootstyle=DARK, command=self.generate_invoice).pack(side=RIGHT, padx=5)

        # Cart display (simple listbox for demonstration)
        #label for cart
        # tb.Label(sidebar, text="Shopping Cart", font=("Helvetica", 16, "bold")).pack(pady=10)
        # self.cart_listbox = tk.Listbox(sidebar)
        # self.cart_listbox.pack(fill=BOTH, expand=True, pady=10)
        # Cart Display Table View 
        cart_coldata = [
            {"text": "Item Name", "stretch": True},
            {"text": "Price", "stretch": True},
            {"text": "Quantity", "stretch": True},
            {"text": "Total", "stretch": True},
        ]
        cart_rowdata = []
        self.cart_table = Tableview(
            master=sidebar,
            coldata=cart_coldata,
            rowdata=cart_rowdata,
            paginated=False,
            searchable=False,
            bootstyle=WARNING,
            
        )
        self.cart_table.pack(fill=BOTH, expand=True, pady=10)
        


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
                    {"text": "Stock", "stretch": True}
                ], rowdata=rows)
                
            else:
                print(f"Backend returned error: {response.status_code}")
        except Exception as e:
            print(f"Error connecting to Backend: {e}")
                
                
        except Exception as e:
            print(f"Error connecting to Backend: {e}")

    def add_item(self):
        try:
            payload = {
                "name": self.name_ent.get(),
                "price": float(self.price_ent.get()),
                "stock": int(self.stock_ent.get())
            }
            requests.post(API_URL, json=payload)
            self.load_items()
            # Clear entries after adding
            self.name_ent.delete(0, END)
            self.price_ent.delete(0, END)
            self.stock_ent.delete(0, END)
        except ValueError:
            print("Please enter valid price and stock numbers.")

    def add_to_cart(self):
        # Access the underlying ttk.Treeview selection
        selected_items = self.table.view.selection()
        
        if not selected_items:
            print("No item selected!")
            return

        for iid in selected_items:
            # Get the values for the specific row ID
            row_values = self.table.view.item(iid, "values")
            self.cart.append(row_values)
            print(f"Added to cart: {row_values[1]}")
            print(f"Added to cart: {row_values[2]}")
            # Insert row_values into cart_table
            insert_data = [row_values[1], row_values[2], 1, float(row_values[2])]
            print(f"Insert data: {insert_data}")
            # update data in cart table
            self.cart_table._build_table_rows(rowdata=[insert_data])
            
            

    def generate_invoice(self):
        if not self.cart:
            print("Cart is empty!")
            return
        
        invoice_content = "--- POS INVOICE ---\n"
        total = 0
        for item in self.cart:
            invoice_content += f"{item[1]} - ${item[2]}\n"
            total += float(item[2])
        
        invoice_content += f"\nTOTAL: ${total:.2f}"
        
        file_path = "invoice.txt"
        with open(file_path, "w") as f:
            f.write(invoice_content)
        
        print("Invoice Generated. Printing...")
        if os.name == 'nt':
            os.startfile(file_path, "print")
        else:
            os.system(f"lpr {file_path}")
        
        self.cart = [] 
        #clear cart table
        self.cart_table.delete_rows()
        

if __name__ == "__main__":
    app = POSApp()
    app.mainloop()