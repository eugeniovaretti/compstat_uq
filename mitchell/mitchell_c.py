#imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

# constants[0] = IstimStart
# constants[1] = IstimEnd
# constants[2] = IstimAmplitude
# constants[3] = IstimPeriod
# constants[4] = IstimPulseDuration

def mitchell(D=0.1,
            tau_in=0.3,
            tau_out=5,
            tau_open=40,
            tau_close=50,
            v_gate=0.13,
            K=8,
            alpha=0.1, #soglia
            ):
    
    nodes = 201
    L = 50
    delta_t = 0.025
    T = 400
    time = np.arange(0, T + delta_t, delta_t)
    
    # domain
    domain_length = L
    max_iter_time = np.int32(T/delta_t)
    print(max_iter_time)

    # physical coefficients
#     D = 0.1

#     tau_in = 0.3
#     tau_out = 5
#     tau_open = 40
#     tau_close = 50
#     v_gate = 0.13   

#     K = 8
#     alpha = 0.1
    Chi = np.sqrt(K)/(2*np.sqrt(2*D))

    # space discretization
    delta_x = domain_length/(nodes-1)
    x = np.arange(0,domain_length+delta_x,delta_x)
    gamma = D*delta_t / (delta_x ** 2)

    # Initialize solution
    u = np.zeros((max_iter_time, nodes))
    w = np.ones((max_iter_time, nodes))

    # Set the initial condition
    #u[0][:] = 0.5*(1.0+np.tanh(-Chi*(x-10)))

    # inner function for solution computation
    def calculate(sol,sol_w):
        for k in range(0, max_iter_time-1, 1):
            for i in range(0, nodes, 1):

                Ut = sol[k][i]
                Wt = sol_w[k][i]

                J_in = Wt*(Ut*Ut*(1.0-Ut))/tau_in
                J_out = - Ut/tau_out
                g_ion = ((1-Wt)/tau_open)*(Ut<v_gate) + ((-Wt)/tau_close)*(Ut>v_gate)

                sol_w[k+1][i] = sol_w[k][i] + delta_t *  g_ion

                I_app = 0.

                for firing in range(10):
                    if (i>10)&(i<15)&(k<(6000*firing)+20)&(k>=(6000*firing)):
                        I_app = 1.0

                if (i==0):

                    

                    # left neumann bc with ghost node
                    sol[k + 1, i] = gamma * (sol[k][i+1] + sol[k][i+1] - \
                    2.0*sol[k][i]) + sol[k][i] + delta_t\
                    * ( J_in + J_out ) 
                else:
                    if (i==(nodes-1)):
                        # right neumann bc with ghost node
                        sol[k + 1, i] = gamma * (sol[k][i-1] + sol[k][i-1] \
                        - 2.0*sol[k][i]) + sol[k][i] + delta_t\
                        *( J_in + J_out )
                    else:
                        # inner nodes
                        sol[k + 1, i] = gamma * (sol[k][i+1] + sol[k][i-1] \
                         - 2.0*sol[k][i]) + sol[k][i] + delta_t\
                         *( J_in + J_out + I_app )

        return sol

    # inner function for gif construction
    def plotsolution(u_k, k):
        # Clear the current plot figure
        plt.clf()

        plt.title(f"Solution at t = {k*delta_t:.3f} [t.u.]")
        plt.xlabel("x")
        plt.ylabel("u")

        plt.plot( x , u_k,  'g', linewidth=2)

        plt.ylim([-0.05,1.05])

        return plt

    # Compute the solution
    u = calculate(u,w)
    
    values = u[:,0] # 0 indica il nodo 0, cambia a seconda


    return time, values
