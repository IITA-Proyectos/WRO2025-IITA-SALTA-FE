from pybricks.parameters import Port
from pybricks.pupdevices import Motor
from pybricks.robotics import Car
from pybricks.tools import wait
from pybricks.hubs import PrimeHub

# Inicialización del hub
hub = PrimeHub()
hub.imu.reset_heading(0)  # Rumbo inicial en 0°

# Motores
back_motor = Motor(Port.A)  # Tracción
front_motor = Motor(Port.B)  # Dirección

# Robot tipo auto
car = Car(steer_motor=front_motor, drive_motors=[back_motor])
car.steer(0)

# PID config
Kp = 0.6
Ki = 0.0
Kd = 0.3

integral = 0
last_error = 0

# Ángulo objetivo constante (recto)
target_angle = 0

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

wait(3000)

# Bucle principal
while True:
    steer = pid_control()
    car.drive_power(30)
    car.steer(steer)
    wait(20)
