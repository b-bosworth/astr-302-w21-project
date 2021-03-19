#!/usr/bin/env python
import requests
import pandas as pd
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed

def downloadthedata():
    """
    Downloads the file MPCORB.DAT from minorplanetcenter.net
    """
    r = requests.get('https://minorplanetcenter.net/iau/MPCORB/MPCORB.DAT')
    with open('MPCORB.DAT', 'w') as fp:
        fp.write(r.text)

def readthedata():
    """
    Constructs a table with semi-major axis and eccentricity columns 
    of the first 100000 asteroids in the file MPCORB.DAT
    """
    columnnames = ['Des\'n','H','G','Epoch','M','Peri.','Node','Incl.','e','n','a','U',
                   'Reference','#Obs','#Opp','Arc','rms','Perts','pert2','Computer',
                  'na1','na2','na3','na4']
    usecols = ['e','a']
    table1 = pd.read_fwf('MPCORB.DAT',skiprows=43,nrows=100000,header=None,names=columnnames,usecols=usecols)
    return table1

def plotthedata(table1,x1=1,x2=5.5):
    """
    Plots the semimajor axis and eccentricity of each asteroid in the table.
    generates lines and labels as in https://ssd.jpl.nasa.gov/?dist_ae_ast,
    with additional lines marking the semimajor axes of planets.
    """
    fig,ax = plt.subplots(1,1)
    fig.set_size_inches(12,10)
    fig.tight_layout()
    
    ax.set_xlim(x1-.01,x2+.01) #adjusted to avoid errors when x1=x2 from the interact widget
    ax.set_ylim(0.0,1.0)
    
    lc = 'c' #line color
    pc = 'm' #planet color
    
    #generating the horizontal and vertical lines marking the different groups
    verticals = [1.7,2.0,2.1,2.3,2.5,2.8,3.3,3.7,4.2,5.05,5.4]
    heights = [0.18,0.18,1,1,1,1,0.35,0.35,0.35,1,1]
    for n in range(len(verticals)):
        ax.vlines(verticals[n],0,heights[n], color=lc, linewidth=1, linestyle = ':')
    
    ax.hlines(0.18, 1.7, 2, color=lc, linewidth=1, linestyle = ':')
    ax.hlines(0.35, 2.7, 3.3, color=lc, linewidth=1, linestyle = ':')
    ax.hlines(0.3, 3.3, 3.7, color=lc, linewidth=1, linestyle = ':')
    ax.hlines(0.35, 3.7, 4.2, color=lc, linewidth=1, linestyle = ':')
    
    #generating the labels for each group of asteroids
    group_a = [1.72,2.12,2.32,2.52,2.82,3.32,3.72,5.07]
    group_e = [0.02,0.72,0.72,0.72,0.37,0.32,0.37,0.72]
    group_names = ['Hungaria Group', 'Flora Family', 'Main Belt (zone I)', 'Main Belt (zone II)', 
                   'Main Belt (zone III)', 'Cybele Group','Hilda Group', 'Trojan Group']
    for n in range(len(group_a)):
        isvisible = False
        if group_a[n] < x2 and group_a[n] >= x1:
            isvisible = True # adjusting what is visible to avoid labels being visible off the graph
        ax.text(group_a[n], group_e[n], group_names[n], color=lc, fontsize=11, rotation='vertical',visible=isvisible)
    
    #generating lines and labels for planets
    #source for planets https://nssdc.gsfc.nasa.gov/planetary/factsheet/planet_table_ratio.html
    planet_a = [0.387,0.723,1.0,1.52,5.20,9.58]
    planet_names = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn']
    for n in range(len(planet_a)):
        ax.vlines(planet_a[n], 0, 1, color=pc, linewidth=1)
        isvisible = False
        if planet_a[n] < x2 and planet_a[n] >= x1:
            isvisible = True
        ax.text(planet_a[n]+0.02, 0.52, planet_names[n], color=pc, fontsize=11, rotation='vertical',visible=isvisible)
    
    ax.set_title('Asteroids Distribution')
    ax.set_xlabel('semimajor axis (AU)')
    ax.set_ylabel('eccentricity')
    
    ax.plot(table1['a'], table1['e'], color='b', marker='.', linestyle='None',markersize=1);

def interactive_asteroid_plot(table1):
    """
    plots the data table with the range for the semimajor axis being adjustable
    """
    interact(plotthedata,table1=fixed(table1), x1=(0,10,0.05), x2=(0,10,0.05))
