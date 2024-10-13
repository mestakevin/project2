#main simulation module

import numpy as np
from particle import Neutron,Uranium,Barium, Krypton
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

def initializeSim():
    nuetron_num = 1
    uranium_num = 1
    nuetron_list = []
    uranium_list = []
    box_dim = [1,1,1]
    pos_1 = np.array([0.25,0.0,0.0])
    vel_1 = np.array([1.0,0.0,0.0])
    
    pos_2 = np.array([0.75,0.0,0.0])
    vel_2 = np.array([-1.0,0.0,0.0])

    
    for i in range(nuetron_num):
        nuetron_list.append(Neutron(pos_1, vel_1) )

    for i in range(uranium_num):
        uranium_list.append(Uranium(pos_2, vel_2) )


    return nuetron_list, uranium_list, box_dim

def run_Simulation():
        nuetron_list, uranium_list, box_dim = initializeSim()
        dt = 1.0e-3
        drag_coeff = 1
        time_limit = 1.0e0
        nuetron_pos_list = []
        uranium_pos_list = []
        time = 0

        while time < time_limit:
            #for i in range(len(nuetron_list)):
            #   this_neutron is equals nuetron_list[i]
            
            for i,this_nuetron in enumerate(nuetron_list):
                this_nuetron.move(drag_coeff, dt)
                nuetron_pos_list.append(this_nuetron.getPos())    
                
                for i,other_particle in enumerate(uranium_list):
                    this_nuetron.collideParticle(other_particle)
                this_nuetron.collideWall(box_dim)
                

            for i,this_uranium in enumerate(uranium_list):
                this_uranium.move(drag_coeff, dt)
                uranium_pos_list.append(this_uranium.getPos())
                for i,other_particle in enumerate(nuetron_list):
                    this_uranium.collideParticle(other_particle)
                this_uranium.collideWall(box_dim)
            time += dt
    return nuetron_pos_list, uranium_pos_list

def animate_simulation():
    # Get the positions from the simulation
    nuetron_pos_list, uranium_pos_list = run_Simulation()
    
    # Extract positions over time
    nuetron_pos = np.array(nuetron_pos_list)
    uranium_pos = np.array(uranium_pos_list)

    # Set up the figure and 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    
    # Initialize particles as scatter plots
    particle1, = ax.plot([], [], [], 'ro', label='Neutron')  # red dot for neutron
    particle2, = ax.plot([], [], [], 'bo', label='Uranium')  # blue dot for uranium

    # Function to initialize the animation
    def init():
        particle1.set_data([], [])
        particle1.set_3d_properties([])
        particle2.set_data([], [])
        particle2.set_3d_properties([])
        return particle1, particle2

    # Function to update the positions of the particles for each frame
    def update(frame):
        # Use lists/arrays with set_data and set_3d_properties
        particle1.set_data([nuetron_pos[frame][0]], [nuetron_pos[frame][1]])
        particle1.set_3d_properties([nuetron_pos[frame][2]])
        particle2.set_data([uranium_pos[frame][0]], [uranium_pos[frame][1]])
        particle2.set_3d_properties([uranium_pos[frame][2]])
        return particle1, particle2

    # Create the animation
    ani = FuncAnimation(fig, update, frames=len(nuetron_pos), init_func=init, blit=True, interval=50)

    # Display the animation
    plt.legend()
    plt.show()
    #ani.save('particle_simulation.gif', writer='imagemagick', fps=30)

# Run the animation
animate_simulation()

