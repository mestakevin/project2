#main simulation module

import numpy as np
from particle import Neutron,Uranium,Barium, Krypton
import matplotlib as plt

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
        for i,n_pos in enumerate(nuetron_pos_list):
            print('n: ',n_pos[0], '', n_pos[1],'',n_pos[2])
            print('u235: ',uranium_pos_list[i])

    
       


run_Simulation()

