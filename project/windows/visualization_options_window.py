# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 12:28:35 2025

@author: simsa
"""

import customtkinter as ctk
from project import rxns
from project.logic.plotter import simulate

class dataVisualizerOptions(ctk.CTkToplevel):
    def __init__(self, master, btn_visualizer):
        super().__init__(master)
        self.title("Surface Concentrations")
        self.minsize(600, 500)
        
        self.lift()
        self.attributes("-topmost", True)
        
        self.protocol("WM_DELETE_WINDOW", self.close)
        
        self.master_app = master
        self.btn_visualizer = btn_visualizer
        
        self.colors = [ "red", "orangered", "darkorange", "orange", "gold", "yellowgreen", "forestgreen", "limegreen", "mediumturquoise",
                  "darkcyan", "deepskyblue", "steelblue", "dodgerblue", "royalblue", "blue", "slateblue", "darkviolet", "violet",
                  "darkmagenta", "hotpink", "crimson" ]
        
        self.et_species = []
        for spec in rxns.ET["R"].values():
            self.et_species.append(spec)
        for spec in rxns.ET["P"].values():
            if spec not in self.et_species: self.et_species.append(spec)
                    
        self.build_layout()
        
    def build_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.build_controls()
        
    def build_controls(self):
        frm_data_cntrls = ctk.CTkFrame(self)
        frm_data_cntrls.grid()
        
        ct, cl, self.cbx_concs, self.opt_concs  = 0, 0, {}, {}
        for spec in self.et_species:
            ctk.CTkLabel(frm_data_cntrls, text=spec, width=40).grid(row=ct, column=0, sticky="ew", padx=[5, 20])
            
            self.cbx_concs[spec] = ctk.CTkCheckBox(frm_data_cntrls, text="", width=10, command=self.update)
            self.opt_concs[spec] = ctk.CTkOptionMenu(frm_data_cntrls, values=self.colors, command=self.update)
            
            self.cbx_concs[spec].grid(row=ct, column=1, sticky="ew", padx=10, pady=10)
            self.opt_concs[spec].grid(row=ct, column=2, sticky="ew", padx=10, pady=5)
            
            if spec in rxns.conc_vis.keys():
                self.cbx_concs[spec].select()
                self.opt_concs[spec].set(rxns.conc_vis[spec])
            else:
                if cl > len(self.colors): cl=0
                self.cbx_concs[spec].deselect()
                self.opt_concs[spec].set(self.colors[cl])
                
            cl+=1
            ct+=1
            
    def update(self, *args):
        for spec in self.et_species:
            if self.cbx_concs[spec].get():
                rxns.conc_vis[spec] = self.opt_concs[spec].get()
            else:
                if spec in rxns.conc_vis.keys():
                    del rxns.conc_vis[spec]
                        
    def close(self):
        self.update()
        print(rxns.conc_vis)
        simulate(self.master_app)
        self.btn_visualizer.configure(state="normal")
        self.destroy()