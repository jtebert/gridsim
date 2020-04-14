"""
An experiment as a test
"""

# from .context import gridsim as gs

import gridsim as gs
from test_robot import TestRobot
from hub_robot import HubRobot


def main():
    x = 50
    num_robots = 2
    robots = []
    for n in range(num_robots):
        robots.append(TestRobot(x-1-n, x/2-n))
    hub_robot = HubRobot(x/2, x/2)

    world = gs.World(x, x, robots=robots)
    viewer = gs.Viewer(world, display_rate=5, show_grid=True)
    world.add_robot(hub_robot)

    num_steps = 100
    for n in range(num_steps):
        world.step()
        viewer.draw()

    print('SIMULATION FINISHED')


if __name__ == "__main__":
    main()
