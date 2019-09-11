import cProfile

def run(proc):
    p = cProfile.Profile()
    p.enable()
    proc()
    p.print_stats()
