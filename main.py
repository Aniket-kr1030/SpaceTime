# main.py

from simulation import Simulation

def main():
    width, height = 800, 600
    num_particles = 2
    simulation = Simulation(width, height, num_particles)
    simulation.run()

if __name__ == "__main__":
    main()
