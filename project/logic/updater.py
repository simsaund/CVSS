# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 12:05:14 2025

@author: simsa
"""

from project import rxns

def update_rxn_params(app):
    temp_et_params = {}
    for rxn in rxns.ET_parameters:
        temp_et_params[rxn] = {}
        for param in rxns.ET_parameters[0].keys():
            temp_et_params[rxn][param] = float(app.et_param_entries[rxn][param].get())
            
    rxns.ET_parameters = temp_et_params
    
    temp_spec_params = {}
    for spec in rxns.diffusionCoefficient:
        temp_spec_params[spec] = float(app.spec_param_entries[spec].get())
        
    rxns.diffusionCoefficient = temp_spec_params
    
    temp_hr_params = {}
    for rxn in rxns.HR_parameters:
        temp_hr_params[rxn] = float(app.hr_param_entries[rxn].get())
        
    rxns.HR_parameters = temp_hr_params

### updates rxns (rxns.simvars) experiment parameters according to expt control panel entries
def update_expt_params(app):
    for exptparam in app.simvars:
        if app.simvars[exptparam]["type"] == "float":
            app.simvars[exptparam]["val"] = float(app.var_entries[exptparam].get())
        else:
            app.simvars[exptparam]["val"] = int(app.var_entries[exptparam].get())