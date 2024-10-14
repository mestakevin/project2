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


    
