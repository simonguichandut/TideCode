## Main code . run with >> python main.py

import numpy as np
import matplotlib.pyplot as plt
from IO import *
import Plots
import Solver

result = Solver.solve()
print('Finished!')

# Plotting
save = 0       # ENTER: 0 for plotting on screen, 1 for saving frames as png


M,a,D,T,u0,v0,zeta0,Ntheta,Nphi,dt,Nt,m1,R1,zhat1,omega1,psi1 = read_data()
Phi,Theta = get_grid()
M = Plots.Mollweide(Theta,Phi)
if save: plt.close()
for i in range(Nt):

    data = result['z'][i]  # which data to plot

    # Mask data? suggested to do this for 'z' as currently diverging at poles
    data[:4][:] = np.zeros((1,Nphi))
    data[-4:][:] = np.zeros((1,Nphi))

    M.update(data)
    M.set_time(dt*i)

    # With quiver plot
    M.quiver(result['v'][i] , result['u'][i])

    if save:
        M.fig.savefig('./png/%06d.png'%(i+1))
    else:
        plt.pause(0.01)

    # q.remove()


