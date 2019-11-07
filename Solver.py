''' ODE Solver. Centered derivative in (phi,theta), forward explicit Euler in time '''

import numpy as np
import Moons
import IO    

def solve():

    eps = 0.01
    
    M,a,D,T,u0,v0,zeta0,Ntheta,Nphi,dt,Nt,m1,R1,zhat1,omega1,psi1=IO.read_data()
    dtheta = ((np.pi - 2 * eps)/(Ntheta - 1)) # Jusqu'à pi
    dphi = (2*np.pi/(Nphi)) # Jusqu'à 2pi
    G = 6.67430*10**(-11)
    g = G*M/a**2
    # omega =2*np.pi / (T*3600)
    omega = 0 # force earth stationnary
    
    u = np.zeros([Nt,Ntheta,Nphi]) + u0
    v = np.zeros([Nt,Ntheta,Nphi]) + v0
    z = np.zeros([Nt,Ntheta,Nphi]) + zeta0 
    U = np.zeros([Nt,Ntheta,Nphi])
  
    
    theta_val = np.linspace(eps, np.pi - eps, Ntheta)
    phi_val = np.linspace(0, 2 * np.pi, Nphi + 1)[:-1]
    
    phi, theta = np.meshgrid(phi_val, theta_val)
    
    # omega1 = 2*np.pi / (1000) # force a rotation
    # psi1 = np.pi/2
    orbits = [Moons.orbit(R1, M, zhat1, omega1, psi1)]

    # Custom moons (can put many)
    # orbits = [Moons.orbit(R1, M, (0,0,1), omega1, psi1) , Moons.orbit(R1, M, (0,1,1), omega1*2, psi1+np.pi/2),
    # Moons.orbit(R1, M, (-1,0,-1), omega1, psi1)]


    U[0] = Moons.get_U(phi, theta, orbits, a, G)
    def t_plus_one(u, v, z, U): 
        up = np.copy(u)
        vp = np.copy(v)
        zp = np.copy(z)
        for i in range(0, Ntheta):
            for j in range(0, Nphi):                 
                if i == 0:
               
                    zp[i,j] = -(D/(a*np.sin(theta_val[i])))*((np.cos(theta_val[i]))*u[i,j] + \
                      np.sin(theta_val[i])*((u[i + 1, j] - u[i, j])/(dtheta) + ( v[i,(j + 1) % Nphi]-v[i, j - 1] )/(2*dphi))) *dt + z[i,j]   
                
                    up[i,j] = dt * (-(g/a)*(z[i + 1,j] - z[i,j])/(dtheta) - \
                      (1/a)*(U[i + 1, j]-U[i, j])/(dtheta) + 2*omega*np.cos(theta_val[i])*v[i,j]) + u[i,j]
                    
                elif i == Ntheta - 1:
                    zp[i,j] = -(D/(a*np.sin(theta_val[i])))*((np.cos(theta_val[i]))*u[i,j] + \
                      np.sin(theta_val[i])*((u[i, j] - u[i - 1, j])/(dtheta) + ( v[i,(j + 1) % Nphi]-v[i, j - 1] )/(2*dphi))) *dt + z[i,j]   
                
                    up[i,j] = dt * (-(g/a)*(z[i,j] - z[i - 1,j])/(dtheta) - \
                      (1/a)*(U[i, j]-U[i - 1, j])/(dtheta) + 2*omega*np.cos(theta_val[i])*v[i,j]) + u[i,j]

   
                    
                else:
                    
                    zp[i,j] = -(D/(a*np.sin(theta_val[i])))*(np.cos(theta_val[i])*u[i,j]+ \
                      np.sin(theta_val[i])*((u[i + 1,j]-u[i - 1,j])/(2*dtheta) + ( v[i,(j + 1) % Nphi]-v[i,j-1] )/(2*dphi))) *dt + z[i,j]   
                
                    up[i,j] = dt * (-(g/a)*(z[i + 1,j]-z[i-1,j])/(2*dtheta) - \
                      (1/a)*(U[i + 1,j]-U[i-1,j])/(2*dtheta) + 2*omega*np.cos(theta_val[i])*v[i,j])+u[i,j]
                
                vp[i,j] = v[i,j] + dt * (-2 * omega * np.cos(theta_val[i]) * u[i,j] - \
                     1/(a*np.sin(theta_val[i])) * (g*(z[i,(j + 1) % Nphi] - z[i,j-1])/(2*dphi) + (U[i,(j + 1) % Nphi] - U[i,j-1])/(2*dphi)))
            
        for orbit in orbits:    
          orbit.update_psi(dt)
        Up = Moons.get_U(phi, theta, orbits, a, G)
        # print(orbits[0].psi)
        return up, vp, zp, Up
    
    
     
    for k in range(0,Nt-1):
        print('Step #%d'%k)
      # Code pour solve dans le temps
        u[k+1,:,:],v[k+1,:,:],z[k+1,:,:], U[k+1,:,:] = t_plus_one(u[k,:,:],v[k,:,:],z[k,:,:],U[k,:,:])

      # Boundary conditions brute force : force all to zero at poles
        u[k+1,0,:] = np.zeros((1,Nphi))
        u[k+1,-1,:] = np.zeros((1,Nphi))
        v[k+1,0,:] = np.zeros((1,Nphi))
        v[k+1,-1,:] = np.zeros((1,Nphi))
        z[k+1,0,:] = np.zeros((1,Nphi))
        z[k+1,-1,:] = np.zeros((1,Nphi))
     
     #Sauvegarde des résultats 
    result = {"u":u,"v":v,"z":z, "U":U}
    return result
