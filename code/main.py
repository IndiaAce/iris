import tkinter as tk
from interface import IntelligenceApp
from database import setup_database
from jira import create_jira_ticket, update_jira_ticket
import sqlite3

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.intelligence_app = IntelligenceApp(self.root)

        # Hook the modification events to Jira integration
        self.intelligence_app.add_pir_callback = self.handle_pir_addition
        self.intelligence_app.edit_pir_callback = self.handle_pir_edit
        
    def run(self):
        setup_database()
        self.root.mainloop()

    def handle_pir_addition(self, pir_id):
        create_jira_ticket(pir_id)

    def handle_pir_edit(self, pir_id):
        update_jira_ticket(pir_id)

# Extend IntelligenceApp to provide hooks for callbacks
def extended_setup_pir_tab(self):
    self.original_setup_pir_tab()
    # Override add_pir method to invoke callback
    original_add_pir = self.add_pir
    
    def new_add_pir():
        original_add_pir()
        selected_item = self.pir_list.selection()
        if selected_item:
            pir_id = self.pir_list.item(selected_item)['values'][0]
            if hasattr(self, 'add_pir_callback'):
                self.add_pir_callback(pir_id)

    self.add_pir = new_add_pir
    
    # Override edit_pir method to invoke callback
    original_edit_pir = self.edit_pir
    
    def new_edit_pir():
        selected_item = self.pir_list.selection()
        if selected_item:
            pir_id = self.pir_list.item(selected_item)['values'][0]
            original_edit_pir()
            if hasattr(self, 'edit_pir_callback'):
                self.edit_pir_callback(pir_id)

    self.edit_pir = new_edit_pir

# Monkey patch the setup_pir_tab to provide the callback capabilities
IntelligenceApp.original_setup_pir_tab = IntelligenceApp.setup_pir_tab
IntelligenceApp.setup_pir_tab = extended_setup_pir_tab

if __name__ == "__main__":
    app = MainApp()
    app.run()
