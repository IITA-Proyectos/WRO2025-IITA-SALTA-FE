from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.robotics import Car

from Funciones import get_section, get_round_direction

# Inicialización del hub
hub = PrimeHub()

# Motores
back_motor = Motor(Port.A)  # Tracción
front_motor = Motor(Port.B)  # Dirección

# Sensor de Color
color_sensor = ColorSensor(Port.D)

# Sensor de Distancia
ds_left = UltrasonicSensor(Port.C)
ds_right = UltrasonicSensor(Port.F)

# Robot tipo auto
car = Car(steer_motor=front_motor, drive_motors=[back_motor])
car.steer(0)

# Máquina de Estados

status = 'straight_sequence'

# Configuración del Sensor de Color
Color.NARANJA  = Color(h=24, s=100, v=100)
Color.VIOLETA  = Color(h=228, s=100, v=100)
Color.BLANCO   = Color(h=60, s=0, v=100)
Color.CELESTE  = Color(h=0, s=0, v=100)

color_sensor.detectable_colors((Color.NARANJA, Color.VIOLETA, Color.CELESTE, Color.NONE))

# Global Variables
direction      = "unknown"
direction_edit = True

total_lap  = 3
actual_lap = 0

# PID config
Kp = 0.8
Ki = 0.001
Kd = 0.35

integral = 0
last_error = 0

# Ángulo objetivo constante (recto)
target_angle = 0

# Angulo giro

angle_section_1 = 40

# Funciones y Procedimientos
def pid_control():
    global integral, last_error
    actual_angle = hub.imu.heading()

    # Error entre -180 y 180
    error = target_angle - actual_angle
    if error > 180:
        error -= 360
    elif error < -180:
        error += 360

    integral += error
    derivative = error - last_error
    last_error = error

    output = Kp * error + Ki * integral + Kd * derivative
    output = max(min(output, 100), -100)
    print("Error:", error, ",", output)
    return output

def get_round_direction(colorActualizado):
    global direction, direction_edit
    if current_color == Color.NARANJA:
        direction = "clockwise"
        direction_edit = False
    elif current_color == Color.VIOLETA:
        direction = "counterclockwise"
        direction_edit = False

initial_section= get_section("COUNTERCLOCKWISE", ds_right.distance()/10, ds_left.distance()/10)
wait(2000)
hub.imu.reset_heading(0)  # Rumbo inicial en 0°

while True:
    current_color = color_sensor.color()
    if direction_edit:
        get_round_direction(current_color)
    
    if status == "straight_sequence": #Secuencia ir derecho
        steer = pid_control()
        car.drive_power(20)
        car.steer(steer)
        wait(30)

        if current_color == Color.VIOLETA:
            status = "turn_sequence" #Secuencia de giro
            target_angle -= 90

    if status == "turn_sequence": #secuencia de giro
        # steer = calcular_giro_adaptativo(ds_left.distance(), ds_right.distance())

        if direction == 'counterclockwise':
            car.drive_power(20)
            car.steer(angle_section_1)
            if hub.imu.heading() <= (target_angle+4):
                status = "straight_sequence"


    print("Estado actual:", status)
    print("Target_Angle:", target_angle)
    print("Color actual:", current_color)
    print("Angulo Actual:", hub.imu.heading())
    print("Direccion:", direction)
    print("Sección:", initial_section)
    print("Angulo objetivo:", target_angle)
    print("------------------------------")



# while True:
#     get_section("CLOCKWISE", ds_left.distance()/10, ds_right.distance()/10)
#     wait(1000)
#     print("Left:", ds_left.distance()/10, "RIGHT:", ds_right.distance()/10)