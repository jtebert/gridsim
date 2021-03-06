from typing import List
import argparse
from random import randint

import numpy as np

import gridsim as gs
from random_robot import RandomRobot


def green_agg(robots: List[gs.Robot]) -> np.ndarray:
    """
    This is a dummy aggregator function (for demonstration) that just saves
    the value of each robot's green color channel

    Parameters
    ----------
    robots : List[gs.Robot]
        All robots from the World (sent by the Logger)

    Returns
    -------
    np.ndarray
        1D array of green color channel values for every Robot
    """
    # If you have multiple types of robots in your World, you can filter them
    # to only aggregate values for a single robot type. In this case, we only
    # have ``RandomRobot``s, so we don't need this

    # robots = list(filter(lambda r: isinstance(r, RandomRobot), robots))

    out_arr = np.zeros([len(robots)])
    for i, r in enumerate(robots):
        out_arr[i] = r._color[1]

    return out_arr


def main(config_file: str):
    # Import configuration
    config = gs.ConfigParser(config_file)
    print('STARTING', config.get('name'))

    # Number of cells in the width/height of the square grid
    grid_w = config.get('grid_width')

    num_robots = config.get('num_robots')
    # Use a default communication range if one is not in the configuration
    comm_range = config.get('comm_range', default=6)
    overwrite_trials = config.get('overwrite_trials', default=False)
    start_trial = config.get('start_trial', default=1)
    end_trial = config.get('end_trial')

    for trial in range(start_trial, end_trial+1):

        robots = []
        for n in range(num_robots):
            robots.append(RandomRobot(randint(0, grid_w-1),
                                      randint(0, grid_w-1),
                                      comm_range=comm_range))
        # Create the World, with the robots in it
        world = gs.World(grid_w, grid_w, robots=robots)
        # Add the image to the World
        world.add_environment(config.get('environment_img'))

        # Create the viewer
        viewer = gs.Viewer(world, display_rate=10,
                           show_grid=False, window_width=1000)

        # Logger
        log_filename = config.get('log_filename')
        logger = gs.Logger(world, log_filename, trial_num=trial,
                           overwrite_trials=overwrite_trials)
        logger.add_aggregator('green', green_agg)
        logger.log_config(config)

        num_steps = config.get('num_steps')
        # Run the simulation
        for n in range(num_steps):
            # Run a single step of the
            world.step()
            # Draw the updated world state
            viewer.draw()
            # Save the state of the World using the aggregators
            logger.log_state()
        print(f'TRIAL {trial} FINISHED')

    print('SIMULATION FINISHED')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the example simulations")
    parser.add_argument('config_file', type=str,
                        help='YAML configuration filename')
    args = parser.parse_args()
    main(args.config_file)
