#fission reaction methods
import numpy as np
from particle import Barium, Krypton, Neutron, Uranium  

# Method for fission reaction
def fissionReaction(self):
    # When a neutron hits Uranium, simulate the fission
    print("Fission reaction occurred!")
    # Replace Uranium with fission products and release energy
    # Velocity increase are relative.
    barium = Barium(self.pos, (10000 * np.random.rand(3)))  # Random initial velocity
    krypton = Krypton(self.pos, (700 * np.random.rand(3)))
    
    # Optionally, release more neutrons in random directions
    new_neutron_1 = Neutron(self.pos, (14000 * np.random.rand(3)))
    new_neutron_2 = Neutron(self.pos, (14000 * np.random.rand(3)))
    new_neutron_3 = Neutron(self.pos, (14000 * np.random.rand(3)))

    # The fission products can be added to the particle list in the main simulation loop
    return [barium, krypton, new_neutron_1, new_neutron_2, new_neutron_3]


    
