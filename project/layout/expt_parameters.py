# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 11:47:42 2025

@author: simsa
"""

import customtkinter as ctk
from project import rxns
import copy

def build_expt_params(app):
    if hasattr(app, "frm_expt_params"):
        app.frm_expt_params.destroy()
    
    app.frm_expt_params = ctk.CTkFrame(app)
    app.frm_expt_params.grid(row=0, column=2, sticky="ns")
    
    ctk.CTkLabel(app.frm_expt_params, text="Experiment Params").grid(row=0, column=1, sticky="ew")
    
    ct = 1
    for key, val in app.simvars.items():
        label = ctk.CTkLabel(app.frm_expt_params, text=key, padx=10)
        unit = ctk.CTkLabel(app.frm_expt_params, text=val["unit"], padx=10)

        label.grid(row=ct, column=0)
        unit.grid(row=ct, column=2)
        
        entry = ctk.CTkEntry(app.frm_expt_params, width=100)
        entry.grid(row=ct, column=1, pady=1)
        entry.insert(0, str(val["val"]))
        app.var_entries[key] = entry
        
        ct+=1
    
    btn_reset = ctk.CTkButton(app.frm_expt_params, text="Reset", width=100, command=lambda: reset_simvars(app))
    btn_reset.grid(row=10, column=1, pady=20)
    
def reset_simvars(app):
    rxns.simvars.clear()
    rxns.simvars.update(copy.deepcopy(rxns._defaults["simvars"]))
    
    build_expt_params(app)