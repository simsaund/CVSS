# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 12:22:53 2025

@author: simsa
"""

from tkinter import filedialog
from project import rxns
import os
from pathlib import Path
import pickle

from project.logic.updater import update_expt_params, update_rxn_params
from project.layout.control_bar import build_control_bar
from project.layout.expt_parameters import build_expt_params

def open_data(app):
    filename = filedialog.askopenfile()
    
    if filename:
        print("Selected file:", filename.name)
        app.data_file = filename.name
        rxns.data_file["file"] = filename.name

def close_data(app):
    rxns.data_file["file"] = None
        
def save_as_mechanism(app):
    current_directory = os.getcwd()
    save_directory = Path(f"{current_directory}/save_files")
    
    save_file = filedialog.asksaveasfilename(
        initialdir=save_directory,
        defaultextension=".log",
        filetypes=[("Log Files", "*.log"), ("All Files", "*.*")]
        )
    
    if not save_file:
        return
    
    print(save_file)
    
    save_mechanism(app, save_file)
    
def load_custom_mechanism(app):
    load_file = filedialog.askopenfile()
    print(load_file.name)
    
    load_mechanism(app, load_file.name)
    
def numbered_record(app, val, saveload):
    current_directory = os.getcwd()
    parent_directory = os.path.dirname(current_directory)
    save_directory = Path(f"{parent_directory}/save_files")
    save_directory.mkdir(parents=True, exist_ok=True)
    
    filename = f"save_{val}.log"
    filepath = os.path.join(save_directory, filename)
    
    print(filepath, saveload)
    
    if saveload == "save": save_mechanism(app, filepath)
    elif saveload == "load": load_mechanism(app, filepath)
    else: print("ERROR: root.numbered_record received an invalid saveload value")
    
### pickles rxns variables
def save_mechanism(app, save_file):
    update_rxn_params(app)
    update_expt_params(app)
    
    save_data = {
        "et_rxns" : app.et_rxns,
        "hr_rxns" : app.hr_rxns,
        "HR_parameters" : rxns.HR_parameters,
        "ET_parameters" : rxns.ET_parameters,
        "species" : rxns.species,
        "diffusionCoefficient" : rxns.diffusionCoefficient,
        "simvars" : rxns.simvars,
        "data_file" : rxns.data_file
        }
    
    open(save_file, "w").close()
    
    with open(save_file, "ab") as file:
        pickle.dump(save_data, file)
    
### loads and updates rxns variables
def load_mechanism(app, load_file):
    if os.path.exists(load_file):
        pass
    else:
        print("save file not found")
        return
    
    with open(load_file, "rb") as file:
        loaded_data = pickle.load(file)
    
    app.et_rxns.clear()
    app.hr_rxns.clear()
    rxns.HR_parameters.clear()
    rxns.ET_parameters.clear()
    rxns.species.clear()
    rxns.diffusionCoefficient.clear()
    rxns.simvars.clear()
    rxns.data_file.clear()
    
    app.et_rxns.update(loaded_data["et_rxns"])
    app.hr_rxns.update(loaded_data["hr_rxns"])
    rxns.HR_parameters.update(loaded_data["HR_parameters"])
    rxns.ET_parameters.update(loaded_data["ET_parameters"])
    rxns.species.extend(loaded_data["species"])
    rxns.diffusionCoefficient.update(loaded_data["diffusionCoefficient"])
    rxns.simvars.update(loaded_data["simvars"])
    rxns.data_file.update(loaded_data["data_file"])
    
    build_control_bar(app)
    build_expt_params(app)