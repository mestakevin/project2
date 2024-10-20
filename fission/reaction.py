# fission reaction methods
import numpy as np


# Method for fission reaction
def fissionReaction(uranium_pos, Barium, Krypton, Neutron):
    """
    Executes logic for fission reaction between Uranium object and Neutron object

    Paramters:
        uranium_pos (list): position of the Uranium object
        Barium (Barium): Barium object that was created
        Krypton (Krypton): Kyrpton object that was created
        Neutron (Neutron): Neutron that collided into Uranium object
    Returns:
        list: A list with updated Barium object, Krypton object, 3 Neutron objects with randomly determined velocities
    """
    # When a neutron hits Uranium, simulate the fission

    # Replace Uranium with fission products and release energy
    # Velocity increase are relative.
    pos = uranium_pos
    velocity = [np.random.uniform(-1, 1, 3) for i in range(5)]
    barium = Barium(pos, (10 * velocity[0]))  # Random initial velocity
    krypton = Krypton(pos, (7 * velocity[1]))

    # Optionally, release more neutrons in random directions
    new_neutron_1 = Neutron(pos, (14 * velocity[2]))
    new_neutron_2 = Neutron(pos, (14 * velocity[3]))
    new_neutron_3 = Neutron(pos, (14 * velocity[4]))

    # The fission products can be added to the particle list in the main simulation loop
    return [barium, krypton, new_neutron_1, new_neutron_2, new_neutron_3]


def dragEnergy(dt, velocity, radius):
    """
    Calculates the amount of energy transferred to the surrounding water as particles move through box

    Parameters:
        dt (float): The time step for simulation
        velocity (list): The vel attribute of a particle
        radius (float): The radius of the particle
    Returns:
        float: The amount of energy transferred(lost) to surrounding water
    """
    # Drag force heat transfer
    vel = np.linalg.norm(velocity)
    if np.isnan(vel):
        print("Warning: Invalid velocity detected!")
    cross_sectional_area = np.pi * (radius**2)
    drag_coefficient = 0.47  # assuming spherical particles
    water_density = 1000  # kg/m^3 for water

    # Drag force calculation (F_drag = 0.5 * Cd * rho * A * v^2)
    drag_force = (
        0.5 * drag_coefficient * water_density * cross_sectional_area * (vel**2)
    )

    # Work done by drag (W_drag = F_drag * distance traveled)
    distance_traveled = vel * dt  # approximation for small dt
    work_done_by_drag = drag_force * distance_traveled  # energy in joules

    # Add the energy dissipated by this particle to the total drag energy

    return abs(work_done_by_drag)


def heatRelease(num_fission_rxn, box_dim, total_drag_energy):
    """
    Calculates the change of temperature of the water in the box based on how many fission reactions occurred and the total drag energy

    Parameters:
        num_fission_rxn (int): The number of fission reactions that occurred during simulation
        box_dim (float): Half the length of the box the simulation takes place in
        total_drag_energy (float): The total amount of energy transferred to the water due to drag

    Returns:
        float: The temperature change of the water in the box
        float: The energy released from the fission reactions

    """
    # calculating the volume of water tank and its water capacity
    box_vol = (box_dim * 2) ** 3  # in meter cubed
    mass_water = 1000 * box_vol  # in kg, water density is equal to 1000 Kg/m^3
    specific_heat = 4184  # c = 4184 J/kg.c

    # Energy released per fission and total energy
    fission_energy = 2.97 * 10e-11  # energy in joules per fission reaction
    total_fission_energy = num_fission_rxn * fission_energy

    # Total energy transferred to the water
    total_energy_to_water = total_fission_energy + total_drag_energy

    # Temperature change in the water tank due to fission and drag forces
    temp_change = total_energy_to_water / (mass_water * specific_heat)  # in Celsius

    return temp_change, total_fission_energy
