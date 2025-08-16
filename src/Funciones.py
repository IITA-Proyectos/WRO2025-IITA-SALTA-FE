from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

def get_round_direction():
    global direction, direction_edit
    if current_color == Color.ORANGE:
        direction = "clockwise"
        direction_edit = False
    elif current_color == Color.BLUE:
        direction = "counterclockwise"
        direction_edit = False

def get_section(orientation, left_measure, right_measure):
    if orientation == 'COUNTERCLOCKWISE':
        if left_measure > 1 and left_measure < 37:
            return "SECTION_1"
        if left_measure > 37 and left_measure < 51.6:
            return "SECTION_2"
        if left_measure > 51.6 and left_measure < 90:
            return "SECTION_3"
    elif orientation == 'CLOCKWISE': # REVISAR SECCIONES
        if right_measure > 1 and right_measure < 37:
            return "SECTION_3"
        if right_measure > 37 and right_measure < 51.6:
            return "SECTION_2"
        if right_measure > 51.6 and right_measure < 90:
            return "SECTION_1"
    
