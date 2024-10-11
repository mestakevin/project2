#main simulation module

import numpy as np
from particle import Particle

def run_Simulation():
    time = 0
    pos = np.array([0.0,0.0,0.0])
    vel = np.array([1.0,3.0,5.0])
    drag_coeff = 0.5
    dt = 0.01
    test_particle = Particle(pos,vel)
    
    print(test_particle.getPos())
    print(test_particle.getEng())
    while time < 10:
        test_particle.move(drag_coeff, dt)
        print(test_particle.getPos())
        print(test_particle.getEng())
        time += dt

run_Simulation()

