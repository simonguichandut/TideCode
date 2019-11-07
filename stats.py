#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 03:56:25 2019

@author: gabriel
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sci

M,P,D,A=[[] for i in range(4)]
with open('moondata','r') as f:
    next(f)
    for line in f:
        # print(line)
        # print(line.split(','))
        l = line.split(',')
        if l[0]!='':
            M.append(eval(l[0]))
        else:
            M.append(-1)
        P.append(eval(l[1]))
        D.append(eval(l[2]))
        if len(l)>=4 and l[3]!='\n':
            A.append(eval(l[3]))
        else:
            A.append(-1)
  
#make numpy arrays
M = np.array(M)
P = np.array(P)
D = np.array(D)
A = np.array(A)
#%%         
# histograms
plt.figure(1, figsize = (7, 5))
logbins = np.logspace(np.log10(np.min(P[~(P == -1)])), \
                      np.log10(np.max(P[~(P == -1)])), 50)
plt.hist(P, bins = logbins,color='#0504aa', \
                            alpha=0.7, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xscale('log')
plt.xlabel('Period (h)', fontsize = 16)
plt.ylabel('Frequency', fontsize = 16)

#%%
# histograms
plt.figure(2, figsize = (7, 5))
logbins = np.logspace(np.log10(np.min(M[~(M == -1)])), \
                      np.log10(np.max(M[~(M == -1)])), 20)
plt.hist(M, bins = logbins, color='#0504aa', \
                            alpha=0.7, rwidth=0.85)

plt.xscale('log')
plt.xlabel('Mass (kg)', fontsize = 16)
plt.ylabel('Frequency', fontsize = 16)

#%%
# histograms
plt.figure(3, figsize = (7, 5))
plt.grid(axis='y', alpha=0.75)
logbins = np.logspace(np.log10(np.min(D[~(D == -1)])), \
                      np.log10(np.max(D[~(D == -1)])), 20)
plt.hist(D, bins = logbins, color='#0504aa', \
                            alpha=0.7, rwidth=0.85)
plt.xscale('log')
plt.xlabel('Distance (km)', fontsize = 16)
plt.ylabel('Frequency', fontsize = 16)

#%%
# histograms
plt.figure(4, figsize = (7, 5))
plt.grid(axis='y', alpha=0.75)
plt.hist(A[~(A == -1)], bins = 20, color='#0504aa', \
                            alpha=0.7, rwidth=0.85)
plt.xlabel('Angle of orbit (degree)', fontsize = 16)
plt.ylabel('Frequency', fontsize = 16)


#%% correlatioms
plt.scatter(P, D)
plt.xscale('log')
plt.yscale('log')
plt.ylim([1, 20**10])

#%%
indexes = np.where(~(A == -1) & ~(D == -1))
plt.scatter(A[indexes], D[indexes])
plt.yscale('log')
#%%
indexes = np.where(~(A == -1) & ~(P == -1))
plt.scatter(A[indexes], P[indexes])
plt.yscale('log')

#%%
#make data with APD
indexes = np.where(~(A == -1) & ~(P == -1) & ~(D == -1))
X = np.column_stack((A[indexes], np.log10(P[indexes]), np.log10(D[indexes])))
#normalize X
mean = np.mean(X, axis = 0)
std = np.std(X, axis = 0)
Xnorm = (X - mean) / std

#%%
# plot X in 3D
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(Xnorm[:, 0], Xnorm[:, 1], Xnorm[:, 2], c= 'k')
#%%
# apply gaussian KDE
from scipy.stats import gaussian_kde

kernel = gaussian_kde(Xnorm.T, bw_method = 0.1)
Xnewnorm = kernel.resample(25)
Xnewnorm = Xnewnorm.T
Xnew = Xnewnorm * std + mean
Xnew[:, 1:] = 10 ** (Xnew[:, 1:])

fig = plt.figure(figsize=(16,10))
ax = fig.add_subplot(1, 3, 1)

ax.scatter(X[:, 0], 10 ** X[:, 1], c = 'b')
ax.scatter(Xnew[:, 0], Xnew[:, 1], c = 'r')
ax.set_yscale('log')
ax.set_xlabel('Angle of orbit (degree)', fontsize = 16)
ax.set_ylabel('Period (h)', fontsize = 16)

ax = fig.add_subplot(1, 3, 2)

ax.scatter(X[:, 0], 10 ** X[:, 2], c = 'b')
ax.scatter(Xnew[:, 0], Xnew[:, 2], c = 'r')
ax.set_yscale('log')
ax.set_xlabel('Angle of orbit (degree)', fontsize = 16)
ax.set_ylabel('Distance (km)', fontsize = 16)


ax = fig.add_subplot(1, 3, 3)

ax.scatter(10 ** X[:, 1], 10 ** X[:, 2], c = 'b')
ax.scatter(Xnew[:, 1], Xnew[:, 2], c = 'r')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Period (h)', fontsize = 16)
ax.set_ylabel('Distance (km)', fontsize = 16)
plt.tight_layout()
