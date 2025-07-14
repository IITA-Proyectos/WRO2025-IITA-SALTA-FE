from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# Devices initialization
hub = PrimeHub()
hub.imu.reset_heading(0)

color_sensor = ColorSensor(Port.D)

# MOTORS
back_motor = Motor(Port.A)
front_motor = Motor(Port.B)
front_motor.reset_angle(0)

# Global Variables
target_angle = 90
direction    = "unknown"

total_lap  = 3
actual_lap = 0

direction_edit = True

# ColorSensorConfig

Color.ORANGE = Color(h=24, s=100, v=100)
Color.BLUE   = Color(h=228, s=100, v=100)
Color.WHITE   = Color(h=60, s=0, v=100)
Color.CYAN  = Color(h=0, s=0, v=100)

color_sensor.detectable_colors((Color.ORANGE, Color.BLUE, Color.CYAN, Color.NONE))

# Functions and Procedures

def get_round_direction():
    global direction, direction_edit
    if current_color == Color.ORANGE:
        direction = "clockwise"
        direction_edit = False
    elif current_color == Color.BLUE:
        direction = "counterclockwise"
        direction_edit = False


# Main loop
while True:
    current_color = color_sensor.color()
    actual_angle = hub.imu.heading()

    if direction_edit:
        get_round_direction()
    
    print(current_color)

    back_motor.run(60)
    
    if current_color == Color.BLUE:
        front_motor.run_target(200, 40)



# front_motor.run_target(200, -50)
# wait(1000)
# front_motor.run_target(200, 0)
# wait(3000)
# front_motor.run_target(200, 50)
# wait(1000)