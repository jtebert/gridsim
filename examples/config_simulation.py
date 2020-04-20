import gridsim as gs

from random_robot import RandomRobot


def main():
    config = gs.ConfigParser('simple_config.yml')
    print(config.get('name'))
    grid_width = config.get('grid_width')
    num_robots = config.get('num_robots')
    # You can specify a default value in case a parameter isn't in the
    # configuration file
    num_steps = config.get('num_steps', default=100)

    # Create a few robots to place in your world
    robots = []
    # Configuration values can also be lists, not just single values.
    x_pos = config.get('robot_x_pos')
    for n in range(num_robots):
        robots.append(RandomRobot(x_pos[n],
                                  grid_width/2 - n*2))

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
