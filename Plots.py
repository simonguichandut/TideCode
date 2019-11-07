import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.axes3d as axes3d
from  IO import read_data,get_grid

class Rect:
    def __init__(self,Theta,Phi):
        self.Theta=Theta
        self.Phi=Phi

        # Initialize plot_window
        fig = plt.figure(figsize=(10,6))
        ax = fig.add_subplot(111)
        im = ax.pcolormesh(self.Phi,self.Theta, 0*Theta, cmap='PuOr')

        self.fig,self.ax,self.im = fig,ax,im

    def update(self,data):
        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        self.im = self.ax.pcolormesh(self.Phi-np.pi,self.Theta-np.pi/2, data, cmap='PuOr')
        self.cbar = self.fig.colorbar(self.im,ax=self.ax)

    def set_time(self,t):
        self.ax.set_title('Time = %.3f'%t)


class Mollweide:
    def __init__(self,Theta,Phi):
        self.Theta=Theta
        self.Phi=Phi
        self.Ntheta = np.shape(Theta)[0]
        self.Nphi   = np.shape(Theta)[1]

        # Initialize plot_window
        fig = plt.figure(figsize=(10,6))
        ax = fig.add_subplot(111, projection='mollweide')
        im = ax.pcolormesh(Phi-np.pi,Theta-np.pi/2, 0*Theta, cmap='PuOr')
        # im = ax.pcolormesh(Phi,Theta-np, 0*Theta, cmap='PuOr')
        self.fig,self.ax,self.im = fig,ax,im

    def rotate(self,data):
        # Plot is shifted by -pi in phi, meaning that the data in the phi=0 half-circle is shown at the -180deg line.
        # To fix this we perform a half rotation of the data array, but only in the phi axis
        return np.roll(data,int(self.Nphi/2)-1,axis=1)

    def update(self,data):

        data = self.rotate(data)

        self.fig.clf()
        self.ax = self.fig.add_subplot(111, projection='mollweide')
        self.im = self.ax.pcolormesh(self.Phi-np.pi,self.Theta-np.pi/2, data, cmap='PuOr')
        self.cbar = self.fig.colorbar(self.im,ax=self.ax)

    def quiver(self,vphi,utheta):
        
        vphi,utheta = self.rotate(vphi) , self.rotate(utheta)
        
        # parsed data so the arrows can be visible
        x,y = np.linspace(0,2*np.pi,self.Nphi)[::10]-np.pi  ,  np.linspace(0,np.pi,self.Ntheta)[::4]-np.pi/2
        vphi , utheta = vphi[::4,::10] , utheta[::4,::10]
        self.q = self.ax.quiver(x,y,vphi,utheta)

    def shadow(self,pos_phi,pos_theta):
        sha = 1-(self.Phi-pos_phi)**4*(self.Theta-pos_theta)**4
        self.imshadow = self.ax.pcolormesh(self.Phi-np.pi,self.Theta-np.pi/2, sha, cmap='gray',alpha=0.9)

    def set_time(self,t):
        self.ax.set_title('Time = %.3f'%t)
        

# Movies of results
def Movie(result,var,plot,scale='lin',mask=0):
    M,a,D,T,u0,v0,zeta0,Ntheta,Nphi,dt,Nt,m1,R1,zhat1,omega1,psi1 = read_data()
    Theta,Phi = get_grid()

    if plot == 'Rect' or plot == 'Rectangle':
        M=Rect(Theta,Phi)
    elif plot == 'Moll' or plot == 'Mollweide':
        M=Mollweide(Theta,Phi)

    plt.pause(0.1)
    for i in range(Nt):
        data = result[var][i]

        if mask>0:
            data[:mask][:] = np.zeros((1,Nphi))
            data[-mask:][:] = np.zeros((1,Nphi))

        if scale=='log':
            data = np.log10(np.abs(data))

        M.update(data)
        M.set_time(i*dt)
        plt.pause(0.05)





# MISC TESTS  (can ignore)


# # Test of rolling arrays
# phi=np.linspace(0,2*np.pi,100)
# theta=np.linspace(0,np.pi,50)
# Phi,Theta=np.meshgrid(phi,theta)
# M=Mollweide(Theta,Phi)
# data=Phi**2
# M.update(data)
# plt.show()



# # Test moons gab  

# Phi,Theta = get_grid()
# M,a,D,T,u0,v0,zeta0,Ntheta,Nphi,dt,Nt,m1,R1,zhat1,omega1,psi1 = read_data()


# import Moons
# # orbits = [Moons.orbit(100, 1, np.array([0,1,0]), 1, -np.pi / 2)]
# # orbits = [Moons.orbit(10, 1, np.array([0,1,0]), 1, -np.pi / 2),Moons.orbit(5, 1, np.array([0,0,1]), 1, -np.pi / 2)]
# # orbits = [Moons.orbit(R1, m1, zhat1, 1, psi1)]

# orbits = [
# Moons.orbit(1, 1, np.array([1 ,1, 1]), 1, 0),
# Moons.orbit(2, 1, np.array([0 ,0, 1]), 2, 0),
# Moons.orbit(1, 1, np.array([1 ,-2, 3]), 3, 0)]

# G = 6.67430*10**(-11)

# U = Moons.get_U(Phi,Theta, orbits, a, G)

# # M1 = Mollweide(Theta,Phi)
# M2 = Mollweide(Theta,Phi)

# t,dt=0,0.1
# while t<20:

#     # zeta = np.sin(Theta*t)*np.sin(Phi*t)
#     # M1.update(zeta)
#     # M.shadow(3*np.pi/2,3*np.pi/4)

#     for orbit in orbits:
#         orbit.update_psi(dt)
#     M2.update(Moons.get_U(Phi,Theta,orbits,a,G)*t)

#     plt.pause(0.01)
#     # M.imshadow.remove()
#     t+=dt








