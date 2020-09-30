from gridsim import Robot, Message


class HubRobot(Robot):
    def init(self):
        # print('"TestRobot._init" not implemented yet')
        self.set_color(255, 0, 255)

    def comm_criteria(self, dist_sqr: int) -> bool:
        # print('"TestRobot.comm_criteria" not implemented yet')
        return dist_sqr < 5**2

    def receive_msg(self, msg: Message, dist_sqr: float):
        # print('"HubRobot.receive_msg" not implemented yet')
        print('HUB:', dist_sqr)
        pass

    def msg_received(self):
        pass

    def loop(self):
        # print('"TestRobot.loop" not implemented yet')
        pass
