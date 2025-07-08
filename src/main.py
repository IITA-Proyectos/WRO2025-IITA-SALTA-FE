from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()
hub.imu.reset_heading(0)

# MOTORS
back_motor = Motor(Port.A)

# VARIABLES
target_angle = 90
direction = "unknown"
actual_angle = 0

direction_edit = True

# ColorSensorConfig
color_sensor = ColorSensor(Port.D)

orange_custom = Color(h=24, s=100, v=100)
blue_custom   = Color(h=228, s=100, v=100)
cyan_custom   = Color(h=0, s=0, v=70)

color_sensor.detectable_colors((orange_custom, blue_custom, cyan_custom, Color.NONE))

# MAIN LOOP
while True:
    current_color = color_sensor.color()
    
    if direction_edit:
        if current_color == orange_custom:
            direction = "clockwise"
            direction_edit = False
        elif current_color == blue_custom:
            direction = "counterclockwise"
            direction_edit = False
    print(direction)
        
