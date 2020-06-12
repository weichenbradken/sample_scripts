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


def PLOT_WEAR_COMP(t, rd_w, sv_w, pg_w, cn):
    # to plot the wear comparison between different sims
    fig1 = plt.figure(figsize=(8.0, 6.0))
    ax = fig1.add_subplot(111)

    #width = 0.25
    ax.plot(t, rd_w, 'b', label='Bradken Design')
    ax.plot(t, sv_w, 'r', label='Metso Design')
    #ax.plot(t, pg_w, 'y', label='Radial_2')
    #ax.plot(t, sv_w, 'y', label='Radial2')

    # axes:
    ax.grid(True)
    ax.set_xlim([0, 64])
    ax.xaxis.label.set_fontsize(12)
    ax.xaxis.label.set_fontname("Arial")
    #fig1.add_subplot(111).set_ylim([0, 400])
    ax.yaxis.label.set_fontsize(12)
    ax.yaxis.label.set_fontname("Arial")
    # labels:
    ax.set_xlabel(r"Time - [s]", fontname = "Arial", fontsize=14, color = "k")
    ax.set_ylabel(r"Wear Intensity", fontname = "Arial", fontsize=14, color = "k")
    ax.set_title(r"Wear Comparison Between Designs", fontname = "Arial", fontsize=14, color = "k")
    plt.legend(loc=2)
    # saving:
    fig1.savefig("Wear_RPM_8_5_"+str(cn)+".png", dpi = 300)
    print("Processing" + str(cn))
    #writer.grab_frame()
    fig1.clear()


def WEAR_VTK_PARSER(filename, L_start, L_end):
    f = open(filename, 'r')
    # Process the VTK files
    lines = f.readlines()
    wear_lines = lines[L_start:L_end]
    
    # parse data into tmp
    tmp = []
    for lne in wear_lines:
        tmp_a = lne.strip('\n')
        tmp_b = tmp_a.split()
        #print(tmp_b)
        for tmp_c in tmp_b:
            #print(str(tmp_c))
            tmp.append(float(tmp_c))
        
    #re = np.array(tmp)
    mean_wear = np.average(tmp)
    return mean_wear


def main():
    # survey the vtk files in current dir
    radial_vtk_list = glob.glob('Radial\mesh_*.vtk')
    sv_vtk_list = glob.glob('SV\mesh_*.vtk')
    ptg_vtk_list = glob.glob('PTG\mesh_*.vtk')
    #radial2_vtk_list = glob.glob('Radial2\mesh_*.vtk')
    
    print('successfully reached here_1')
    # arrange the files by modified time
    radial_vtk_list.sort(key=os.path.getmtime)
    sv_vtk_list.sort(key=os.path.getmtime)
    ptg_vtk_list.sort(key=os.path.getmtime)
    #radial2_vtk_list.sort(key=os.path.getmtime)
    print('successfully reached here_2')
    # fetch the wear data for each frame
    radial_wear = []
    for radial_vtk in radial_vtk_list:
        tmp_rad_wear = WEAR_VTK_PARSER(radial_vtk, 274859, 288600)
        radial_wear.append(tmp_rad_wear)
    print('successfully reached here_3')
    
    sv_wear = []
    for sv_vtk in sv_vtk_list:
        tmp_sv_wear = WEAR_VTK_PARSER(sv_vtk, 336579, 353406)
        sv_wear.append(tmp_sv_wear)
    print('successfully reached here_4')
        
    ptg_wear = []
    for ptg_vtk in ptg_vtk_list:
        tmp_ptg_wear = WEAR_VTK_PARSER(ptg_vtk, 275099, 288852)
        ptg_wear.append(tmp_ptg_wear)    
    print('successfully reached here_5')
    
    #radial2_wear = []
    #for radial2_vtk in radial_vtk_list:
    #    tmp_rad2_wear = WEAR_VTK_PARSER(radial2_vtk, 274859, 288600)
    #    radial2_wear.append(tmp_rad2_wear)
    #print('successfully reached here_6')
    # get the time
    ts = np.arange(0,64.0,0.05)
    
    #tmp_t = np.zeros(len(ts))
    #tmp_rd_wear = np.zeros(len(ts))
    #tmp_sv_wear = np.zeros(len(ts))
    #tmp_pg_wear = np.zeros(len(ts))
    
    #print('successfully reached here_6')
    # plot the comparative histogram chart    
    for tmp in range(len(ts)):
        tmp_t = ts[0:tmp+1]
        tmp_rd_wear = radial_wear[0:tmp+1]
        tmp_sv_wear = sv_wear[0:tmp+1]
        tmp_pg_wear = ptg_wear[0:tmp+1]
        #tmp_rd2_wear = radial2_wear[0:tmp+1]
        #print('successfully reached here_3' + str(tmp))
        # save the png files
        PLOT_WEAR_COMP(tmp_t, tmp_rd_wear, tmp_sv_wear, tmp_pg_wear, tmp)



    
if __name__ == "__main__":
    main()