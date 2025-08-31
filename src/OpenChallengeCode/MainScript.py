from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

from robot_funcional93 import Robot

# ------------------- CONFIGURACIÓN INICIAL -----------------------
robotito = Robot()

robotito.angulo_resetear()
robotito.direccion_centrar()

direccion = 0                 # heading deseado (grados)
robotito.control_direccion = -1  # -1 izquierda / 1 derecha (por defecto)

# ----------------- PRIMER AVANCE: DEFINIR LA DIRECCIÓN ------------------
robotito.contador_resetear()
while not robotito.timeout(10_000):
    color_detectado = robotito.get_color()  # detectar color de la primera línea
    robotito.direccion_controlar(direccion, kp=1.2, velocidad_traccion=1000)

    if color_detectado in ("Violeta", "Naranja"):
        robotito.motor_traccion.hold()
        robotito.control_direccion = 1 if color_detectado == "Naranja" else -1
        break

robotito.pip()

# Avance hasta despegarse de la pared (distancia > 900 mm)
while robotito.ultrasonido_elegido() < 900:
    robotito.direccion_controlar(direccion, kp=1.2, velocidad_traccion=2000)

robotito.pip()

# ------------- BUCLE DE VUELTAS (90° cada vez) --------------
while True:
    # Girar “virtualmente” 90° en el sentido que corresponda
    print(robotito.control_direccion)
    direccion += -90 if robotito.control_direccion == -1 else 90

    # Avance inicial para alinearse con la próxima pared
    robotito.contador_resetear()
    contador_grados_inicio = robotito.motor_traccion.angle()
    # Avanza ~1500 ticks de motor de tracción
    while robotito.motor_traccion.angle() <= contador_grados_inicio + 1500:
        robotito.direccion_controlar(direccion, kp=1.1, velocidad_traccion=2000)
    robotito.pip()

    # Avanza hasta acercarse a la pared (distancia < 900 mm)
    while robotito.ultrasonido_elegido() < 900:
        robotito.direccion_controlar(direccion, kp=1.2, velocidad_traccion=2000)

    robotito.pip()

    # Salida: tras ~4 giros (± 360°); margen por acumulación
    if abs(direccion) > 989:
        robotito.pip()
        break

robotito.motor_traccion.hold()

#----------------- AVANCE FINAL PARA TERMINAR EN LA SECCIÓN INICIAL ------------------
direccion += -90 if robotito.control_direccion == -1 else 90

contador_grados_inicio = robotito.motor_traccion.angle()
while robotito.motor_traccion.angle() <= contador_grados_inicio + 1500:
    robotito.direccion_controlar(direccion, kp=0.65, velocidad_traccion=2000)

robotito.motor_traccion.hold()
