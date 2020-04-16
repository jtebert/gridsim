import gridsim as gs

from random_robot import RandomRobot


def main():
    grid_width = 50  # Number of cells for the width & height of the world
    num_robots = 5
    num_steps = 100  # simulation steps to run

    # Create a few robots to place in your world
    robots = []
    for n in range(num_robots):
        robots.append(RandomRobot(grid_width-2*n,
                                  grid_width-2*n))

    # Create a 50 x 50 World with the Robots
    world = gs.World(grid_width, grid_width, robots=robots)

    # Run the simulation
    for n in range(num_steps):
        # Execute a simulation step
        world.step()
        # To make sure it works, print the tick (world time)
        print('Time:', world.get_time())

    print('SIMULATION FINISHED')


if __name__ == '__main__':
    # Run the simulation if this program is called directly
    main()
