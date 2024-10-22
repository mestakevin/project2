Fission Module README

Thank you for downloading and installing the "fission" package, please make sure that you also have the appropriate "pyproject.toml" file for version 2.0.1 before continuing below. 


The main focus of this package is to perform a Monte Carlo simulation of neutron particles and uranium, barium, and krypton atoms traveling within a sealed water tank as fission reactions of uranium occur. The trajectories of each of these particles was simulated according to a 2nd order ODE, due to the drag created from traveling through water, and probabilistic collisions occurred between all particles in the simulation. The simulation is initialized with a set number of neutrons and uranium atoms according to an exponential random distribution, a set time step to increment the particles through time, and the dimensions of the cubic container the simulation is run in. The simulation then runs until there are no more remaining uranium atoms and the change in water temperature and total time elapsed is displayed to the user. 

The package can be installed by typing the following in the command line: "pip(3) install fission" which downloads all the corresponding modules necessary for the fission module to run properly. In addition please be sure to have pip version 24.2 installed in your virtual environment prior to installation of fission.

Following installation, the following scripts can be ran from command line:

main_script
heat_vs_uranium
heatmap
heattime
uranium_time
neutron_time
heat_vs_dt

"main_script" performs the fission simulation according to user inputted parameters and returns the temperature change of water and the total time in seconds of the simulation. A sample input for this script looks like this:

##########################################################################################
Please enter how many neutrons to generate within the box
>2
Please enter how many uraniums to generate within the box
>4
Please enter a value for half the length of the box
>0.5
Please enter the time step for the simulation
>0.001
##########################################################################################

The values for neutrons and uranium atoms must be positive integers while the values for length and time step can be positive floats or integers (larger lengths may not result in measurable temperature changes and larger time steps may not cause collisions).

"heat_vs_uranium" performs 6 fission simulations varying the amount of uranium atoms (1,50,100,300,700,1000) with 4 neutrons in a box with a volume of 1m^3 and a time step of 0.001 seconds. A graph is then displayed showing how the temperature change of the water within the box varies as a function of initial uranium atoms. 

"heatmap" performs 25 fission simulations varying the amount of uranium atoms, starting at 25 and incrementing up to 25, with 4 neutrons in a box with a volume of 8 micrometers^3 and a time step of 0.001 seconds. A heat map is generated as a result that shows how the temperature change increases as more uranium atoms are initialized.

"heattime" performs 9 different size simulation batches to quantitatively observe the sampling error and how it decreases as larger sample sizes are taken. Each simulation batch size (10,25,50,75,100,200,300,400,500) is repeated 100 times, and is initialized with 4 neutrons, 2 uranium atoms, a box volume of 1m^3 and a time step of 0.001 seconds. 4 graphs are displayed to the user showing the average of the average temperature change , the standard deviation of the average temperature change, the average standard deviation of temperature change, and the standard deviation of the standard deviation of temperature change all as a function of simulation batch size.

"uranium_time" performs 15 different simulations varying the amount of uranium atoms (10,25,50,100,200,250,300,400,500,600,700,750,800,900,1000) with 4 neutrons in a box with a volume of 1m^3 and a time step of 0.001 seconds. Each simulation is repeated 5 times and the average computation time is plotted against the number of uranium atoms the simulation was initialized with.  

"neutron_time" performs 15 different simulations varying the amount of neutron particles (10,25,50,100,200,250,300,400,500,600,700,750,800,900,1000) with 2 uranium atoms in a box with a volume of 1m^3 and a time step of 0.001 seconds. Each simulation is repeated 5 times and the average computation time is plotted against the number of neutron particles the simulation was initialized with.  

"heat_vs_dt" performs 9 different simulations varying the size of the time step (0.00001, 0.000025, 0.00005, 0.000075, 0.00010, 0.00025, 0.00050, 0.00075, 0.00100,) with 2 uranium atoms and 4 neutron particles in a box with a volume of 1m^3. Each simulation is repeated 25 times and 4 graphs are displayed to the user, the average temperature change, the standard deviation of the average temperature change, the average computation time and the standard deviation of the computation time all as a function of time step size. 

