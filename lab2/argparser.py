import argparse
def get_workload():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workload', choices=['matrix-multiply', 'bubblesort', 'binary-search'], required=True)
    args = parser.parse_args()
    workload = args.workload
    return workload
    
