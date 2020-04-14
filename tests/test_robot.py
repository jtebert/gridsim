from gridsim import Robot


class TestRobot(Robot):
    def init(self):
        # print('"TestRobot._init" not implemented yet')
        self.set_color(255, 0, 0)

    def comm_criteria(self, dist: int) -> bool:
        # print('"TestRobot.comm_criteria" not implemented yet')
        return dist < 5

    def receive_msg(self):
        print('"TestRobot.receive_msg" not implemented yet')
        pass

    def loop(self):
        # print('"TestRobot.loop" not implemented yet')
        x, y = self.get_pos()
        if x == 0:
            self.move(1, 0)
        else:
            self.move(-1, 0)
