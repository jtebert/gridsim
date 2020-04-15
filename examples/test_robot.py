# from gridsim import Robot, Message
import gridsim as gs
from hub_robot import HubRobot


class TestRobot(gs.Robot):
    def init(self):
        self.set_color(255, 0, 0)
        self._msg_success = False

    def comm_criteria(self, dist: int) -> bool:
        return dist < 5

    def receive_msg(self, msg: gs.Message, dist: float):
        print('"TestRobot.receive_msg" not implemented yet')
        pass

    def msg_received(self):
        self._msg_success = True

    def loop(self):
        x, y = self.get_pos()
        if x == 0:
            self.move(1, 0)
        else:
            self.move(-1, 0)

        msg = gs.Message(self.id, {'test': 'hello'}, rx_type=HubRobot)
        self.set_tx_message(msg)

        if self._msg_success:
            self.set_color(0, 255, 00)
        else:
            self.set_color(0, 0, 255)
