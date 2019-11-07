import numpy as np 

def read_data():
    ''' function call : M,a,D,T,u0,v0,zeta0,Ntheta,Nphi,dt,Nt,m1,R1,zhat1,omega1,psi1 = read_data() '''
    data = []
    with open('params','r') as f:
        next(f)
        for i,line in enumerate(f):
            if i not in (4,5,9,10,13,14,17,18,24) and i<25:
                data.append(eval(line.split()[1]))
    M,a,D,T,u0,v0,zeta0,Ntheta,Nphi,dt,Nt,m1,R1,zhat1,omega1,psi1 = data
    return M,a,D,T,u0,v0,zeta0,Ntheta,Nphi,dt,Nt,m1,R1,zhat1,omega1,psi1

def get_grid():
    M,a,D,T,u0,v0,zeta0,Ntheta,Nphi,dt,Nt,m1,R1,zhat1,omega1,psi1=read_data()
    phi, theta = np.linspace(0, 2*np.pi, Nphi), np.linspace(0, np.pi, Ntheta)
    Phi, Theta = np.meshgrid(phi,theta)
    return Phi,Theta
    
# M,a,D,T,u0,v0,zeta0,Ntheta,Nphi,dt,Nt,m1,R1,zhat1,omega1,psi1=read_data()
# print(M,a,D,T,u0,v0,zeta0,Ntheta,Nphi,dt,Nt,m1,R1,zhat1,omega1,psi1)