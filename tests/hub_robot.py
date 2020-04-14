from gridsim import Robot, Message


class HubRobot(Robot):
    def init(self):
        # print('"TestRobot._init" not implemented yet')
        self.set_color(0, 255, 0)

    def comm_criteria(self, dist: int) -> bool:
        # print('"TestRobot.comm_criteria" not implemented yet')
        return dist < 5

    def receive_msg(self, msg: Message, dist: float):
        # print('"HubRobot.receive_msg" not implemented yet')
        print('HUB:', dist)
        pass

    def msg_received(self):
        pass

    def loop(self):
        # print('"TestRobot.loop" not implemented yet')
        pass
