#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 16:47:42 2019

@author: gabriel
"""
import numpy as np

def get_xhat_yhat(zhat):
    if zhat[0] == 0:
        xhat= np.array([1, 0, 0])
        yhat = np.array([0, zhat[2], -zhat[1]])
    else:
        c = 1 / np.sqrt(1 + zhat[2] **2 / zhat[0] ** 2)
        xhat = c * np.array([-zhat[2] / zhat[0], 0, 1])
        if xhat[0] < 0:
            xhat *= -1
        yhat = np.cross(zhat, xhat)
    return xhat, yhat

class orbit(object):
    def __init__(self, R, M, zhat, omega, psi_0):
        self.R = R
        self.M = M
        zhat = zhat / np.linalg.norm(zhat)
        xhat, yhat = get_xhat_yhat(zhat)
        self.P = np.column_stack((xhat, yhat, zhat))
        self.omega = omega
        self.psi = psi_0
    
    def update_psi(self, dt):
        self.psi += self.omega * dt
        
    def get_pos(self):
        rhat = self.R * np.array([np.cos(self.psi), np.sin(self.psi), 0]).reshape((-1, 1))
        r = np.dot(self.P, rhat)
        return r


def get_U(phi, theta, orbits, a, G):
    U = np.zeros(phi.shape)
    for orbit in orbits:
        r = orbit.get_pos()
        costhetap = np.sin(theta) * np.cos(phi) * r[0] + \
                    np.sin(theta) * np.sin(phi) * r[1] + \
                    np.cos(theta) * r[2]
        costhetap = costhetap / np.linalg.norm(r)
        Rp = np.sqrt(orbit.R ** 2 + a ** 2 - 2 * a * orbit.R * costhetap)
        U -= G * orbit.M / Rp
        
    return U
    