
from gridsim import Robot


class TestRobot(Robot):
    def init(self):
        print('"TestRobot._init" not implemented yet')
        pass

    def comm_criteria(self) -> bool:
        print('"TestRobot.comm_criteria" not implemented yet')
        return True

    def receive_msg(self):
        print('"TestRobot.receive_msg" not implemented yet')
        pass

    def controller(self):
        print('"TestRobot.controller" not implemented yet')
        pass
