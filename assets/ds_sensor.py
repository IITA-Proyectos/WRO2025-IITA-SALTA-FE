from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.robotics import Car

hub = PrimeHub()

ds_left = UltrasonicSensor(Port.F)
ds_right = UltrasonicSensor(Port.C)

def get_section(orientation, left_measure, right_measure):
    if orientation == 'COUNTERCLOCKWISE': #EN CONTRA DE LAS AGUJAS DEL RELOJ
        if left_measure > 1 and left_measure < 37:
            print("SECTION 1")
        if left_measure > 37 and left_measure < 51.6:
            print("SECTION 2")
        if left_measure > 51.6 and left_measure < 90:
            print("SECTION 3")
    elif orientation == 'CLOCKWISE': # REVISAR SECCIONES
        if right_measure > 1 and right_measure < 37:
            print("SECTION 3")
        if right_measure > 37 and right_measure < 51.6:
            print("SECTION 2")
        if right_measure > 51.6 and right_measure < 90:
            print("SECTION 1")

while True:
    get_section("CLOCKWISE", ds_left.distance()/10, ds_right.distance()/10)
    wait(1000)
    print("Left:", ds_left.distance()/10, "RIGHT:", ds_right.distance()/10)