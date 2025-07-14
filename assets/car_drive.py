from pybricks.parameters import Port, Direction
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.robotics import Car
from pybricks.tools import wait
from pybricks.hubs import PrimeHub
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop

# Definición de motores
back_motor = Motor(Port.A)  # Motor de tracción
front_motor = Motor(Port.B)  # Motor de dirección

hub = PrimeHub()
hub.imu.reset_heading(0)

direction_edit = True
direction    = "unknown"

color_sensor = ColorSensor(Port.D)

Color.ORANGE = Color(h=24, s=100, v=100)
Color.BLUE   = Color(h=228, s=100, v=100)
Color.WHITE   = Color(h=60, s=0, v=100)
Color.LIGHTBLUE  = Color(h=0, s=0, v=100)

color_sensor.detectable_colors((Color.ORANGE, Color.BLUE, Color.LIGHTBLUE, Color.NONE))

car = Car(steer_motor=front_motor, drive_motors=[back_motor])
car.steer(0)

def get_round_direction():
    global direction, direction_edit
    if current_color == Color.ORANGE:
        direction = "clockwise"
        direction_edit = False
    elif current_color == Color.BLUE:
        direction = "counterclockwise"
        direction_edit = False

while True:
    current_color = color_sensor.color()
    actual_angle = hub.imu.heading()

    if direction_edit:
        get_round_direction()

    print(actual_angle)

    car.drive_power(20)
    if current_color == Color.BLUE:
        car.steer(37)
    if current_color == Color.ORANGE:
        car.steer(10)
        car.steer(-20)

