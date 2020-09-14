from karel_the_robot.src.karel_the_robot import World, Robot

# Create a new turn method for all Robots to use
@Robot.add_method(Robot)
def turn(Robot, x):
    x = (4 - (x % 4)) % 4
    for i in range(0, x):
        Robot.turn_left()


# Create a new move method for all Robots to use
@Robot.add_method(Robot)
def move_x(Robot, x):
    for i in range(0, x):
        Robot.move()


# Create a new World from the specified file
world = World.from_file("example_world.txt")

# Create a new Robot called karel at (4, 4), facing East with 0 Beepers
karel = Robot(4, 4, "East", 0)

# Add karel to the World
world.add_robots(karel)

# Start the World
world.start()

# Have karel use our new methods, along with base methods, to interact with the World
karel.turn(2)
karel.move_x(2)
karel.turn(-1)
karel.move_x(2)
karel.pick_beeper()
karel.pick_beeper()
karel.pick_beeper()
karel.pick_beeper()
karel.pick_beeper()
karel.pick_beeper()
karel.pick_beeper()
karel.pick_beeper()
karel.turn(2)
karel.move_x(3)
karel.turn(1)
karel.move_x(3)
karel.pick_beeper()
karel.turn(1)
karel.move_x(1)
karel.put_beeper()
karel.move_x(1)
karel.put_beeper()
karel.move_x(1)
karel.put_beeper()
karel.move_x(1)
karel.put_beeper()
karel.move_x(1)
karel.put_beeper()
karel.turn(-1)
karel.move_x(1)
karel.put_beeper()
karel.move_x(1)
karel.put_beeper()
karel.move_x(1)
karel.put_beeper()
karel.move_x(1)
karel.put_beeper()

# The World quits here automatically
