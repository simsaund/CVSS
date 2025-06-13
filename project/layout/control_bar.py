# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 11:39:59 2025

@author: simsa
"""

import customtkinter as ctk
from project import rxns

def build_control_bar(app):
    if hasattr(app, "frm_cntrl"):
        app.frm_cntrl.destroy()
    
    app.frm_cntrl = ctk.CTkFrame(app)
    app.frm_cntrl.grid(row=1, column=1, sticky="ew")
    
    app.frm_et_params = ctk.CTkFrame(app.frm_cntrl)
    app.frm_spec_params = ctk.CTkFrame(app.frm_cntrl)
    app.frm_hr_params = ctk.CTkFrame(app.frm_cntrl)
    
    app.frm_et_params.grid(row=0, column=0, sticky="ns")
    app.frm_spec_params.grid(row=0, column=1, sticky="ns")
    app.frm_hr_params.grid(row=0, column=2, sticky="ns")
    
    build_et_params(app)
    build_species_params(app)
    build_hr_params(app)
    
def build_et_params(app):        
    for widget in app.frm_et_params.winfo_children():
        widget.destroy()
    
    dict_et_frms = {}
    for rxn in app.et_rxns["R"]:
        dict_et_frms[rxn] = ctk.CTkFrame(app.frm_et_params)
        dict_et_frms[rxn].grid(row=0, column=rxn, sticky="ns")
        
        ctk.CTkLabel(dict_et_frms[rxn], text=f"Rxn {rxn}").grid(row=0, column=rxn+1)
        
        app.et_param_entries[rxn], ct = {}, 1
        for param in rxns.ET_parameters[0].keys():
            if rxn == 0:
                ctk.CTkLabel(dict_et_frms[0], text=param, width=40).grid(row=ct, column=0)
                
            entry = ctk.CTkEntry(dict_et_frms[rxn], width=60)
            entry.grid(row=ct, column=rxn+1)
            entry.insert(0, str(rxns.ET_parameters[rxn][param]))
            app.et_param_entries[rxn][param] = entry
            
            ct+=1
            
def build_species_params(app):
    for widget in app.frm_spec_params.winfo_children():
        widget.destroy()
    
    ctk.CTkLabel(app.frm_spec_params, text="D (cm-1)").grid(row=0, column=1)
    
    print("rxns.diffusionCoefficients: ", rxns.diffusionCoefficient)
    print("")
    
    ct = 1
    for spec in rxns.species:
        ctk.CTkLabel(app.frm_spec_params, text=f"{spec}", width=40).grid(row=ct, column=0)
        entry = ctk.CTkEntry(app.frm_spec_params, width=60)
        entry.grid(row=ct, column=1)
        entry.insert(0, float(rxns.diffusionCoefficient[spec]))
        app.spec_param_entries[spec] = entry
        
        ct+=1
        
def build_hr_params(app):
    for widget in app.frm_hr_params.winfo_children():
        widget.destroy()
    
    ctk.CTkLabel(app.frm_hr_params, text="kc (s-1)").grid(row=0, column=1)
    
    for hrrxn in app.hr_rxns["R"]:
        ctk.CTkLabel(app.frm_hr_params, text=f"{hrrxn}", width=40).grid(row=hrrxn+1, column=0)
        entry = ctk.CTkEntry(app.frm_hr_params, width=60)
        entry.grid(row=hrrxn+1, column=1)
        entry.insert(0, float(rxns.HR_parameters[hrrxn]))
        app.hr_param_entries[hrrxn] = entry