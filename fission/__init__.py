#__init__ file

def main_program():
    import argparse
    import test_module as test

    parser = argparse.ArgumentParser()
    parser.add_argument("--number",type=float)

    args = parser.parse_args()
    
    test.test_function(args.number)

