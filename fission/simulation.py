import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from particle import Neutron, Uranium, Barium, Krypton

# Function to generate initial particles
def generate_particles(num_neutrons, num_uranium, box_dim):
    particles = []

    # Generate neutrons with high random velocities
    for i in range(num_neutrons):
        pos = np.random.uniform(-box_dim, box_dim, 3).tolist()
        vel = np.random.uniform(-100, 100, 3).tolist()  # Neutrons move faster
        particles.append(Neutron(pos, vel))

    # Generate uranium with lower random velocities
    for j in range(num_uranium):
        pos = np.random.uniform(-box_dim/2, box_dim/2, 3).tolist()
        vel = np.random.uniform(-10, 10, 3).tolist()  # Uranium moves slower
        particles.append(Uranium(pos, vel))
    print("func_gen", particles)
    return particles

# Function to run the simulation
def run_simulation(num_neutrons, num_uranium, box_dim, dt):
    # Generate initial particles
    particles = generate_particles(num_neutrons, num_uranium, box_dim)
    all_positions = []

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
    print()
    while num_uranium > 0:

        particle_positions = []
        # Move and check particle interactions
        for particle in particles:
            particle.move(drag_coeff=0.47, dt=dt)
            particle.collideWall([box_dim, box_dim, box_dim])  # Wall collision
            particle_positions.append(particle.getPos())  # Collect current position 

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
                        break
                else:
                    particle.collideParticle(other_particle)
                    particle_positions.append(particle.getPos())

        # Save particle positions for this step
        all_positions.append(particle_positions)

    return particles, all_positions  

def animate_simulation(particles, all_positions, box_dim):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-box_dim, box_dim])
    ax.set_ylim([-box_dim, box_dim])
    ax.set_zlim([-box_dim, box_dim])

    # Define colors for different particle types
    colors = {
        'Neutron': 'blue',
        'Uranium': 'red',
        'Barium': 'green',
        'Krypton': 'orange'
    }

    # Initialize scatter plot (empty at first)
    scat = ax.scatter([], [], [], s=20)

    # Initialize a text box to display particle counts
    text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes)

    def update(frame):
        # Get the positions and states of particles at the current frame
        positions = all_positions[frame]
        xs, ys, zs, cs = [], [], [], []

        # For each particle in the current step, update positions and colors
        for particle, pos in zip(particles, positions):
            xs.append(pos[0])
            ys.append(pos[1])
            zs.append(pos[2])
            cs.append(colors[particle.__class__.__name__])

        # Update the scatter plot with new data
        scat._offsets3d = (xs, ys, zs)
        scat.set_color(cs)

        # Count particles of each type for the current frame
        neutron_count = sum(1 for p in particles if isinstance(p, Neutron))
        uranium_count = sum(1 for p in particles if isinstance(p, Uranium))
        barium_count = sum(1 for p in particles if isinstance(p, Barium))
        krypton_count = sum(1 for p in particles if isinstance(p, Krypton))

        # Update the text box with particle counts
        text.set_text(f'Neutrons: {neutron_count}\nUranium: {uranium_count}\nBarium: {barium_count}\nKrypton: {krypton_count}')
        
        return scat, text

    # Create the animation, animating each frame from the simulation
    anim = FuncAnimation(fig, update, frames=len(all_positions), interval=200, blit=False)

    plt.show()

    # save the animation
    #anim.save('particle_simulation.gif', writer='imagemagick', fps=30)

# Run and visualize the simulation
if __name__ == "__main__":
    num_neutrons = 4
    num_uranium = 1
    box_dim = 1     # Must be in meter unit
    dt = 1e-3

    particles, all_positions = run_simulation(num_neutrons, num_uranium, box_dim, dt)
    print(particles)
            
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
    print("Neutron: ", count_neutron)
    print("Uranium: ", count_uranium)
    print("Barium: ", count_barium)
    print("Krypton: ", count_krypton)
    #animate_simulation(particles, all_positions, box_dim)
