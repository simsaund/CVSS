# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 11:38:01 2025

@author: simsa
"""

import customtkinter as ctk

def build_plot_window(app):
    app.frm_mpl = ctk.CTkFrame(app)
    app.frm_mpl.grid(row=0, column=1, sticky="nsew")
    app.frm_mpl.rowconfigure(0, weight=1)
    app.frm_mpl.columnconfigure(0, weight=1)