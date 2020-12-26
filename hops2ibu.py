#!/usr/bin/env -S python -u
import numpy as np
import matplotlib.pyplot as plt
import sys

# SOURCES:
# http://univers-biere.net/amertume.php
# https://realbeer.com/hops/research.html

# INITIALIZATION
number_hops = int(sys.argv[1])
IBU = np.zeros(number_hops) # IBU brought by each hops sort
util = np.zeros(number_hops) # % of utilization for each hops sort
hops_masses = np.zeros(number_hops) # mass of hops for boiling, in grams 
hops_alphas = np.zeros(number_hops) # alpha, in %
hops_times =  np.zeros(number_hops) # time spent boiling, in minutes
print('... Brewing with ' + str(number_hops) + ' types of hops ...')
loss = 5 # volume lost during boiling

# USER INPUT
final_density = float(input('Post-boiling density? (grams/liter): '))
final_volume = float(input('Post-boiling volume? (liters): '))

pre_boil_volume = final_volume + loss
pre_boil_density = final_density * final_volume/pre_boil_volume

for n in range(number_hops):
    hops_masses[n] = float(input('mass of hops type ' + str(n+1) + ' (grams): '))
    hops_alphas[n] = float(input('alpha concentration of hops type ' + str(n+1) + ' (%): '))
    hops_times[n] = float(input('boiling time of hops type ' + str(n+1) + ' (min.): '))

# COMPUTE
for n in range(number_hops):
    if pre_boil_density > 1050:
	    cdensity = 1+(pre_boil_density/1000-1.05)/0.2# density correction factor
    else: 
	    cdensity = 1
    util[n] = 1.65*0.000125**(final_density/1000-1)*(1-np.exp(-0.04*hops_times[n]))/4.15
    IBU[n] = hops_masses[n]*util[n]*hops_alphas[n]*10/(final_volume*cdensity)

IBU_total = np.sum(IBU)

# DISPLAY
for n in range(number_hops):
    print('hop number ' + str(n+1) + ':')
    print('\t used at ' + '{0:.2f}'.format(util[n]*100) + ' %')
    print('\t brings ' + '{0:.2f}'.format(IBU[n]) + ' IBU')

print('--- final result is ' + '{0:.2f}'.format(IBU_total) + ' IBU')
