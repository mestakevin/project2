# Heat release simulation
import numpy as np
import matplotlib.pyplot as plt
from .simulation import run_simulation  # Import the function from Simulation.py

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
        particles,temp_change,total_time = run_simulation(num_neutrons, num_uranium, box_dim, dt) 
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
    uranium_range = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])
    box_sizes = np.array([0.000001])

    # Initialize a 2D array to store temperature changes
    temp_changes = np.zeros((len(box_sizes), len(uranium_range)))

    # Run the simulation for each combination of box size and number of uranium atoms
    for i, box_dim in enumerate(box_sizes):
        for j, num_uranium in enumerate(uranium_range):
            # Run the simulation to get the temperature change
            particles,temp_change,total_time = run_simulation(num_neutrons, num_uranium, box_dim, dt)
            temp_changes[i, j] = temp_change

    # Create the heatmap
    plt.figure()
    plt.imshow(temp_changes, aspect='auto', origin='lower', cmap='viridis')
    plt.colorbar(label="Temperature Change ('C)")

    # Label the axes
    plt.xlabel("Number of Uranium Atoms")
    plt.ylabel("Box Size (m)")
    plt.title("Heatmap of Temperature Change vs. Uranium Atoms and Box Size")

    # Set custom Y-ticks to show the exact box sizes
    plt.yticks(ticks=np.arange(len(box_sizes)), labels=[f"{bs:.7f}" for bs in box_sizes])

    # Show the plot
    plt.show()


def heattime_vs_simulations():
    # Simulation parameters (common to all runs)
    num_neutrons = 4
    num_uraniums = 2  
    box_dim = 0.5      # Box dimension in meters
    dt = 1e-3        
    initial_water_temp = 25.0  # Celsius, assumed room temperature

    simulation_range = (100,200,400,600,800,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000) 
    average_temp_change = []
    stdev_temp_change = [] 
    average_time = []
    stdev_avg_time = []

    for simulation in simulation_range:
        print("CURRENT NUM OF SIMULATIONS:",simulation)
        simulation_num = 1
        sim_temp_change_list = []
        sim_total_time_list = []

        while simulation_num <= simulation:
            particles, temp_change,total_time = run_simulation(num_neutrons, num_uraniums, box_dim, dt) 
            print(total_time)
            sim_temp_change_list.append(temp_change)
            sim_total_time_list.append(total_time)
            simulation_num += 1
    
        average_temp_change.append(np.average(sim_temp_change_list))
        stdev_temp_change.append(np.std(sim_temp_change_list))
        average_time.append(np.average(sim_total_time_list))
        stdev_avg_time.append(np.std(sim_total_time_list))

    
    #average temp vs. simulations
    plt.figure()
    plt.plot(simulation_range, average_temp_change, label="Average Temp Change", color="blue", marker='o')
    
    # Label the axes
    plt.xlabel("Number of Simulations")
    plt.ylabel("Average Temp Change")
    plt.title("Average Temp Change vs. Number of Simulations")
    plt.legend()
    
    # Show the plot
    plt.grid(True)
    plt.show()

    #stdev of average temp vs. simulations
    plt.figure()
    plt.plot(simulation_range, stdev_temp_change, label="Standard Deviation Temp Change", color="blue", marker='o')
    
    # Label the axes
    plt.xlabel("Number of Simulations")
    plt.ylabel("Standard Deviation of Temp Change")
    plt.title("Standard Deviation of Temp Change vs. Number of Simulations")
    plt.legend()
    
    # Show the plot
    plt.grid(True)
    plt.show()

    #average simulation time vs. num simulations
    plt.figure()
    plt.plot(simulation_range, average_time, label="Average Simulation Time", color="blue", marker='o')
    
    # Label the axes
    plt.xlabel("Number of Simulations")
    plt.ylabel("Average Simulation Time")
    plt.title("Average Simulation Time vs. Number of Simulations")
    plt.legend()
    
    # Show the plot
    plt.grid(True)
    plt.show()

    #stdev of simulation time vs num simulations
    plt.figure()
    plt.plot(simulation_range, stdev_avg_time, label="Standard Deviation Simulation Time", color="blue", marker='o')
    
    # Label the axes
    plt.xlabel("Number of Simulations")
    plt.ylabel("Standard Deviation of Simulation Time")
    plt.title("Standard Deviation of Simulation Time vs. Number of Simulations")
    plt.legend()
    
    # Show the plot
    plt.grid(True)
    plt.show()