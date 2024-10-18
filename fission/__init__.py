
def main_program():
    from .simulation import main
    main()

def heat_vs_uranium():
    from .analysis import heat_release_vs_uranium
    heat_release_vs_uranium()

def heatmap():
    from .analysis import heat_release_heatmap
    heat_release_heatmap()

def heattime_vs_simulations():
    from .analysis import heattime_vs_simulations
    heattime_vs_simulations()

def computation_vs_uraniums():
    from .analysis import computation_vs_uraniums
    computation_vs_uraniums()

def computation_vs_neutrons():    
    from .analysis import computation_vs_neutrons
    computation_vs_neutrons()