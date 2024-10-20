import numpy as np
import time
from .particle import Neutron, Uranium, Barium, Krypton
from .reaction import heatRelease, dragEnergy


# Function to generate initial particles
def generate_particles(num_neutrons, num_uranium, box_dim):
    """
    Distributes Neutron and Uranium objects within the dimensions of the box according to an exponential distribution

    Parameters:
        num_nuetrons (int): The number of Neutron objects to disperse within box
        num_uranium (int): The number of Uranium objects to disperse wihin box
        box_dim (float): Half of the length of one side of the cubic box the particles will be simulated in

    Returns:
        list: A list containing the Nuetron and Uranium objects generated
    """
    particles = []

    # Generate neutrons with high random velocities
    for i in range(num_neutrons):
        pos = np.random.exponential(scale=box_dim / 5, size=3).tolist()
        vel = np.random.exponential(scale=50, size=3).tolist()  # Neutrons move faster
        particles.append(Neutron(pos, vel))

    # Generate uranium with lower random velocities
    for j in range(num_uranium):
        pos = np.random.exponential(scale=box_dim / 5, size=3).tolist()
        vel = np.random.exponential(scale=10, size=3).tolist()  # Uranium moves slower
        particles.append(Uranium(pos, vel))
    return particles


def total_mass_particles(num_neutrons, num_uranium, num_barium, num_krypton):
    """
    Calculates the total mass of the system in amu

    Parameters:
        num_neutrons (int): The number of Neutron objects present in simulation
        num_uranium (int): The number of Uranium objects present in simulation
        num_barium (int): The number of Barium objects present in simulation
        num_krypton (int): The number of Krypton objects present in simulation

    Returns:
        int: The total mass of the system in amu
    """
    total_mass = (
        num_neutrons * 1 + num_uranium * 235 + num_barium * 141 + num_krypton * 92
    )
    return total_mass


# Function to run the simulation
def run_simulation(num_neutrons, num_uranium, box_dim, dt):
    """
    Executes logic that runs entire simulation with particle and wall collisions, fission reactions and determination of mass for one simulation run (until no more Uranium objects remain)

    Parameters:
        num_neutrons (int): The number of Neutron objects initially present in simulation
        num_uranium (int): The number of Uranium objects initially present in simulation
        box_dim (float): Half of the length of one side of the cubic box the particles will be simulated in
        dt (float): The size of time step for updating particle's position and velocities

    Returns:
        list: A list named particles that contains all the Particle objects in no particular order
        float: The change in temperature within the box
        float: The total time elapsed from particle generation to end of simulation
    """
    # Generate initial particles
    start_time = time.time()
    particles = generate_particles(num_neutrons, num_uranium, box_dim)

    # counting the number of each partcile in particles list
    count_neutron = int(0)
    count_uranium = int(0)
    count_barium = int(0)
    count_krypton = int(0)
    for particle in particles:
        name = particle.__class__.__name__
        if name == "Neutron":
            count_neutron += int(1)
        elif name == "Uranium":
            count_uranium += int(1)
        elif name == "Barium":
            count_barium += int(1)
        elif name == "krypton":
            count_krypton += int(1)
    print("Particles count before fission reaction")
    print("Neutron: ", count_neutron)
    print("Uranium: ", count_uranium)
    print("Barium: ", count_barium)
    print("Krypton: ", count_krypton)
    print(
        "Total mass before simulation: ",
        total_mass_particles(count_neutron, count_uranium, count_barium, count_krypton),
    )
    print()

    num_fission_occur = 0
    total_drag_energy = 0

    while num_uranium > 0:
        # Move and check particle interactions
        for particle in particles:
            particle.move(drag_coeff=0.47, dt=dt)

            vel = particle.getVel()
            radius = particle.getRadius()
            drag_energy = dragEnergy(dt, vel, radius)
            total_drag_energy += drag_energy

            particle.collideWall([box_dim, box_dim, box_dim])  # Wall collision

        # Check for particle collisions and fission
        for particle in particles:
            for other_particle in particles:
                particle_name = particle.__class__.__name__
                other_particle_name = other_particle.__class__.__name__

                # Check if fission occurred
                if (
                    particle_name == "Neutron" and other_particle_name == "Uranium"
                ) or (particle_name == "Uranium" and other_particle_name == "Neutron"):
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

    end_time = time.time()
    total_time = end_time - start_time

    temp_change, total_fission_energy = heatRelease(
        num_fission_occur, box_dim, total_drag_energy
    )
    return particles, temp_change, total_time


def num_input(prompt):
    """
    Obtains a number from the user to be used for simulating

    Parameters:
        prompt (str): Message to be displayed to prompt user to input a number
    Returns:
        float: User inputted number
    """
    try:
        num = float(input(prompt))
    except ValueError:
        num = num_input("Invalid input, please enter a number: ")
    return num


def main():
    """
    Executes logic for one simulation, with user inputted initial values and to be executed by 'main_script'

    Returns:
        None
    Outputs:
        Displays intial and final mass, the temperature change of the water within the box, and the total time elapsed
    """
    num_neutrons = int(
        num_input("Please enter how many neutrons to generate within the box\n>")
    )
    num_uranium = int(
        num_input("Please enter how many uraniums to generate within the box\n>")
    )
    box_dim = num_input(
        "Please enter a value for half the length of the box\n>"
    )  # Must be in meter unit
    dt = num_input("Please enter the time step for the simulation\n>")
    initial_water_temp = 25.0  # in Celcius assumed room temperature

    print("Initial Water Temp:", initial_water_temp)
    particles, temp_change, total_time = run_simulation(
        num_neutrons, num_uranium, box_dim, dt
    )
    print("Temp Change:", temp_change)
    current_water_temp = temp_change + initial_water_temp  # in Celcius
    print("Final Water Temperature:", current_water_temp)

    # counting the number of each partcile in particles list after finishing the fission reaction
    count_neutron = int(0)
    count_uranium = int(0)
    count_barium = int(0)
    count_krypton = int(0)
    for particle in particles:
        name = particle.__class__.__name__
        if name == "Neutron":
            count_neutron += int(1)
        elif name == "Uranium":
            count_uranium += int(1)
        elif name == "Barium":
            count_barium += int(1)
        elif name == "Krypton":
            count_krypton += int(1)
    print("Particles count after fission reaction")
    print("Neutron:", count_neutron)
    print("Uranium:", count_uranium)
    print("Barium:", count_barium)
    print("Krypton:", count_krypton)
    print(
        "Total mass after simulation: ",
        total_mass_particles(count_neutron, count_uranium, count_barium, count_krypton),
    )
    print("Total time elapse:", total_time)
