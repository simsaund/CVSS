# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 11:26:09 2025

@author: simsa
"""

import customtkinter as ctk
from project import rxns
import os
import sys
from project.layout.option_bar import build_option_bar
from project.layout.mechanism_option_bar import build_mech_option_bar
from project.layout.plot_window import build_plot_window
from project.layout.control_bar import build_control_bar
from project.layout.expt_parameters import build_expt_params

from .windows.mech_window import mechanismWindow
from .windows.visualization_options_window import dataVisualizerOptions
from .windows.help_window import helpWindow

root_path = os.path.abspath(os.path.dirname(__file__))  # or use current working directory
if root_path not in sys.path:
    sys.path.append(root_path)

class cvSimulatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Embedded MPL")
        self.minsize(900, 500)
        
        self.simvars = rxns.simvars
        
        self.et_param_entries = {}
        self.spec_param_entries = {}
        self.hr_param_entries = {}
        self.var_entries = {}
        
        self.mech_win_state = None
        self.et_rxns = rxns.ET
        self.hr_rxns = rxns.HR
        
        self.data_file = 0
        
        self.build_layout()
        
        self.protocol("WM_DELETE_WINDOW", self.close)
    
    ### sets up full window layout and calls build methods
    def build_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        build_option_bar(self)
        build_plot_window(self)
        build_mech_option_bar(self)
        build_control_bar(self)
        build_expt_params(self)
        
    ### tests if the reactions window is open, if not, opens reactions window and disables the button
    def openMechanismWindow(self, btn_mechanism):
        try:
            if self.mech_win and self.mech_win.winfo_exists():
                return
        except Exception:
            pass
            
        self.mech_win = mechanismWindow(self, btn_mechanism)
        btn_mechanism.configure(state="disabled")
        
    def open_data_visualizer(self, btn_visualizer):
        print(self.et_rxns)
        self.data_vis_opt = dataVisualizerOptions(self, btn_visualizer)
        btn_visualizer.configure(state="disabled")
        
    def open_help_window(self, btn_help):
        self.help_win = helpWindow(self, btn_help)
        btn_help.configure(state="disabled")
        
    def close(self):
        try:
            if hasattr(self, "canvas") and self.canvas:
                widget = self.canvas.get_tk_widget()
    
                # Cancel idle draw loop if set (avoid Tcl error)
                if hasattr(self.canvas, "_idle_draw_id"):
                    try:
                        widget.after_cancel(self.canvas._idle_draw_id)
                    except Exception:
                        pass
    
                widget.destroy()
                self.canvas = None
    
            if hasattr(self, "toolbar") and self.toolbar:
                self.toolbar.destroy()
                self.toolbar = None
    
            if hasattr(self, "fig") and self.fig:
                import matplotlib.pyplot as plt
                plt.close(self.fig)
                self.fig = None
    
        except Exception as e:
            print("Cleanup error:", e)
    
        self.quit()
        self.destroy()