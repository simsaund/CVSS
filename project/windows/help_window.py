# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 12:25:22 2025

@author: simsa
"""

import customtkinter as ctk
from project.windows import help_text

class helpWindow(ctk.CTkToplevel):
    def __init__(self, master, btn_help):
        super().__init__(master)
        self.title("Help")
        self.geometry("400x300")
        self.minsize(700,700)
        
        self.btn_help = btn_help
        
        self.attributes("-topmost", True)
        
        self.protocol("WM_DELETE_WINDOW", self.close)
        
        txt_help = ctk.CTkTextbox(self, wrap="word", width=380, height=280)
        txt_help.insert("1.0", help_text.help_text)
        txt_help.configure(state="disabled")
        txt_help.pack(padx=10, pady=10, fill="both", expand=True)
    
    def close(self):
        self.btn_help.configure(state="normal")
        self.destroy()