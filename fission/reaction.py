#fission reaction methods
import numpy as np

# Method for fission reaction
def fissionReaction(uranium_pos, Barium, Krypton, Neutron):
    # When a neutron hits Uranium, simulate the fission
    print("Fission reaction occurred!")
    # Replace Uranium with fission products and release energy
    # Velocity increase are relative.
    barium = Barium(uranium_pos, (10 * np.random.uniform(-1, 1, 3)))  # Random initial velocity
    krypton = Krypton(uranium_pos, (7 * np.random.uniform(-1, 1, 3)))
    
    # Optionally, release more neutrons in random directions
    new_neutron_1 = Neutron(uranium_pos, (14 * np.random.uniform(-1, 1, 3)))
    new_neutron_2 = Neutron(uranium_pos, (14 * np.random.uniform(-1, 1, 3)))
    new_neutron_3 = Neutron(uranium_pos, (14 * np.random.uniform(-1, 1, 3)))

    # The fission products can be added to the particle list in the main simulation loop
    return [barium, krypton, new_neutron_1, new_neutron_2, new_neutron_3]

def dragEnergy(dt, velocity, radius):
    # Drag force heat transfer
    vel = np.linalg.norm(velocity)  
    if np.isnan(vel):
        print("Warning: Invalid velocity detected!")
    cross_sectional_area = np.pi * (radius ** 2)
    drag_coefficient = 0.47  # assuming spherical particles
    water_density = 1000  # kg/m^3 for water

    # Drag force calculation (F_drag = 0.5 * Cd * rho * A * v^2)
    drag_force = 0.5 * drag_coefficient * water_density * cross_sectional_area * (vel ** 2)

    # Work done by drag (W_drag = F_drag * distance traveled)
    distance_traveled = vel * dt  # approximation for small dt
    work_done_by_drag = drag_force * distance_traveled  # energy in joules
    
    # Add the energy dissipated by this particle to the total drag energy

    return work_done_by_drag

def heatRelease(num_fission_rxn, box_dim, total_drag_energy):
    # calculating the volume of water tank and its water capacity
    box_vol = box_dim**3  # in meter cubed
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
