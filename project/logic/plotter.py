# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 13:53:55 2025

@author: simsa
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
from project import rxns
from project.logic.sim import simulationProtocol as cv
from project.logic.updater import update_rxn_params, update_expt_params
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

def simulate(app):
    update_rxn_params(app)
    update_expt_params(app)

    # Clean up old canvas and toolbar if they exist
    if hasattr(app, 'canvas') and app.canvas:
        app.canvas.get_tk_widget().destroy()
        app.canvas = None
    if hasattr(app, 'toolbar') and app.toolbar:
        app.toolbar.destroy()
        app.toolbar = None
    if hasattr(app, 'fig') and app.fig:
        plt.close(app.fig)
        app.fig = None

    for widget in app.frm_mpl.winfo_children():
        widget.destroy()

    # New plot
    fig = CV_PLOT(rxns.data_file["file"])
    app.fig = fig

    canvas = FigureCanvasTkAgg(fig, master=app.frm_mpl)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
    app.canvas = canvas

    toolbar = NavigationToolbar2Tk(canvas, app.frm_mpl, pack_toolbar=False)
    toolbar.configure(bg='lightblue')
    toolbar._message_label.configure(bg='lightblue', fg='black')
    for i in toolbar.winfo_children():
        i.config(bg='lightblue')
    toolbar.update()
    toolbar.grid(row=1, column=0, sticky="ew")
    app.toolbar = toolbar

def CV_PLOT(data_file):    
    data = cv().CV_SIM()
    L = data["L"]
    Escale = data["Escale"]
    Zall = data["Z"]
    
    plt.close("all")
    dpi_fig = rxns.simvars["DPI"]["val"]
    ### Plotting
    mpl.rcParams.update(mpl.rcParamsDefault)    
    fig, ax1 = plt.subplots(1,1, figsize=(8, 6), dpi=dpi_fig)
    
    Efw1=int(L/2)
    Eb=int(L/2+1)
    
    ax1.plot(Escale[:Efw1], Zall[:Efw1], color='0.2')
    ax1.plot(Escale[Eb:], Zall[Eb:], color='0.2', linestyle='dashed')
    
    ax2 = ax1.twinx()
    
    print(data["C0"].keys())
    scale = 1E6
    conc_max, conc_min = [], []
    for spec in rxns.conc_vis:
        ax2.plot(Escale[:Efw1], data["C0"][spec][:Efw1]*scale, linewidth=0.6, color=rxns.conc_vis[spec])
        ax2.plot(Escale[Eb:], data["C0"][spec][Eb:]*scale, linewidth=0.6, color=rxns.conc_vis[spec], linestyle='dashed')
        conc_max.append(max(data["C0"][spec]))
        conc_min.append(min(data["C0"][spec]))
        
    if not data_file:
        print("CV_PLOT: no data loaded") 
        xmax = max(Escale)
        xmin = min(Escale)
        ymax = max(Zall)
        ymin = min(Zall)
    else:
        headers = [ "E", "i" ]
        
        df = pd.read_csv(data_file,
                          sep=',', names=headers, skiprows=1)
        xdat = df.E
        ydat = np.array(df.i)
        
        ax1.plot(xdat, ydat, color="orangered", alpha=0.5)
        
        xmax = max( max(xdat), max(Escale) )
        xmin = min( min(xdat), min(Escale) )
        ymax = max( max(ydat), max(Zall) )
        ymin = min( min(ydat), min(Zall) )
    
    try:
        ax1.axis([xmax, 1.1*xmin, 1.1*ymin, 1.1*ymax])
    except Exception:
        ax1.axis([xmax, 1.1*xmin, -50, 100])

    if rxns.conc_vis:
        ax2.set_ylim((min(conc_min) - (max(conc_max)*0.1) * scale), (max(conc_max)*1.1) * scale)
        
    ax1.set_xlabel("Potential (V)")
    ax1.set_ylabel("Current (μA)")
    ax2.set_ylabel("Concentration (mM)")
    # ax1.set_title("Cyclic Voltammetry Simulation")
    
    # plt.show()
    
    return fig
