#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 01:32:54 2019

@author: gabriel
"""
from Moons import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

Nmoons = 2

# test orbites
r = [0 for i in range(Nmoons)]
pastpoints = [0 for i in range(Nmoons)]
plot_planets = [0 for i in range(Nmoons)]



# orbits = [orbit(3, 1, np.array([0,0,1]), 1, 0),
#           orbit(3, 1, np.array([0 ,1, 1]), 1, np.pi/2),
#           orbit(3, 1, np.array([-1 ,0, -1]), 1, 0)]

orbits = [orbit(3, 1, np.array([0,0,1]), 1, 0),
          orbit(3, 1, np.array([0 ,0, 1]), 1, np.pi)]



fig = plt.figure()
plt.close()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(0, 0, 0, 'ko', s = 500)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])

dt = 0.1

#intializar
for i in range(Nmoons):
    r[i] = orbits[i].get_pos()
    pastpoints[i] = r[i]

    plot_planets[i] = ax.scatter(r[i][0], r[i][1], r[i][2], facecolor = 'k')

# plt.pause(0.05)

# Hide grid lines
ax.grid(False)

# Hide axes ticks
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])


for i in range(Nmoons):
    plot_planets[i].remove()

for i in range(200):
    for j in range(Nmoons):
        orbits[j].update_psi(dt)
        r[j] = orbits[j].get_pos()
        # if orbits[j].psi < 2 * np.pi + 0.2:
        pastpoints[j] = np.hstack((pastpoints[j][:, [-1]], r[j]))
        ax.plot(pastpoints[j][0, :], pastpoints[j][1, :], pastpoints[j][2, :], 'k')

    
        plot_planets[j] =  ax.scatter(r[j][0], r[j][1], r[j][2], facecolor = 'k')
    # plt.pause(0.05)
    fig.savefig('./png/%06d.png'%(i+1))

    for j in range(Nmoons):
        plot_planets[j].remove()