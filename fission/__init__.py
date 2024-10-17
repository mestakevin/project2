
def main_program():
    from .simulation import run_Simulation
    run_Simulation()

def heat_vs_uranium():
    from .analysis import heat_release_vs_uranium
    heat_release_vs_uranium()

def heatmap():
    from .analysis import heat_release_heatmap
    heat_release_heatmap()

def heat_vs_simulations():
    from .analysis import heat_release_vs_simulations
    heat_release_vs_simulations()
