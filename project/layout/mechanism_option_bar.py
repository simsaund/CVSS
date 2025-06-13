# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 11:34:50 2025

@author: simsa
"""

import customtkinter as ctk
from project.logic.record_keeper import save_as_mechanism, load_custom_mechanism, numbered_record

def build_mech_option_bar(app):
    frm_mech_opt = ctk.CTkFrame(app)
    frm_mech_opt.grid(row=1, column=0, sticky="ns")
    
    btn_save = ctk.CTkButton(frm_mech_opt, text="Save", width=40, command=lambda: save_as_mechanism(app))
    btn_load = ctk.CTkButton(frm_mech_opt, text="Load", width=40, command=lambda: load_custom_mechanism(app))

    btn_load.grid(row=0, column=1, sticky="ew", padx=5, pady=10)
    btn_save.grid(row=0, column=0, sticky="ew", padx=5, pady=10)

    dict_save, dict_load = {}, {}
    for i in range(4):
        dict_save[i] = ctk.CTkButton(frm_mech_opt, text=i+1, width=40, command=lambda i=i+1: numbered_record(app, i, "save"))
        dict_load[i] = ctk.CTkButton(frm_mech_opt, text=i+1, width=40, command=lambda i=i+1: numbered_record(app, i, "load"))
        dict_save[i].grid(row=i+2, column=0)
        dict_load[i].grid(row=i+2, column=1)