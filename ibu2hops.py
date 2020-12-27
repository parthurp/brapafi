#!/usr/bin/env -S python -u
import numpy as np
import matplotlib.pyplot as plt
import sys

### FUNCTIONS
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height.
    from https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py"""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{:.0f}'.format(height), xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

def plot_bar(mass_proportions_2hops, offset, masses, width, label):
    curr_plot = ax.bar(mass_proportions_2hops+offset, masses, width=width, label=label)
    return curr_plot
# SOURCES:
# http://univers-biere.net/amertume.php
# https://realbeer.com/hops/research.html

# INITIALIZATION
step = 10; mass_proportions_2hops = np.arange(0,110,step)/100 # from 0 to 100 % (steps of 10%), mass proportion of each hop type
number_hops = int(sys.argv[1])
util = np.zeros(number_hops) # % of utilization for each hops sort
if number_hops == 1:
    hops_masses = 0
elif number_hops == 2:
    hops_masses = np.zeros([number_hops,len(mass_proportions_2hops)]) # mass of hops for boiling, in grams 
elif number_hops == 3:
    hops_masses = np.zeros([number_hops,len(mass_proportions_2hops),len(mass_proportions_2hops)]) # mass of hops for boiling, in grams 
hops_alphas = np.zeros(number_hops) # alpha, in %
hops_times =  np.zeros(number_hops) # time spent boiling, in minutes
print('... Brewing with ' + str(number_hops) + ' types of hops ...')
loss = 5 # volume lost during boiling

# USER INPUT
final_density = float(input('Post-boiling density? (grams/liter): '))
final_volume = float(input('Post-boiling volume? (liters): '))
IBU_target = float(input('Target IBU? '))
#final_density = 1080
#final_volume = 30
#IBU_target = 80

pre_boil_volume = final_volume + loss
pre_boil_density = final_density * final_volume/pre_boil_volume

#for n in range(number_hops):
#    hops_alphas[n] = float(input('alpha concentration of hops type ' + str(n+1) + ' (%): '))
#    hops_times[n] = float(input('boiling time of hops type ' + str(n+1) + ' (min.): '))
hops_alphas = [14,10,8]
hops_times = [80,60,30]

# COMPUTE
for n in range(number_hops):
    if pre_boil_density > 1050:
        cdensity = 1+(pre_boil_density/1000-1.05)/0.2# density correction factor
    else: 
        cdensity = 1
    util[n] = 1.65*0.000125**(final_density/1000-1)*(1-np.exp(-0.04*hops_times[n]))/4.15

if (number_hops == 1):
    hops_masses = IBU_target*final_volume*cdensity/(util*hops_alphas*10)
elif (number_hops == 2):
    for ind,current_IBU_proportion in enumerate(mass_proportions_2hops):
        hops_masses[0,ind] = current_IBU_proportion*IBU_target*final_volume*cdensity/(util[0]*hops_alphas[0]*10)
        hops_masses[1,ind] = (1-current_IBU_proportion)*IBU_target*final_volume*cdensity/(util[1]*hops_alphas[1]*10)
elif (number_hops == 3):
    for ind,current_IBU_proportion in enumerate(mass_proportions_2hops):
        for ind2,current_IBU_proportion2 in enumerate(mass_proportions_2hops[ind:]):
            hops_masses[0,ind,ind2] = current_IBU_proportion*IBU_target*final_volume*cdensity/(util[0]*hops_alphas[0]*10)
            hops_masses[1,ind,ind2] = current_IBU_proportion2*IBU_target*final_volume*cdensity/(util[1]*hops_alphas[1]*10)
            hops_masses[2,ind,ind2] = (1-current_IBU_proportion-current_IBU_proportion2)*IBU_target*final_volume*cdensity/(util[2]*hops_alphas[2]*10)
    pass

# DISPLAY
if (number_hops == 1):
    print('You need ' + '{0:.0f}'.format(hops_masses[0]) + ' grams of this hop! (alpha = ' + '{0:.0f}'.format(hops_alphas[0]) + ' %, boil time = ' + '{0:.0f}'.format(hops_times[0]) + ' min.)')
elif (number_hops == 2):
    width = step/500
    offset = step/400
    fig, ax = plt.subplots()

    for n in range(number_hops):
        curr_plot = plot_bar(mass_proportions_2hops, n*offset, hops_masses[n], width, 'Hop' + str(n+1) + ' (alpha=' + str(hops_alphas[n]) + '%)')
        autolabel(curr_plot)

    ax.set_ylabel('mass (g)')
    ax.set_title('proportion of hops (mass, in grams)')
    ax.set_xticks([])
    ax.legend()

    fig.tight_layout()
    plt.show()

elif (number_hops == 3):
    width = step/500
    offset = step/400
    for ind,val in enumerate(mass_proportions_2hops):
        fig, ax = plt.subplots()

        for n in range(number_hops):
            curr_plot = plot_bar(mass_proportions_2hops, n*offset, hops_masses[n,ind], width, 'Hop' + str(n+1) + ' (alpha=' + str(hops_alphas[n]) + '%)')
            autolabel(curr_plot)

        ax.set_ylabel('mass (g)')
        ax.set_title('proportion of hops (mass, in grams) -- Hops 1 represents ' + '{0:.0f}'.format(val*100) + '% of total hops mass')
        ax.set_xticks([])
        ax.legend()

        fig.tight_layout()
        plt.show()

    print(hops_masses)
