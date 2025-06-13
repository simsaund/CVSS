# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 09:55:53 2025

@author: simsa
"""

import copy

ET = {
       "R" : {
           0 : "A"
           },
       "P" : {
           0 : "B"
           }
       }

HR = {
       "R" : {},
       "P" : {}
       }

HR_parameters = {}

ET_parameters = {
    0 : { "E" : -1.5, "alpha" : 0.5, "ko" : 1, "n" : 1 }
    }

species = [ "A", "B" ]

diffusionCoefficient = {
    "A" : 1.0E-5,
    "B" : 1.0E-5
    }

simvars = {
    "C"     : { "val" : 0.001, "type" : "float", "unit" : "M" },
    "Ei"    : { "val" : -0.5, "type" : "float", "unit" : "V" },
    "Ef"    : { "val" : -2.5, "type" : "float", "unit" : "V" },
    "v"     : { "val" : 0.1, "type" : "float", "unit" : "V/s" },
    "A"     : { "val" : 0.09, "type" : "float", "unit" : "cm^2" },
    "L"     : { "val" : 600, "type" : "int", "unit" : "grid" },
    "DM"    : { "val" : 0.45, "type" : "float", "unit" : "" },
    "DPI"   : { "val" : 100, "type" : "int", "unit" : "" }
    }

conc_vis = {}

data_file = { "file" : None }

save_file = { "file" : None }

# --- Store original deep copies ---
_defaults = {
    "ET": copy.deepcopy(ET),
    "ET_parameters": copy.deepcopy(ET_parameters),
    "HR": copy.deepcopy(HR),
    "HR_parameters": copy.deepcopy(HR_parameters),
    "species": copy.deepcopy(species),
    "diffusionCoefficient": copy.deepcopy(diffusionCoefficient),
    "simvars": copy.deepcopy(simvars),
    "conc_vis": copy.deepcopy(conc_vis),
    "data_file": copy.deepcopy(data_file),
    "save_file": copy.deepcopy(save_file),
}


# --- Reset function ---
def reset():
    ET.clear()
    ET.update(copy.deepcopy(_defaults["ET"]))

    ET_parameters.clear()
    ET_parameters.update(copy.deepcopy(_defaults["ET_parameters"]))

    HR.clear()
    HR.update(copy.deepcopy(_defaults["HR"]))

    HR_parameters.clear()
    HR_parameters.update(copy.deepcopy(_defaults["HR_parameters"]))

    species.clear()
    species.extend(copy.deepcopy(_defaults["species"]))

    diffusionCoefficient.clear()
    diffusionCoefficient.update(copy.deepcopy(_defaults["diffusionCoefficient"]))

    simvars.clear()
    simvars.update(copy.deepcopy(_defaults["simvars"]))
    
    conc_vis.clear()
    conc_vis.update(copy.deepcopy(_defaults["conc_vis"]))

    data_file.clear()
    data_file.update(copy.deepcopy(_defaults["data_file"]))

    save_file.clear()
    save_file.update(copy.deepcopy(_defaults["save_file"]))