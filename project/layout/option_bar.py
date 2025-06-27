# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 11:27:49 2025

@author: simsa
"""

import customtkinter as ctk
from project.logic.record_keeper import open_data, close_data
from project.logic.plotter import simulate

### builds the left option bar
def build_option_bar(app):
    frm_optbar = ctk.CTkFrame(app)
    frm_optbar.grid(row=0, column=0, sticky="ns")

    btn_open_dat = ctk.CTkButton(frm_optbar, text="Load Data", command=lambda: open_data(app))
    btn_close_dat = ctk.CTkButton(frm_optbar, text="Close Data", command=lambda: close_data(app))
    btn_quit = ctk.CTkButton(frm_optbar, text="Quit", fg_color="#7F7F7F", command=app.close)
    btn_sim = ctk.CTkButton(frm_optbar, text="Simulate", fg_color="#FF6600", command=lambda: simulate(app))
    app.btn_mechanism = ctk.CTkButton(frm_optbar, text="Reactions", command=lambda: app.openMechanismWindow(app.btn_mechanism))
    app.btn_help = ctk.CTkButton(frm_optbar, text="Help", fg_color="#7F7F7F", command=lambda: app.open_help_window(app.btn_help))
    app.btn_visualizer = ctk.CTkButton(frm_optbar, text="Data", command=lambda: app.open_data_visualizer(app.btn_visualizer))

    btn_open_dat.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
    btn_close_dat.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
    btn_sim.grid(row=0, column=0, sticky="ew", padx=5, pady=(20, 5))
    app.btn_mechanism.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    app.btn_visualizer.grid(row=2, column=0, sticky="ew", padx=5, pady=(5, 40))
    app.btn_help.grid(row=45, column=0, sticky="ew", padx=5, pady=5)
    btn_quit.grid(row=10, column=0, sticky="ew", padx=5, pady=(100, 5))
