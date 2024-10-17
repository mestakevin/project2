
def main_program():
    import argparse
    from .test_module import test_function
    from .simulation import run_Simulation
    parser = argparse.ArgumentParser()
    parser.add_argument("--number", type=float)

    args = parser.parse_args()
    
    #test_function(args.number)
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
