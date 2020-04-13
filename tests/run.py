"""
An experiment as a test
"""

# from .context import gridsim as gs

import gridsim as gs
from test_robot import TestRobot


def main():

    num_robots = 2
    robots = []
    for n in range(num_robots):
        robots.append(TestRobot(n, n))

    world = gs.World(20, 20, robots=robots)
    viewer = gs.Viewer(world)

    num_steps = 10
    for n in range(num_steps):
        world.step()
        viewer.draw()

    print('SIMULATION FINISHED')


if __name__ == "__main__":
    main()
