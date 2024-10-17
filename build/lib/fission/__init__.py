
def main_program():
    import argparse
    from .test_module import test_function
    from .simulation import run_Simulation
    parser = argparse.ArgumentParser()
    parser.add_argument("--number", type=float)

    args = parser.parse_args()
    
    #test_function(args.number)
    run_Simulation()
