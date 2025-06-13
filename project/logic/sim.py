# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 11:04:11 2024

@author: ssaund
"""

import numpy as np
from project import rxns

class simulationProtocol():
    def __init__(self):
        pass
    
    ### setup x axis voltage scale
    def Escale_setup(self, Ei, Ef, L):
        halfscale = np.arange(L/2)
        Estep = abs(Ef-Ei)/(L/2)
        Efw = Ei - (Estep*halfscale) if Ei > Ef else Ei + (Estep*halfscale)
        Ebk = Ef + (Estep*halfscale) if Ei > Ef else Ef - (Estep*halfscale)
        global Escale
        Escale = np.concatenate((Efw, Ebk))
        Escale = np.concatenate((Escale, np.array([Ei])))
        
        return Escale
    
    ### SIMULATION SCRIPT
    def CV_SIM(self):
        
        print(rxns.ET_parameters)
        
        ET, HR, species, kin, ET_pars = rxns.ET, rxns.HR, {}, rxns.HR_parameters, rxns.ET_parameters
        tot_rxns = ( len(ET["R"]) + len(HR["R"]) )
    
        ### setup species parameter log
        for spec in rxns.species:
            species[spec] = {
                "flux" : {},
                "kinetics" : {},
                "km" : {},
                "C" : None,
                "D" : rxns.diffusionCoefficient[spec]
                }
    
        print("CV_SIM.species: ", species)
        
        ### setup species log based on CV_rxns_X_X module    
        for spec in species:
            for reaction in HR["R"].keys():
                species[spec]["kinetics"][reaction] = 0
            for reactant in HR["R"]:
                if spec == HR["R"][reactant]:
                    print("HR_parameters: ", kin)
                    species[spec]["kinetics"][reactant] = -kin[reactant]
            for product in HR["P"]:
                if spec == HR["P"][product]:
                    species[spec]["kinetics"][product] = kin[product]
        
        ### GLOBAL DECLARATIONS
        global C, Jo, Z, kf, kb, E, initial_C, D
        print("rxns.ET: ", rxns.ET)
        
        ### CONSTANTS
        T = 293.15 # K
        F = 96485 # C/mol
        const_R = 8.31451 # J/Kmol
        f = F / (const_R * T)
        
        initial_C, v, A, L, DM = rxns.simvars["C"]["val"], rxns.simvars["v"]["val"], rxns.simvars["A"]["val"], rxns.simvars["L"]["val"], rxns.simvars["DM"]["val"]
        
        Ei = rxns.simvars["Ei"]["val"]
        Ef = rxns.simvars["Ef"]["val"]
        Escale = self.Escale_setup(Ei, Ef, L)
        
        num_et = len(rxns.ET_parameters)
        E, D, alpha, ko, kc, n = [], [], [], [], [], []
        for i in rxns.ET_parameters:
            E.append(rxns.ET_parameters[i]["E"])
            alpha.append(rxns.ET_parameters[i]["alpha"])
            ko.append(rxns.ET_parameters[i]["ko"])
            n.append(rxns.ET_parameters[i]["n"])
            
        for spec in species: D.append(rxns.diffusionCoefficient[spec])
        for hrrxn in rxns.HR_parameters: kc.append(rxns.HR_parameters[hrrxn])
        
        print(D)
        
        ### set variables as arrays
        if np.isscalar(E): E = np.array([E])
        # if np.isscalar(D): D = np.array([D])
        if np.isscalar(n): n = np.array([n])
        if np.isscalar(alpha): alpha = np.array([alpha])
        if np.isscalar(ko): ko = np.array([ko])
        if np.isscalar(kc): kc = np.array([kc])
        
        # print(D)
        
        Dcoeff = rxns.diffusionCoefficient
        
        ### CALCULATED SIMULATION PARAMETERS
        # num_et = 1 #len(E)
        global tk, dt, dx
        tk = abs(2 * ((Ei - Ef) / v))
        dt = tk / L
        dx = ((Dcoeff["A"] * dt) / DM)
        jmaxint1 = 6 * (D[0] * tk) ** 0.5
        jmaxint=50
        dx = jmaxint1 / 50
        kscale = np.arange(L)
        halfscale = np.arange(L/2)
        
        ### CALCULATED EXPERIMENT PARAMETERS
        DM, DM_species = [], {}
        for i in D: DM.append((i * dt) / (dx ** 2))
        for i in species: DM_species[i] = (species[i]["D"] * dt) / (dx ** 2)
        initial_C = initial_C / 1000 # convert M (mol/dm3) to mol/cm3
        time = dt * kscale
    
        ### CALCULATED KINETIC PARAMETERS
        global kf, kb, ktk, km
        kf, kb, ktk, km = [], [], [], []
        for i in kc: ktk.append(i * tk)
        for i in ktk: km.append(i / L)
        for spec in species:
            for hrrxn in species[spec]["kinetics"]:
                species[spec]["km"][hrrxn] = ( species[spec]["kinetics"][hrrxn] * tk ) / L
        if num_et == 1 or (num_et == 2 and E[0] > E[1]):
            for i in range(len(E)):
                # print(i)
                kf.append(ko[i] * np.exp( -alpha[i] * n[i] * ( (Escale-E[i])*f)) )
                kb.append(ko[i] * np.exp( (1 - alpha[i]) * n[i] * ( (Escale-E[i])*f)) )
        else:
            for i in range(len(E)):
                kf.append(ko[i] * np.exp( -alpha[i] * n[i] * ( (Escale-E[i])*f)) )
                kb.append(ko[i] * np.exp( (1 - alpha[i]) * n[i] * ( (Escale-E[i])*f)) )
        ### SIMULATION SETUP
        global conc, Zarc, Jo
        conc, Jo, Zarc, Z = {}, {}, [], {}
            
        for rxn_index in range(num_et):
            Jo[rxn_index] = np.zeros((L+1, 1))
            conc[rxn_index] = {}
            if ET["R"][rxn_index] == "A" : conc[rxn_index]["R"] = initial_C * np.ones((L+1, jmaxint))
            else: conc[rxn_index]["R"] = np.zeros((L+1, jmaxint))
            conc[rxn_index]["P"] = np.zeros((L+1, jmaxint))
        
        
        
        ### SIMULATION
        global error_out
        error_out = {}
        # print("begin simulation")
        for rxn_index in range(num_et):
            # print("SIMULATING RXN #", rxn_index)
            R, P = ET["R"][rxn_index], ET["P"][rxn_index]
            # print("R:", R, "P:", P)
            species[R]["flux"][rxn_index], species[P]["flux"][rxn_index] = np.zeros((L+1, 1)), np.zeros((L+1, 1))
            
            ### TRIAGE
            error_out[rxn_index] = False
            
            ### SIMULATION EVOLUTION CYCLES
            for t in range(L):
                for x in range(1, jmaxint-1):
                    
                    ### DETERMINE RATE TERM FOR T=t+1, X=x
                    listed_kinetics_R, sum_kinetics_R, listed_kinetics_P, sum_kinetics_P = [], 0, [], 0
                    for hrrxn in rxns.HR_parameters:
                        HR_R = HR["R"][hrrxn]
                        
                        if species[R]["km"][hrrxn] != 0:
                            if HR_R == R: listed_kinetics_R.append( species[R]["km"][hrrxn] * conc[rxn_index]["R"][t][x] )
                            elif species[HR_R]["C"].any(): listed_kinetics_R.append( species[R]["km"][hrrxn] * species[HR_R]["C"][t][x] )
                            
                            else: error_out = True
                        
                        if species[P]["km"][hrrxn] != 0:
                            if HR_R == P: listed_kinetics_P.append( species[P]["km"][hrrxn] * conc[rxn_index]["P"][t][x] )
                            elif species[HR_R]["C"].any(): listed_kinetics_P.append( species[P]["km"][hrrxn] * species[HR_R]["C"][t][x] )
                            
                            else: error_out = True
                            
                    ### sum all homogeneous kinetic terms
                    for i in listed_kinetics_R: sum_kinetics_R += i
                    for i in listed_kinetics_P: sum_kinetics_P += i
                    
                    ### DIFFUSIONAL/KINETIC PROPOGATION FOR T=t+1, X=1 -> x
                    conc[rxn_index]["R"][t+1][x] = conc[rxn_index]["R"][t][x] + DM_species[R] * ( conc[rxn_index]["R"][t][x+1] - ( 2 * conc[rxn_index]["R"][t][x] ) + conc[rxn_index]["R"][t][x-1] ) + sum_kinetics_R
                    conc[rxn_index]["P"][t+1][x] = conc[rxn_index]["P"][t][x] + DM_species[P] * ( conc[rxn_index]["P"][t][x+1] - ( 2 * conc[rxn_index]["P"][t][x] ) + conc[rxn_index]["P"][t][x-1] ) + sum_kinetics_P
                    
                ### ECHEM FLUX CALCULATION
                Jo[rxn_index][t+1] = ( kf[rxn_index][t+1] * conc[rxn_index]["R"][t+1][1] - kb[rxn_index][t+1] * conc[rxn_index]["P"][t+1][1] ) / ( 1 + ( dx * kf[rxn_index][t+1] )/Dcoeff[R] + ( dx * kb[rxn_index][t+1] )/Dcoeff[P] )
                
                species[R]["flux"][rxn_index][t+1] = -Jo[rxn_index][t+1]
                species[P]["flux"][rxn_index][t+1] = Jo[rxn_index][t+1]
                
                ### SUM TOTAL FLUX TERM FOR T=t+1
                sum_J_R, sum_J_P = 0, 0
                for j in species[R]["flux"]: sum_J_R += species[R]["flux"][j][t+1]
                for j in species[P]["flux"]: sum_J_P += species[P]["flux"][j][t+1]
                    
                ### DETERMINE SURFACE CONCENTRATIONS (X=0)
                conc[rxn_index]["R"][t+1][0] = conc[rxn_index]["R"][t+1][1] + ( sum_J_R * (dx/Dcoeff[R]) )
                conc[rxn_index]["P"][t+1][0] = conc[rxn_index]["P"][t+1][1] + ( sum_J_P * (dx/Dcoeff[P]) )
                
            ### LOG CONCENTRATION PROFILES BY SPECIES 
            species[R]["C"] = conc[rxn_index]["R"]
            species[P]["C"] = conc[rxn_index]["P"]
            
            if error_out[rxn_index] == True: print("fatal error in kinetic term calculation")
            
            ### CURRENT CALCULATION FOR RXN
            Z[rxn_index] = A * n[rxn_index] * F * Jo[rxn_index]    
        
        ### OUTPUT FORMATTING
        print("Zall summation")
        global Zout
        Zall = 0
        for i in Z: Zall += (Z[i]*1000000)       
        
        ### Surface concentrations
        surface_conc, species_surface_conc = {}, {}
        for i in conc:
            surface_conc[i] = { "R" : np.ones([L+1,1]), "P" : np.ones([L+1,1]) }
            R, P = rxns.ET["R"][i], rxns.ET["P"][i]
            species_surface_conc[R], species_surface_conc[P] = np.ones([L+1,1]), np.ones([L+1,1])
            for t in range(L+1):
                surface_conc[i]["R"][t] *= conc[i]["R"][t][0]
                surface_conc[i]["P"][t] *= conc[i]["P"][t][0]
                species_surface_conc[R][t] *= conc[i]["R"][t][0]
                species_surface_conc[P][t] *= conc[i]["P"][t][0]
            
        tscale = np.concatenate((np.array([0]), time))
        
        Zout = np.ravel(Zall)
        
        print("Zout", Zout[0])
        
        global data
        data = {
            "Z" : Zout,
            "Jo" : Jo,
            "C" : conc,
            "C0" : species_surface_conc,
            "L" : L,
            "Escale" : Escale,
            }
        
        print("simulation done")
        return data