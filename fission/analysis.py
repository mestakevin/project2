# Heat release simulation
import numpy as np
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

def heat_release_heatmap():
    # Simulation parameters
    num_neutrons = 4
    dt = 1e-3
    initial_water_temp = 25.0  # Celsius, assumed room temperature

    # Range of uranium atoms and box sizes to simulate
    uranium_range = np.array([1, 50, 100, 300, 700, 1000])
    box_sizes = np.array([0.001, 0.005, 0.01, 0.02, 0.05, 0.1])  # Box sizes in meters

    # Initialize a 2D array to store temperature changes
    temp_changes = np.zeros((len(box_sizes), len(uranium_range)))

    # Run the simulation for each combination of box size and number of uranium atoms
    for i, box_dim in enumerate(box_sizes):
        for j, num_uranium in enumerate(uranium_range):
            # Run the simulation to get the temperature change
            particles, all_positions, temp_change = run_simulation(num_neutrons, num_uranium, box_dim, dt)
            temp_changes[i, j] = temp_change

    # Create the heatmap
    plt.figure()
    plt.imshow(temp_changes, extent=[uranium_range[0], uranium_range[-1], box_sizes[0], box_sizes[-1]], 
               aspect='auto', origin='lower', cmap='viridis')
    plt.colorbar(label="Temperature Change ('C)")

    # Label the axes
    plt.xlabel("Number of Uranium Atoms")
    plt.ylabel("Box Size (m)")
    plt.title("Heatmap of Temperature Change vs. Uranium Atoms and Box Size")

    # Show the plot
    plt.show()

def heat_release_vs_simulations():
    # Simulation parameters (common to all runs)
    num_neutrons = 4
    num_uraniums = 2  
    box_dim = 0.5      # Box dimension in meters
    dt = 1e-3        
    initial_water_temp = 25.0  # Celsius, assumed room temperature

    simulation_range = (5,10,15,20,25,50,100,200,400,600,800,1000,2000,3000,4000,5000) 
    average_temp_change = []
    stdev_temp_change = [] 

    for simulation in simulation_range:
        simulation_num = 1
        sim_temp_change_list = []

        while simulation_num <= simulation:
            
            particles, all_positions, temp_change = run_simulation(num_neutrons, num_uraniums, box_dim, dt) 
            sim_temp_change_list.append(temp_change)
            simulation_num += 1
    
        average_temp_change.append(np.average(sim_temp_change_list))
        stdev_temp_change.append(np.std(sim_temp_change_list))
    
    
    plt.figure()
    plt.plot(simulation_range, stdev_temp_change, label="Standard Deviation", color="blue", marker='o')
    
    # Label the axes
    plt.xlabel("Number of Simulations")
    plt.ylabel("Standard Deviation")
    plt.title("Standard Deviation vs. Number of Simulations")
    plt.legend()
    
    # Show the plot
    plt.grid(True)
    plt.show()


# Run and visualize the simulation
if __name__ == "__main__":
    #heat_release_vs_uranium()
    #heat_release_heatmap()
    heat_release_vs_simulations()
