from karel_the_robot import World, Robot


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
karel = Robot(2, 2, 90, 1)
warel = Robot(1, 1, 0, 1)


world.add_robots(karel, warel)
world.start()

karel.put_beeper()
karel.move()

karel.turn_left()

karel.turn_off()
warel.move_x(3)
