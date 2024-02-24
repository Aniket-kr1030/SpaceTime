# main.py

from simulation import Simulation

def main():
    width, height = 1000 , 800
    num_particles = 1
    simulation = Simulation(width, height, num_particles)
    simulation.run()

if __name__ == "__main__":
    main()
