import numpy as np
import time
#import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation
#from mpl_toolkits.mplot3d import Axes3D
from .particle import Neutron, Uranium, Barium, Krypton
from .reaction import heatRelease, dragEnergy

# Function to generate initial particles
def generate_particles(num_neutrons, num_uranium, box_dim):
    particles = []

    # Generate neutrons with high random velocities
    for i in range(num_neutrons):
        pos = np.random.exponential(scale=box_dim/5, size=3).tolist()
        vel = np.random.exponential(scale=50, size=3).tolist()  # Neutrons move faster
        particles.append(Neutron(pos, vel))

    # Generate uranium with lower random velocities
    for j in range(num_uranium):
        pos = np.random.exponential(scale=box_dim/5, size=3).tolist()
        vel = np.random.exponential(scale=10, size=3).tolist()  # Uranium moves slower
        particles.append(Uranium(pos, vel))
    return particles

def total_mass_particles(num_neutrons,num_uranium,num_barium,num_krypton):
    total_mass = num_neutrons * 1 + num_uranium * 235 + num_barium * 141 + num_krypton * 92
    return total_mass

# Function to run the simulation
def run_simulation(num_neutrons, num_uranium, box_dim, dt):
    # Generate initial particles
    start_time = time.time()
    print(start_time)
    particles = generate_particles(num_neutrons, num_uranium, box_dim)
    #all_positions = []

    # counting the number of each partcile in particles list
    count_neutron = int(0)
    count_uranium = int(0)
    count_barium = int(0)
    count_krypton = int(0)
    for particle in particles:
        name = particle.__class__.__name__
        if name == 'Neutron':
            count_neutron += int(1)
        elif name == 'Uranium':
            count_uranium += int(1)
        elif name == 'Barium':
            count_barium += int(1)
        elif name == 'krypton':
            count_krypton += int(1)
    print("Particles count before fission reaction")
    print("Neutron: ", count_neutron)
    print("Uranium: ", count_uranium)
    print("Barium: ", count_barium)
    print("Krypton: ", count_krypton)
    print("Total mass before simulation: ", total_mass_particles(count_neutron,count_uranium,count_barium,count_krypton))
    print()

    num_fission_occur = 0
    total_drag_energy = 0

    while num_uranium > 0:

        #particle_positions = []
        # Move and check particle interactions
        for particle in particles:
            particle.move(drag_coeff=0.47, dt=dt)
            
            vel    = particle.getVel()
            radius = particle.getRadius()
            drag_energy = dragEnergy(dt, vel, radius)
            total_drag_energy += drag_energy

            particle.collideWall([box_dim, box_dim, box_dim])  # Wall collision
            #particle_positions.append(particle.getPos())  # Collect current position 

        # Check for particle collisions and fission
        for particle in particles:
            for other_particle in particles:
                particle_name = particle.__class__.__name__
                other_particle_name = other_particle.__class__.__name__

                # Check if fission occurred
                if (particle_name == 'Neutron' and other_particle_name == 'Uranium') or (particle_name == 'Uranium' and other_particle_name == 'Neutron'):
                    fission_products = particle.collideParticle(other_particle)
                    if fission_products is not None:
                        # Update particle list to include new particles
                        particles.extend(fission_products)
                        particles.remove(particle)
                        particles.remove(other_particle)
                        num_uranium -= 1
                        num_fission_occur += 1
                        break
                else:
                    particle.collideParticle(other_particle)
                    #particle_positions.append(particle.getPos())

    end_time = time.time()
    print(end_time)
    total_time = end_time-start_time

    
    temp_change, total_fission_energy = heatRelease(num_fission_occur, box_dim, total_drag_energy)

    return particles,temp_change, total_time

# Run and visualize the simulation

def num_input(prompt):
        try:
            num = float(input(prompt))
        except ValueError:
            num = num_input("Invalid input, please enter a number: ")
        return num



def main():
#if __name__ == "__main__":
    num_neutrons = int(num_input("Please enter how many neutrons to generate within the box\n>"))
    num_uranium = int(num_input("Please enter how many uraniums to generate within the box\n>"))
    box_dim = 1.0e-2     # Must be in meter unit
    dt = 1e-3
    initial_water_temp = 25.0 # in Celcius assumed room temperature

    print("Initial Water Temp:",initial_water_temp )
    particles, temp_change, total_time = run_simulation(num_neutrons, num_uranium, box_dim, dt)
    print("Temp Change:", temp_change)
    current_water_temp = temp_change + initial_water_temp   # in Celcius
    print("Final Water Temperature:", current_water_temp)
            
    # counting the number of each partcile in particles list after finishing the fission reaction
    count_neutron = int(0)
    count_uranium = int(0)
    count_barium = int(0)
    count_krypton = int(0)
    for particle in particles:
        name = particle.__class__.__name__
        if name == 'Neutron':
            count_neutron += int(1)
        elif name == 'Uranium':
            count_uranium += int(1)
        elif name == 'Barium':
            count_barium += int(1)
        elif name == 'Krypton':
            count_krypton += int(1)
    print("Particles count after fission reaction")
    print("Neutron:", count_neutron)
    print("Uranium:", count_uranium)
    print("Barium:", count_barium)
    print("Krypton:", count_krypton)
    print("Total mass after simulation: ", total_mass_particles(count_neutron,count_uranium,count_barium,count_krypton))
    print("Total time elapse:",total_time)




