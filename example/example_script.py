from src.karel_the_robot import World, Robot


#TODO: terminal, then run pdoc --html karel_the_robot.py

@Robot.add_method(Robot)
def turn(Robot, x):
    x = (4 - (x % 4)) % 4
    for i in range(0, x):
        Robot.turn_left()


@Robot.add_method(Robot)
def move_x(Robot, x):
    for i in range(0, x):
        Robot.move()


world = World.from_file("example_world.txt")
karel = Robot(15, 15, "East", 0)
world.add_robots(karel)
world.start()
