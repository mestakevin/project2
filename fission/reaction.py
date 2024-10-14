#fission reaction methods
import numpy as np

# Method for fission reaction
def fissionReaction(neutron_pos, Barium, Krypton, Neutron):
    # When a neutron hits Uranium, simulate the fission
    print("Fission reaction occurred!")
    # Replace Uranium with fission products and release energy
    # Velocity increase are relative.
    barium = Barium(neutron_pos, (10000 * np.random.rand(3)))  # Random initial velocity
    krypton = Krypton(neutron_pos, (700 * np.random.rand(3)))
    
    # Optionally, release more neutrons in random directions
    new_neutron_1 = Neutron(neutron_pos, (14000 * np.random.rand(3)))
    new_neutron_2 = Neutron(neutron_pos, (14000 * np.random.rand(3)))
    new_neutron_3 = Neutron(neutron_pos, (14000 * np.random.rand(3)))

    # The fission products can be added to the particle list in the main simulation loop
    return [barium, krypton, new_neutron_1, new_neutron_2, new_neutron_3]


    
