# This script is designed to process the tonnage and wear date for 
# mill discharge simulations performed in LIGGGHTS
# Author: Dr Wei Chen
# Market and Business Development

import os
import glob
#import math
#import pandas as pd

import matplotlib.pyplot as plt
import numpy as np


def PLOT_WEAR_COMP(t, sv_w, sv2_w, cn):
    # to plot the wear comparison between different sims
    fig1 = plt.figure(figsize=(8.0, 6.0))
    ax = fig1.add_subplot(111)

    #width = 0.25
    ax.plot(t, sv_w, 'b', label='Super Vortex')
    ax.plot(t, sv2_w, 'r', label='Super Vortex2')
    #ax.plot(t, pg_w, 'y', label='Radial_2')
    #ax.plot(t, rd2_w, 'y', label='Radial2')

    # axes:
    ax.grid(True)
    ax.set_xlim([0, 36])
    ax.xaxis.label.set_fontsize(12)
    ax.xaxis.label.set_fontname("Arial")
    ax.set_ylim([0, 90])
    ax.yaxis.label.set_fontsize(12)
    ax.yaxis.label.set_fontname("Arial")
    # labels:
    ax.set_xlabel(r"Time - [s]", fontname = "Arial", fontsize=14, color = "k")
    ax.set_ylabel(r"Discharge Efficiency - %", fontname = "Arial", fontsize=14, color = "k")
    ax.set_title(r"Discharge Efficiency Comparison Between Designs", fontname = "Arial", fontsize=14, color = "k")
    plt.legend(loc=2)
    # saving:
    fig1.savefig("DE_RPM_8_5_"+str(cn)+".png", dpi = 300)
    print("Processing" + str(cn))
    #writer.grab_frame()
    fig1.clear()


def DE_PARSER(filename):
    f = open(filename, 'r')
    # Process the VTK files
    lines = f.readlines()
    wear_lines = lines[1:-1]
    
    # parse data into tmp
    tmp = []
    cnt = 0
    for lne in wear_lines:
        tmp_a = lne.strip('\n')
        tmp_b = tmp_a.split(',')
        #print(tmp_b[0])
        tmp.append(float(tmp_b[3]))
        tmp.append(float(tmp_b[3]))

    return tmp


def main():
    # survey the vtk files in current dir
    tmp_sv_DE = DE_PARSER('sv_output.csv')
    tmp_sv2_DE = DE_PARSER('sv2_output.csv')
    #tmp_ptg_DE = DE_PARSER('ptg_output.csv')
    #tmp_rad2_DE = DE_PARSER('radial2_output.csv')

    print('successfully reached here_1')
    # get the time
    ts = np.arange(0,35.5,0.05)
    
    # plot the comparative histogram chart    
    for tmp in range(len(ts)):
        tmp_t = ts[0:tmp+1]
        tmp_sv_wear = tmp_sv_DE[0:tmp+1]
        tmp_sv2_wear = tmp_sv2_DE[0:tmp+1]
        #tmp_pg_wear = tmp_ptg_DE[0:tmp+1]
        #tmp_rd2_wear = tmp_rad2_DE[0:tmp+1]
        #print('successfully reached here_3' + str(tmp))
        # save the png files
        PLOT_WEAR_COMP(tmp_t, tmp_sv_wear, tmp_sv2_wear, tmp)

if __name__ == "__main__":
    main()