import random

from gridsim.grid_robot import GridRobot
import gridsim as gs


class RandomRobot(GridRobot):
    # Change direction every 10 ticks
    DIR_DURATION = 10

    def init(self):
        self.set_color(255, 0, 0)
        self._msg_sent = False

        # Next tick when Robot will change direction
        self._next_dir_change = self.get_tick()

    def receive_msg(self, msg: gs.Message, dist: float):
        # This robot got a message from another robot
        self._msg_sent = True

    def loop(self):

        # Change direction every DIR_DURATION ticks
        tick = self.get_tick()
        if tick >= self._next_dir_change:
            new_dir = random.choice(GridRobot.DIRS)
            self.set_direction(new_dir)
            self._next_dir_change = tick + RandomRobot.DIR_DURATION

        # Broadcast a test message to any robots nearby
        msg = gs.Message(self.id, {'test': 'hello'})
        self.set_tx_message(msg)

        # Change color depending on whether messages have been sent or received
        # Robot will be white when it has successfully sent & received a message
        green = 255 * self._msg_sent
        self.set_color(255, green, 0)
