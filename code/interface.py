import tkinter as tk
from tkinter import ttk, messagebox
from database import add_pir, update_pir, delete_pir, add_source, update_source, delete_source, add_mapping
import sqlite3

class IntelligenceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligence Requirements Management")
        self.root.geometry("800x600")
        
        # Create tabs for the interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Tabs
        self.pir_tab = ttk.Frame(self.notebook)
        self.sources_tab = ttk.Frame(self.notebook)
        self.mapping_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.pir_tab, text="PIR Management")
        self.notebook.add(self.sources_tab, text="Source Management")
        self.notebook.add(self.mapping_tab, text="Mapping")
        
        self.setup_pir_tab()
        self.setup_sources_tab()
        self.setup_mapping_tab()
        
    def setup_pir_tab(self):
        # PIR Management Section
        self.pir_list = ttk.Treeview(self.pir_tab, columns=("ID", "Description", "Priority", "Date Added", "Status"), show="headings")
        self.pir_list.heading("ID", text="ID")
        self.pir_list.heading("Description", text="Description")
        self.pir_list.heading("Priority", text="Priority")
        self.pir_list.heading("Date Added", text="Date Added")
        self.pir_list.heading("Status", text="Status")
        self.pir_list.pack(expand=True, fill='both')
        
        self.load_pir_data()
        
        # Add PIR Form
        self.pir_form_frame = ttk.Frame(self.pir_tab)
        self.pir_form_frame.pack(pady=10)
        
        ttk.Label(self.pir_form_frame, text="Description").grid(row=0, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(self.pir_form_frame, width=30)
        self.description_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.pir_form_frame, text="Priority").grid(row=1, column=0, padx=5, pady=5)
        self.priority_entry = ttk.Entry(self.pir_form_frame, width=30)
        self.priority_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(self.pir_form_frame, text="Add PIR", command=self.add_pir).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(self.pir_form_frame, text="Edit PIR", command=self.edit_pir).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(self.pir_form_frame, text="Delete PIR", command=self.delete_pir).grid(row=2, column=2, padx=5, pady=5)
        
    def load_pir_data(self):
        for row in self.pir_list.get_children():
            self.pir_list.delete(row)
        connection = sqlite3.connect(r'C:\\Users\\lukew\\OneDrive\\Documents\\dev_link\\Threat\\iris\\intelligence.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM PIRs")
        rows = cursor.fetchall()
        for row in rows:
            self.pir_list.insert("", "end", values=row)
        connection.close()
        
    def add_pir(self):
        description = self.description_entry.get()
        priority = self.priority_entry.get()
        if description and priority:
            add_pir(description, priority, "2024-11-10", "Open", "None")
            self.load_pir_data()
            self.description_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "All fields are required")

    def edit_pir(self):
        selected_item = self.pir_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a PIR to edit")
            return
        pir_id = self.pir_list.item(selected_item)['values'][0]
        description = self.description_entry.get()
        priority = self.priority_entry.get()
        if description and priority:
            update_pir(pir_id, description=description, priority_level=priority)
            self.load_pir_data()
        else:
            messagebox.showerror("Error", "All fields are required")

    def delete_pir(self):
        selected_item = self.pir_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a PIR to delete")
            return
        pir_id = self.pir_list.item(selected_item)['values'][0]
        delete_pir(pir_id)
        self.load_pir_data()

    def setup_sources_tab(self):
        # Source Management Section
        self.source_list = ttk.Treeview(self.sources_tab, columns=("Source ID", "Name", "Type", "Relevance"), show="headings")
        self.source_list.heading("Source ID", text="Source ID")
        self.source_list.heading("Name", text="Name")
        self.source_list.heading("Type", text="Type")
        self.source_list.heading("Relevance", text="Relevance")
        self.source_list.pack(expand=True, fill='both')
        
        self.load_source_data()
        
        # Add Source Form
        self.source_form_frame = ttk.Frame(self.sources_tab)
        self.source_form_frame.pack(pady=10)
        
        ttk.Label(self.source_form_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(self.source_form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.source_form_frame, text="Type").grid(row=1, column=0, padx=5, pady=5)
        self.type_entry = ttk.Entry(self.source_form_frame, width=30)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.source_form_frame, text="Relevance").grid(row=2, column=0, padx=5, pady=5)
        self.relevance_entry = ttk.Entry(self.source_form_frame, width=30)
        self.relevance_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(self.source_form_frame, text="Add Source", command=self.add_source).grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(self.source_form_frame, text="Edit Source", command=self.edit_source).grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(self.source_form_frame, text="Delete Source", command=self.delete_source).grid(row=3, column=2, padx=5, pady=5)
        
    def load_source_data(self):
        for row in self.source_list.get_children():
            self.source_list.delete(row)
        connection = sqlite3.connect(r'C:\\Users\\lukew\\OneDrive\\Documents\\dev_link\\Threat\\iris\\intelligence.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Sources")
        rows = cursor.fetchall()
        for row in rows:
            self.source_list.insert("", "end", values=row)
        connection.close()
        
    def add_source(self):
        name = self.name_entry.get()
        type_ = self.type_entry.get()
        relevance = self.relevance_entry.get()
        if name and type_ and relevance:
            add_source(name, type_, relevance)
            self.load_source_data()
            self.name_entry.delete(0, tk.END)
            self.type_entry.delete(0, tk.END)
            self.relevance_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "All fields are required")

    def edit_source(self):
        selected_item = self.source_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a source to edit")
            return
        source_id = self.source_list.item(selected_item)['values'][0]
        name = self.name_entry.get()
        type_ = self.type_entry.get()
        relevance = self.relevance_entry.get()
        if name and type_ and relevance:
            update_source(source_id, name=name, type=type_, relevance=relevance)
            self.load_source_data()
        else:
            messagebox.showerror("Error", "All fields are required")

    def delete_source(self):
        selected_item = self.source_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a source to delete")
            return
        source_id = self.source_list.item(selected_item)['values'][0]
        delete_source(source_id)
        self.load_source_data()
        
    def setup_mapping_tab(self):
        # Mapping Management Section
        ttk.Label(self.mapping_tab, text="Mapping PIRs to Sources (Coming Soon)").pack(pady=20)
        # Placeholder for future mapping logic

if __name__ == "__main__":
    root = tk.Tk()
    app = IntelligenceApp(root)
    root.mainloop()