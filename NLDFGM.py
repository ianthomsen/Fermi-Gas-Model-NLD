#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"Created on Wed Mar 05 00:26:02 2023, @author: ianthomsen"

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Get isotope and isotope ground energy
isotope = input("Enter Isotope & J: ")
strground = input("Enter Ground Energy: ")
# strenergy = input("Enter Yrast Energy: ")


########################## Constant Temperature Section ##########################

# Load constant temperature model data and put it into an array of size 100
with open('/Users/ianthomsen/Downloads/Shell Model/sm' + isotope + '.txt', "r") as c:
    states = []
    d = c.read()
    e = d.replace('+', '')
    states = e.split()
 
#    d = c.readlines()
#    d = d[:99]
#    states = []
#    for line in d:
#        states.append(line.split()[0])

# Convert its content into floats
for i in range(len(states)):
    states[i] = float(states[i])

# For each integer energy bin, find the number of states in that bin by summing up how many times that integer appears
bins = [0 for i in range(len(states))]

# Since all of the CTM energy files are biased to 0, add the energy shift to each energy in the file
ground = float(strground)

# Add the energy shift to each array element and then convert to an integer
for i in range(len(states)):
    states[i] += ground
    print(round(states[i], 3))
    states[i] = int(states[i])
    
# Fill each energy bin with the number of states belonging to that integer energy bin
for i in range(len(states)):
    for j in range(len(states)):
        if states[i] == j:
            bins[j] += 1

# Remove the trailing zeroes after the final nonzero value to preserve a good exponential fit
# while bins[-1] == 0:
#      bins.pop(-1)
# bins = bins[:-1]
        

########################## Moments Method Section #################################

# Load moments method data and put it into an array
with open('/Users/ianthomsen/Downloads/Moments Method/mm' + isotope + '.txt', 'r') as g:
    h = g.read()
    k = h.strip()
    data = k.split()

# Convert its content into floats
for i in range(len(data)):
    data[i] = float(data[i])

# # Initialize arrays and sort full data array into xdata and ydata arrays
fullxdata = []
fullydata = []
for i in range(len(data)):
    if i % 2 == 0:
        fullxdata.append(np.float64(data[i]))
    else:
        fullydata.append(np.float64(data[i]))
        
fullxdata = np.array(fullxdata)
fullydata = np.array(fullydata)

# Truncate xdata and ydata to be the same size as bins so the CT fit works on it and add the energy shift to the xdata so its plotted starting from the right place
truncate = slice(len(bins))
xdata = fullxdata[truncate]
ydata = fullydata[truncate]
        

########################## Plotting/Results Section #################################

# Redefine the length of these arrays to only consider bins up to the 12th bin from the minium to preserve better fitting parameters due to divergence in the data at higher energies
xdata = xdata[11:20]
bins = bins[11:20]
ydata = ydata[11:20]

print(bins)

# Fit both the shell model (SM) and moments method (MM) results with the Fermi gas model (FGM) equation and get the physical parameters T from each fit
smpopt, smpcov = curve_fit(lambda t, sma, smb, p0 = [5, 5]: np.exp(2*(sma*t)**.5)/(12*2**.5*(sma**.25)*t**1.25), xdata, bins)
sma = smpopt[0]

mmpopt, mmpcov = curve_fit(lambda t, mma, mmb, p0 = [5, 5]: np.exp(2*(mma*t)**.5)/(12*2**.5*(sma**.25)*t**1.25), xdata, ydata)
mma = mmpopt[0]

# Get y values from the line of best fit
# smyfit = np.array(sma*np.exp(-smb*xdata))
# mmyfit = np.array(mma*np.exp(-mmb*xdata))

# Get uncertainties for T and E for both fits
# smperr = (np.diag(ctpcov))**.5
# mmperr = (np.diag(mmpcov))**.5
                
# Get the average RMSE per point for the SM and MM
smsum = 0
mmsum = 0
sum = 0
fitsum = 0

# smdiff = (bins - smyfit)**2
# mmdiff = (ydata - mmyfit)**2
# diff = (bins - ydata)**2
# fitdiff = (ydata - smyfit)**2

# for i in range(len(smdiff)):
#     smsum = smsum + smdiff[i]
#     mmsum = mmsum + mmdiff[i]
#     sum = sum + diff[i]
#     fitsum = fitsum + fitdiff[i]
    
# smrmse = (smsum/len(smdiff))**.5
# mmrmse = (mmsum/len(mmdiff))**.5
# rmse = (sum/len(diff))**.5
# fitrmse = (fitsum/len(fitdiff))**.5

# Make and name the graph and plot the shell model results, moments method results, and constant temperature fit to both
plt.rcParams["figure.figsize"] = [6, 5]
plt.rcParams["figure.autolayout"] = True

if isotope[-2] == '.':
    plt.title(isotope[:-3] + ", J = " + isotope[-3:] + " Level Densities")
else:
    plt.title(isotope[:-1] + ", J = " + isotope[-1] + " Level Densities")
    
plt.xlabel("Energy Bin (MeV)")
plt.ylabel("Level Density (MeV^-1)")
plt.plot(xdata, bins, 'o', color = "blue", label = "SM Results")
plt.plot(xdata, ydata, 'o', color = "red", label = "MM Results")
plt.plot(xdata, np.exp(2*(sma*xdata)**.5)/(12*2**.5*(sma**.25)*xdata**1.25), color = "blue", label = "FGM Fit for SM")
plt.plot(xdata, np.exp(2*(mma*xdata)**.5)/(12*2**.5*(sma**.25)*xdata**1.25), color = "red", label = "FGM Fit for MM")
plt.legend()
plt.show()

# Print out all of the parameters
print("SMFG Temp: ", round(sma, 3))
print("MMFG Temp: ", round(mma, 3))
# print("MM Data to SM Fit RMSE: ", round(fitrmse, 3))
# print("Data RMSE: ", round(rmse, 3))
# print("Temp Error: ", smperr[0], "| Edif Error: ", smperr[1])
# print("Temp Error: ", mmperr[0], "| Edif Error: ", mmperr[1])
# print("Energy Bins: ", xdata)
# print("SM States: ", bins)
# print("MM States: ", ydata)
