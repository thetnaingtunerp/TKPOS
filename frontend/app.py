import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import requests

API_URL = "http://127.0.0"

class CRUDApp(tb.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Django-Tkinter CRUD Pro")
        self.geometry("700x500")

        self.selected_id = None
        self.name_var = tk.StringVar()
        self.desc_var = tk.StringVar()

        container = tb.Frame(self, padding=20)
        container.pack(fill=BOTH, expand=YES)

        # Inputs
        tb.Label(container, text="Name:").pack(anchor=W)
        tb.Entry(container, textvariable=self.name_var).pack(fill=X, pady=5)
        tb.Label(container, text="Description:").pack(anchor=W)
        tb.Entry(container, textvariable=self.desc_var).pack(fill=X, pady=5)

        # Buttons
        btn_frame = tb.Frame(container)
        btn_frame.pack(pady=15)
        
        tb.Button(btn_frame, text="Add New", bootstyle=SUCCESS, command=self.create_item).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Update", bootstyle=WARNING, command=self.update_item).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Delete", bootstyle=DANGER, command=self.delete_item).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Refresh", bootstyle=INFO, command=self.load_data).pack(side=LEFT, padx=5)

        # Treeview (Table)
        self.tree = tb.Treeview(container, columns=("id", "name", "desc"), show="headings", height=8)
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("desc", text="Description")
        self.tree.column("id", width=50)
        self.tree.pack(fill=BOTH, expand=YES)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.load_data()

    def load_data(self):
        """API မှ data များဆွဲထုတ်ပြီး Table ထဲပြခြင်း"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            response = requests.get(API_URL)
            for item in response.json():
                self.tree.insert("", END, values=(item['id'], item['name'], item['description']))
        except:
            messagebox.showerror("Error", "Backend server မပွင့်သေးပါ")

    def on_select(self, event):
        """Table ထဲက တစ်ခုကိုနှိပ်လိုက်ရင် Input box ထဲ data ထည့်ပေးခြင်း"""
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            self.selected_id = values[0]
            self.name_var.set(values[1])
            self.desc_var.set(values[2])

    def create_item(self):
        data = {"name": self.name_var.get(), "description": self.desc_var.get()}
        res = requests.post(API_URL, json=data)
        if res.status_code == 201:
            self.load_data()
            self.clear_form()

    def update_item(self):
        if not self.selected_id:
            return messagebox.showwarning("Warning", "ပြင်ချင်တဲ့ item ကို အရင်ရွေးပါ")
        
        data = {"name": self.name_var.get(), "description": self.desc_var.get()}
        res = requests.put(f"{API_URL}{self.selected_id}/", json=data)
        if res.status_code == 200:
            self.load_data()
            self.clear_form()
            messagebox.showinfo("Success", "Updated successfully")

    def delete_item(self):
        if not self.selected_id:
            return messagebox.showwarning("Warning", "ဖျက်ချင်တဲ့ item ကို အရင်ရွေးပါ")
        
        confirm = messagebox.askyesno("Confirm", "တကယ်ဖျက်မှာလား?")
        if confirm:
            res = requests.delete(f"{API_URL}{self.selected_id}/")
            if res.status_code == 204:
                self.load_data()
                self.clear_form()

    def clear_form(self):
        self.selected_id = None
        self.name_var.set("")
        self.desc_var.set("")

if __name__ == "__main__":
    app = CRUDApp()
    app.mainloop()