import gridsim as gs
from typing import List
import numpy as np
from datetime import datetime

from random_robot import RandomRobot


def green_agg(robots: List[gs.Robot]) -> np.ndarray:
    """
    This is a dummy aggregator function (for demonstration) that just saves
    the value of each robot's green color channel
    """
    out_arr = np.zeros([len(robots)])
    for i, r in enumerate(robots):
        out_arr[i] = r._color[1]

    return out_arr


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

    # Logger
    trial_num = config.get('trial_num', default=1)
    # Create a logger for this world that saves to the `test.h5` file
    logger = gs.Logger(world, 'test.h5', trial_num=trial_num,
                       overwrite_trials=True)
    # Tell the logger to run the `green_agg` function every time that
    # `log_state` is called
    logger.add_aggregator('green', green_agg)
    # Save the contents of the configuration, but leave out the 'name' parameter
    logger.log_config(config, exclude='name')
    # Save the date/time that the simulation was run
    logger.log_param('date', str(datetime.now()))

    # Run the simulation
    for n in range(num_steps):
        # Execute a simulation step
        world.step()

        # Log the state every step
        logger.log_state()

        # To make sure it works, print the tick (world time)
        print('Time:', world.get_time())

    print('SIMULATION FINISHED')


if __name__ == '__main__':
    # Run the simulation if this program is called directly
    main()
