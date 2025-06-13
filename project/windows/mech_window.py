# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 12:26:25 2025

@author: simsa
"""

import customtkinter as ctk
from project import rxns
import string
from project.layout.control_bar import build_control_bar

class mechanismWindow(ctk.CTkToplevel):
    def __init__(self, master, btn_mechanism):
        super().__init__(master)
        self.master_app = master
        self.btn_mechanism = btn_mechanism
        self.btn_mechanism.configure(state="disabled")
        
        self.title("Reactions")
        self.minsize(600, 400)
        
        self.lift()
        self.attributes("-topmost", True)
        
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self.close)
        
        self.alphabet = list(string.ascii_uppercase)
        self.mod_alphabet = [ letter for letter in self.alphabet if letter != "A" ]
        
        self.build_layout()
        
    def build_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.build_control_panel()
        self.build_et_rxns()
        self.build_hr_rxns()
    
    def build_control_panel(self):
        frm_control_panel = ctk.CTkFrame(self)
        self.frm_et_rxns = ctk.CTkFrame(self)
        self.frm_hr_rxns = ctk.CTkFrame(self)
        
        frm_control_panel.grid(row=0, column=0, sticky="ns")
        self.frm_et_rxns.grid(row=0, column=1, sticky="nsew")
        self.frm_hr_rxns.grid(row=0, column=2, sticky="nsew")
        
        btn_add_et = ctk.CTkButton(frm_control_panel, text="+ET", command=self.add_et_rxn)
        btn_add_hr = ctk.CTkButton(frm_control_panel, text="+HR", command=self.add_hr_rxn)
        btn_clear = ctk.CTkButton(frm_control_panel, text="Clear", command=self.reset_rxns)
        
        btn_add_et.grid(sticky="ew")
        btn_add_hr.grid(sticky="ew")
        btn_clear.grid(sticky="ew")
        
    def build_et_rxns(self):
        for widget in self.frm_et_rxns.winfo_children():
            widget.destroy()
        
        print(rxns.ET)
        for rxn in rxns.ET["R"]:
            btn_remove_et = ctk.CTkButton(self.frm_et_rxns, text=" ‒ ", width=40, command=lambda rxn=rxn: self.remove_et_rxn(rxn))
            opt_et_reactant = ctk.CTkOptionMenu(self.frm_et_rxns, values=self.alphabet, width=60, command=lambda val, rxn=rxn: self.update_et_rxn(val, "R", rxn))
            opt_et_product = ctk.CTkOptionMenu(self.frm_et_rxns, values=self.alphabet, width=60, command=lambda val, rxn=rxn: self.update_et_rxn(val, "P", rxn))
            
            opt_et_reactant.set(rxns.ET["R"][rxn])
            opt_et_product.set(rxns.ET["P"][rxn])
            if rxn == 0:
                btn_remove_et.configure(state="disabled")
                opt_et_reactant.configure(state="disabled")
                opt_et_product.configure(state="disabled")
            
            ctk.CTkLabel(self.frm_et_rxns, text=f" {rxn} ", width=40).grid(row=rxn, column=0)
            ctk.CTkLabel(self.frm_et_rxns, text=" ⇌ ").grid(row=rxn, column=3)
            
            btn_remove_et.grid(row=rxn, column=1)
            opt_et_reactant.grid(row=rxn, column=2)
            opt_et_product.grid(row=rxn, column=4)
    
    def add_et_rxn(self):
        rxn = len(rxns.ET["R"])
        
        rxns.ET["R"][rxn] = self.alphabet[rxn]
        rxns.ET["P"][rxn] = self.alphabet[rxn+1]
        rxns.ET_parameters[rxn] = { "E" : -1.5, "alpha" : 0.5, "ko" : 1, "n" : 1 }
        if rxns.ET["R"][rxn] not in rxns.species: rxns.species.append(rxns.ET["R"][rxn])
        if rxns.ET["P"][rxn] not in rxns.species: rxns.species.append(rxns.ET["P"][rxn])
        for spec in rxns.species:
            if spec not in rxns.diffusionCoefficient.keys(): rxns.diffusionCoefficient[spec] = 1.0E-5
        
        self.build_et_rxns()
        
    ### changes ET rxn species designator when option menu value is changed
    def update_et_rxn(self, spec, role, rxn):
        rxns.ET[role][rxn] = spec
        
    def remove_et_rxn(self, rxn):        
        if rxn in rxns.ET["R"]: del rxns.ET["R"][rxn]
        else: print(f"Warning: tried to remove nonexistent ET R {rxn}", rxns.ET["R"].keys)()
        if rxn in rxns.ET["P"]: del rxns.ET["P"][rxn]
        else: print(f"Warning: tried to remove nonexistent ET P {rxn}", rxns.ET["P"].keys())
        if rxn in rxns.ET_parameters:  del rxns.ET_parameters[rxn]
        else: print(f"Warning: tried to remove nonexistent ET params {rxn}", rxns.ET_parameters.keys())
        
        species = []
        for etrxn in rxns.ET["R"]:
            if rxns.ET["R"][etrxn] not in species: species.append(rxns.ET["R"][etrxn])
            if rxns.ET["P"][etrxn] not in species: species.append(rxns.ET["P"][etrxn])
        for hrrxn in rxns.HR["R"]:
            if rxns.HR["R"][hrrxn] not in species: species.append(rxns.HR["R"][hrrxn])
            if rxns.HR["P"][hrrxn] not in species: species.append(rxns.HR["P"][hrrxn])
        rxns.species = species
        
        ### reindex rxns.ET
        for j in [ "R", "P" ]:
            vals_list = [ rxns.ET[j][i] for i in sorted(rxns.ET[j]) ]
            temp_rxns = { key : value for key, value in enumerate(vals_list) }
            rxns.ET[j] = temp_rxns
        
        vals_list = [ rxns.ET_parameters[i] for i in sorted(rxns.ET_parameters) ]
        rxns.ET_parameters = { key : value for key, value in enumerate(vals_list) }
        
        self.build_et_rxns()

    def build_hr_rxns(self):
        for widget in self.frm_hr_rxns.winfo_children():
            widget.destroy()
                
        for rxn in rxns.HR["R"]:
            print("self.build_hr_rxns: rxn", rxn)
            btn_remove_hr = ctk.CTkButton(self.frm_hr_rxns, text=" ‒ ", width=40, command=lambda rxn=rxn: self.remove_hr_rxn(rxn))
            opt_hr_reactant = ctk.CTkOptionMenu(self.frm_hr_rxns, values=self.mod_alphabet, width=60, command=lambda val, rxn=rxn: self.update_hr_rxn(val, "R", rxn))
            opt_hr_product = ctk.CTkOptionMenu(self.frm_hr_rxns, values=self.alphabet, width=60, command=lambda val, rxn=rxn: self.update_hr_rxn(val, "P", rxn))
            
            opt_hr_reactant.set(rxns.HR["R"][rxn])
            opt_hr_product.set(rxns.HR["P"][rxn])
            
            ctk.CTkLabel(self.frm_hr_rxns, text=f" {rxn} ", width=40).grid(row=rxn, column=0)
            ctk.CTkLabel(self.frm_hr_rxns, text=" ⇌ ").grid(row=rxn, column=3)
            
            btn_remove_hr.grid(row=rxn, column=1)
            opt_hr_reactant.grid(row=rxn, column=2)
            opt_hr_product.grid(row=rxn, column=4)
        
    def add_hr_rxn(self):
        rxn = len(rxns.HR["R"])
        
        rxns.HR["R"][rxn] = self.mod_alphabet[rxn]
        rxns.HR["P"][rxn] = self.mod_alphabet[rxn+1]
        rxns.HR_parameters[rxn] = 0
        if rxns.HR["R"][rxn] not in rxns.species: rxns.species.append(rxns.HR["R"][rxn])
        if rxns.HR["P"][rxn] not in rxns.species: rxns.species.append(rxns.HR["P"][rxn])
        for spec in rxns.species:
            if spec not in rxns.diffusionCoefficient.keys(): rxns.diffusionCoefficient[spec] = 1.0E-5
        
        self.build_hr_rxns()
        
    def remove_hr_rxn(self, rxn):
        if rxn in rxns.HR["R"]: del rxns.HR["R"][rxn]
        else: print(f"Warning: tried to remove nonexistent ET R {rxn}", rxns.HR["R"].keys)()
        if rxn in rxns.HR["P"]: del rxns.HR["P"][rxn]
        else: print(f"Warning: tried to remove nonexistent ET P {rxn}", rxns.HR["P"].keys())
        if rxn in rxns.HR_parameters:  del rxns.HR_parameters[rxn]
        else: print(f"Warning: tried to remove nonexistent ET params {rxn}", rxns.HR_parameters.keys())
        
        species = []
        for etrxn in rxns.ET["R"]:
            if rxns.ET["R"][etrxn] not in species: species.append(rxns.ET["R"][etrxn])
            if rxns.ET["P"][etrxn] not in species: species.append(rxns.ET["P"][etrxn])
        for hrrxn in rxns.HR["R"]:
            if rxns.HR["R"][hrrxn] not in species: species.append(rxns.HR["R"][hrrxn])
            if rxns.HR["P"][hrrxn] not in species: species.append(rxns.HR["P"][hrrxn])
        rxns.species = species
        
        for j in [ "R", "P" ]:
            vals_list = [ rxns.HR[j][i] for i in sorted(rxns.HR[j]) ]
            temp_rxns = { key : value for key, value in enumerate(vals_list) }
            rxns.HR[j] = temp_rxns
        
        vals_list = [ rxns.HR_parameters[i] for i in sorted(rxns.HR_parameters) ]
        rxns.HR_parameters = { key : value for key, value in enumerate(vals_list) }
        
        self.build_hr_rxns()
    
    ### changes HR rxn species designator when option menu value is changed
    def update_hr_rxn(self, spec, role, rxn):
        rxns.HR[role][rxn] = spec
        print("update_hr_rxn: rxns.HR =", rxns.HR)
        
    def update_rxns(self):        
        species = []
        for etrxn in rxns.ET["R"]:
            if rxns.ET["R"][etrxn] not in species: species.append(rxns.ET["R"][etrxn])
            if rxns.ET["P"][etrxn] not in species: species.append(rxns.ET["P"][etrxn])
            
        for hrrxn in rxns.HR["R"]:
            if rxns.HR["R"][hrrxn] not in species: species.append(rxns.HR["R"][hrrxn])
            if rxns.HR["P"][hrrxn] not in species: species.append(rxns.HR["P"][hrrxn])
        rxns.species = species
        
        diff_coeff_keys = [ key for key in rxns.diffusionCoefficient ]
        for spec in diff_coeff_keys:
            if spec not in rxns.species: del rxns.diffusionCoefficient[spec]
        for spec in rxns.species:
            if spec not in rxns.diffusionCoefficient.keys(): rxns.diffusionCoefficient[spec] = 1E-5
            
            
    def reset_rxns(self):
        rxns.reset()
        
        self.update_rxns()
        self.build_et_rxns()
        self.build_hr_rxns()
        
    def close(self):
        self.update_rxns()
        build_control_bar(self.master_app)
        self.btn_mechanism.configure(state="normal")
        self.master_app.mech_win = None
        self.destroy()