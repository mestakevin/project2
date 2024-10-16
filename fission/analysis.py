# Heat release simulation
import matplotlib.pyplot as plt
from simulation import run_simulation  # Import the function from Simulation.py

def heat_release_vs_uranium():
    # Simulation parameters (common to all runs)
    num_neutrons = 4  
    box_dim = 0.5      # Box dimension in meters
    dt = 1e-3        
    initial_water_temp = 25.0  # Celsius, assumed room temperature
    
    # Range of uranium atoms to simulate
    uranium_range = (1,50,100,300,700,1000)  
    temp_changes = []  

    for num_uranium in uranium_range:
        # Run the simulation to get the temperature change
        particles, all_positions, temp_change = run_simulation(num_neutrons, num_uranium, box_dim, dt) 
        temp_changes.append(temp_change)

    # Plot the heat released as a function of the number of uranium atoms
    plt.figure()
    plt.plot(uranium_range, temp_changes, label="Temp. Change", color="blue", marker='o')
    
    # Label the axes
    plt.xlabel("Number of Uranium Atoms")
    plt.ylabel("Temperature Change ('C)")
    plt.title("Temperature Change vs. Number of Uranium Atoms")
    plt.legend()
    
    # Show the plot
    plt.grid(True)
    plt.show()

# Run and visualize the simulation
if __name__ == "__main__":
    heat_release_vs_uranium()
