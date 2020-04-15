"""
An experiment as a test
"""

# from .context import gridsim as gs

from typing import List

import numpy as np

import gridsim as gs
from test_robot import TestRobot
from hub_robot import HubRobot


def green_agg(robots: List[gs.Robot]) -> np.ndarray:
    test_robots = list(filter(lambda r: isinstance(r, TestRobot), robots))
    out_arr = np.zeros([len(test_robots)])

    for i, r in enumerate(test_robots):
        out_arr[i] = r._color[1]

    return out_arr


def main():
    x = 50
    num_robots = 2
    robots = []
    for n in range(num_robots):
        robots.append(TestRobot(x - 1 - n, x / 2-n))
    hub_robot = HubRobot(x / 2, x / 2)

    world = gs.World(x, x, robots=robots)
    viewer = gs.Viewer(world, display_rate=5, show_grid=True)

    # Test adding a Robot after initializing the Viewer
    world.add_robot(hub_robot)

    # Logger
    logger = gs.Logger(world, 'test.h5', trial_num=1, overwrite_trials=True)
    logger.add_aggregator('green', green_agg)

    num_steps = 100
    for n in range(num_steps):
        world.step()
        viewer.draw()
        logger.log_state()

    print('SIMULATION FINISHED')


if __name__ == "__main__":
    main()
