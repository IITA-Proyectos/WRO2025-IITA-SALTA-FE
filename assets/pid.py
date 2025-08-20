
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop

from pybricks.robotics import Car
from pybricks.tools import wait
from pybricks.hubs import PrimeHub

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
    return output

def get_round_direction(colorActualizado):
    global direction, direction_edit
    if current_color == Color.NARANJA:
        direction = "clockwise"
        direction_edit = False
    elif current_color == Color.VIOLETA:
        direction = "counterclockwise"
        direction_edit = False

def get_section(orientation, left_measure, right_measure):
    if orientation == 'COUNTERCLOCKWISE':
        if left_measure > 5 and right_measure < 60:
            print("SECTION 1")
    elif orientation == 'CLOCKWISE':
        pass

# def calcular_giro_adaptativo(dist_izq, dist_der, d_max=20, k=5):
#     # Determinar el lado interior de la curva
#     if dist_izq < dist_der:
#         d_sensor = dist_izq
#         sentido = -1  # curva hacia la izquierda
#     else:
#         d_sensor = dist_der
#         sentido = 1   # curva hacia la derecha

#     # Calcular cuánto hay que girar
#     error = max(0, d_max - d_sensor)
#     giro = k * error
#     giro = min(giro, 100)  # limitar a 100%

#     return sentido * giro

wait(2000)
hub.imu.reset_heading(0)  # Rumbo inicial en 0°

# Bucle principal
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
            status = "turn_sequence"
            target_angle += 90

    if status == "turn_sequence": #secuencia de giro
        #Si el send
        # steer = calcular_giro_adaptativo(ds_left.distance(), ds_right.distance())

        if direction == 'counterclockwise':
            car.drive_power(20)
            car.steer(abs(ds_right.distance()/10) * 0.5)

        # car.drive_power(20) #Vel. Cte
        # car.steer(steer) #Direccion variable segun distancia
        # wait (60)


#        car.steer(35)
#        car.drive_power(20)
#        wait(60)
    
    print("Estado actual:", status)
    print("Color actual:", current_color)
    print("Angulo Actual:", hub.imu.heading())
    print("Direccion:", direction)
    print("Angulo objetivo:", target_angle)
    print("------------------------------")