#! /usr/bin/env python 
import numpy as np
import matplotlib.pyplot as plt
import sys

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height.
    from https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py"""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{:.0f}'.format(height), xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

# SOURCES:
# http://univers-biere.net/amertume.php
# https://realbeer.com/hops/research.html

step = 10 # in percent
steps = np.arange(0,110,step)/100

# INITIALIZATION
number_hops = 2#int(sys.argv[1])
util = np.zeros(number_hops) # % of utilization for each hops sort
hops_masses = np.zeros([number_hops,len(steps)]) # mass of hops for boiling, in grams 
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

for n in range(number_hops):
    hops_alphas[n] = float(input('alpha concentration of hops type ' + str(n+1) + ' (%): '))
    hops_times[n] = float(input('boiling time of hops type ' + str(n+1) + ' (min.): '))
#hops_alphas = [14,10]
#hops_times = [80,60]

# COMPUTE
for n in range(number_hops):
    if pre_boil_density > 1050:
        cdensity = 1+(pre_boil_density/1000-1.05)/0.2# density correction factor
    else: 
        cdensity = 1
    util[n] = 1.65*0.000125**(final_density/1000-1)*(1-np.exp(-0.04*hops_times[n]))/4.15
for ind,current_IBU_proportion in enumerate(steps):
    hops_masses[0,ind] = current_IBU_proportion*IBU_target*final_volume*cdensity/(util[0]*hops_alphas[0]*10)
    hops_masses[1,ind] = (1-current_IBU_proportion)*IBU_target*final_volume*cdensity/(util[1]*hops_alphas[1]*10)

# DISPLAY
width = step/500
offset = step/800
fig, ax = plt.subplots()
rects0 = ax.bar(steps-offset, hops_masses[0], width, label='Hop1' + ' (alpha=' + str(hops_alphas[0]) + '%)')
rects1 = ax.bar(steps+offset, hops_masses[1], width, label='Hop2' + ' (alpha=' + str(hops_alphas[1]) + '%)')

autolabel(rects0)
autolabel(rects1)

ax.set_ylabel('mass (g)')
ax.set_title('proportion of hops (mass)')
ax.set_xticks([])
ax.legend()

fig.tight_layout()
plt.show()
