
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pupremote import PUPRemoteHub

pr = PUPRemoteHub(Port.E)
pr.add_channel('cam', to_hub_fmt='hhh')
hub = PrimeHub()

class Robot():
    def __init__(self):
        self.spike = PrimeHub()
        self.spike.imu.ready()
        self.spike.imu.reset_heading(0)
        self.motor_direccion = Motor(Port.B, positive_direction=Direction.COUNTERCLOCKWISE)
        self.motor_traccion = Motor(Port.A, positive_direction=Direction.CLOCKWISE)
        
        self.timer1 = StopWatch()
        self.timerAvance = StopWatch()

        self.sensorcolor = ColorSensor(Port.D)
        self.sensorizquierda = UltrasonicSensor(Port.F)
        self.sensorderecha = UltrasonicSensor(Port.C)

        # --- Reloj / utilidades ---
        self.contador = StopWatch()

        # VARIABLES
        self.sentido_giro = 1  # 1 derecha -1 izquierda , inicia derecha por las dudas

        # --- Colores detectables (calibrados) ---
        Color.NARANJA = Color(h=5, s=64, v=96)
        Color.VIOLETA = Color(h=227, s=58, v=65)
        Color.BLANCO = Color(h=49, s=1, v=99)
        Color.CELESTE  = Color(h=40, s=1, v=99)

        self.sensorcolor.detectable_colors(
            (Color.NARANJA, Color.VIOLETA, Color.BLANCO, Color.CELESTE, Color.NONE)
        )

    def distancia_pared_adentro(self):
        if self.sentido_giro == 1:
            return self.sensorderecha.distance()
        elif self.sentido_giro == -1:
            return self.sensorizquierda.distance()

    def distancia_pared_afuera(self):
        if self.sentido_giro == -1:
            return self.sensorderecha.distance()
        elif self.sentido_giro == 1:
            return self.sensorizquierda.distance()

    # ----------------- Color -----------------
    def get_color(self):
        color_det = self.sensorcolor.color()
        # print(color_det)  # debug si quieres
        if color_det == Color.NARANJA:
            return "Naranja"
        elif color_det == Color.VIOLETA:
            return "Violeta"
        else:
            return "Blanco"

    def pip(self, freq):
        hub.speaker.beep(freq)

    def angulo_resetear(self):
        self.spike.imu.reset_heading(0)

    def angulo_obtener(self):
        angulo = self.spike.imu.heading()
        return angulo

    def direccion_centrar(self):
        self.timer1.reset()
        while not self.motor_direccion.stalled() or self.timer1.time() > 2500:  # Defino limite izquierda
            print(self.timer1.time())
            self.motor_direccion.run(-150)
        self.motor_direccion.hold()
        self.pip(5000)
        maximo_izquierda = self.motor_direccion.angle()

        self.timer1.reset()
        while not self.motor_direccion.stalled() or self.timer1.time() < 2500:  # Defino limite derecha
            print(self.timer1.time())
            self.motor_direccion.run(150)
        self.motor_direccion.hold()
        self.pip(5000)
        maximo_derecha = self.motor_direccion.angle()

        centro_absoluto = (maximo_derecha + maximo_izquierda) / 2
        print(maximo_izquierda, maximo_derecha, centro_absoluto)
        self.motor_direccion.run_target(150, centro_absoluto, then=Stop.HOLD, wait=True)
        self.pip(5000)

        self.limite_derecha = maximo_derecha - centro_absoluto
        self.limite_izquierda = maximo_izquierda - centro_absoluto

        print(self.limite_derecha, self.limite_izquierda)

        self.motor_direccion.reset_angle(0)

    def direccion_controlar(self, angulo_deseado, kp, velocidad, id_blob_detectado):
        angulo_actual = self.angulo_obtener()
        error = angulo_deseado - angulo_actual
        correccion = error * kp
        if correccion != 0:
            self.motor_direccion.run_target(200, correccion, then=Stop.BRAKE, wait=False)
        else:
            self.motor_direccion.brake()
        
        # id_blob_elegido, x_blob_elegido, y_blob_elegido = pr.call('cam')

        # if id_blob_detectado in [0, 1]:
        #     print("Detectado en direccion controlar")

        #     if id_blob_detectado == 0:
        #         self.pip()
        #         self.pip()
        #     elif id_blob_detectado == 1:
        #         self.pip()
        #         self.pip()
        #         self.pip()
                # ticks_iniciales = self.motor_traccion.angle()
                # while ticks_iniciales - self.motor_traccion.angle()< 100:
                #     self.direccion_controlar(angulo_deseado + 45, 1.1, 200)
  
                # ticks_iniciales = self.motor_traccion.angle()
                # while ticks_iniciales - self.motor_traccion.angle()< 100:
                #     self.direccion_controlar(angulo_deseado, 1.1, 200)

                # ticks_iniciales = self.motor_traccion.angle()
                # while ticks_iniciales - self.motor_traccion.angle()< 100:
                #     self.direccion_controlar(angulo_deseado - 45, 1.1, 200)
            
            # print("Detectado en direccion")
            # self.motor_traccion.run(0)
            # wait(2000)

        self.motor_traccion.run(velocidad)
    
    def avance_derecho(self, angulo_deseado, kpangulo, velocidad, distancia_deseada, kpdistance, direction, id_blob_detectado, id_x):
        self.timerAvance.reset()
        # print("avance derecho")
        # Obtener el ángulo actual del robot
        angulo_actual = self.angulo_obtener()
        
        # Calcular el error de orientación
        error_angulo = angulo_deseado - angulo_actual
        correccion_angulo = error_angulo * kpangulo
        
        # Obtener la distancia actual a la pared usando el sensor de ultrasonido
        distancia_actual = self.distancia_pared_afuera()
        if distancia_actual > 1000:
            kpdistance = 0
        
        # Calcular el error de distancia
        error_distancia = distancia_deseada - distancia_actual
        correccion_distancia = error_distancia * kpdistance
        if self.sentido_giro == -1:
            correccion_distancia = -correccion_distancia
        
        # Combinar las correcciones de ángulo y distancia
        
        correccion_total = correccion_angulo + correccion_distancia
        if correccion_total > self.limite_derecha:
            correccion_total = 80
        if correccion_total  < self.limite_izquierda:
            correccion_total = -80
        # print(correccion_total,  correccion_angulo, correccion_distancia)
        
        # Aplicar la corrección al motor de dirección
        if correccion_total != 0:
            self.motor_direccion.run_target(200, correccion_total, then=Stop.BRAKE, wait=False)
        
        # Mover el robot hacia adelante

        if id_blob_detectado in [0, 1]:
            print("Detectado en avance derecho")

            self.motor_traccion.run(0)
            wait(1000)

            if id_blob_detectado == 0:
                print("X:", id_x)
                if id_x > 100:
                    self.pip(3000)

                    ticks_iniciales = self.motor_traccion.angle()
                    while abs(ticks_iniciales - self.motor_traccion.angle()) < 300:
                        self.motor_traccion.run(-500)
                    ticks_iniciales = self.motor_traccion.angle()
                    while abs(ticks_iniciales - self.motor_traccion.angle()) < 300:
                        self.direccion_controlar(direction + 65, 1.1, 200, id_blob_detectado=id_blob_detectado)

                    ticks_iniciales = self.motor_traccion.angle()
                    while abs(ticks_iniciales - self.motor_traccion.angle()) < 400:
                        self.direccion_controlar(direction, 1.1, 200, id_blob_detectado=id_blob_detectado)

                    ticks_iniciales = self.motor_traccion.angle()
                    while abs(ticks_iniciales - self.motor_traccion.angle()) < 300:
                        self.direccion_controlar(direction - 65, 1.1, 200, id_blob_detectado=id_blob_detectado)
                
                elif id_x < 100:
                    self.pip(3000)

                    ticks_iniciales = self.motor_traccion.angle()
                    while abs(ticks_iniciales - self.motor_traccion.angle()) < 250:
                        self.motor_traccion.run(-500)
                    ticks_iniciales = self.motor_traccion.angle()
                    while abs(ticks_iniciales - self.motor_traccion.angle()) < 200:
                        self.direccion_controlar(direction + 45, 1.1, 200, id_blob_detectado=id_blob_detectado)

                    ticks_iniciales = self.motor_traccion.angle()
                    while abs(ticks_iniciales - self.motor_traccion.angle()) < 300:
                        self.direccion_controlar(direction, 1.1, 200, id_blob_detectado=id_blob_detectado)

                    ticks_iniciales = self.motor_traccion.angle()
                    while abs(ticks_iniciales - self.motor_traccion.angle()) < 200:
                        self.direccion_controlar(direction - 45, 1.1, 200, id_blob_detectado=id_blob_detectado)



            elif id_blob_detectado == 1:
                print("X VERDE:", id_x)
                self.pip(1000)
                self.motor_traccion.run(0)
                wait(1000)

                ticks_iniciales = self.motor_traccion.angle()
                while abs(ticks_iniciales - self.motor_traccion.angle()) < 250:
                    self.motor_traccion.run(-500)

                ticks_iniciales = self.motor_traccion.angle()
                while abs(ticks_iniciales - self.motor_traccion.angle()) < 250:
                    self.direccion_controlar(direction - 55, 1.1, 200, id_blob_detectado=id_blob_detectado)

                ticks_iniciales = self.motor_traccion.angle()
                while abs(ticks_iniciales - self.motor_traccion.angle()) < 300:
                    self.direccion_controlar(direction, 1.1, 200, id_blob_detectado=id_blob_detectado)

                ticks_iniciales = self.motor_traccion.angle()
                while abs(ticks_iniciales - self.motor_traccion.angle()) < 250:
                    self.direccion_controlar(direction + 55, 1.1, 200, id_blob_detectado=id_blob_detectado)
                
            # print("Detectado en avance")
            # self.motor_traccion.run(0)
            # wait(2000)

        self.motor_traccion.run(velocidad)
        
        tiempoTranscurrido = self.timerAvance.time()
        if tiempoTranscurrido < 10:
            wait(5-tiempoTranscurrido)

    def avance_derecho_ang(self, angulo_apuntado, kpangulo, velocidad):
        # print("avance derecho")
        # Obtener el ángulo actual del robot
        angulo_actual = self.angulo_obtener()
        
        # Calcular el error de orientación
        error_angulo = angulo_apuntado - angulo_actual
        correccion_angulo = error_angulo * kpangulo
        
        # Combinar las correcciones de ángulo y distancia
        correccion_total = correccion_angulo
        if correccion_total > self.limite_derecha:
            correccion_total = 45
        if correccion_total  < self.limite_izquierda:
            correccion_total = -45
        # print(correccion_total,  correccion_angulo, correccion_distancia)
        
        # Aplicar la corrección al motor de dirección
        if correccion_total != 0:
            print("Corrección total:", correccion_total)
            self.motor_direccion.run_target(200, correccion_total, then=Stop.BRAKE, wait=False)
        else:
            self.motor_direccion.brake()
        
        # Mover el robot hacia adelante
        self.motor_traccion.run(velocidad)

    def giro_derecha(self, angulo_giro_d, kp, velocidad):
        angulo_actual = self.angulo_obtener()
        error = angulo_giro_d - angulo_actual
        correccion = error * kp
        if correccion != 0:
            self.motor_direccion.run_target(200, correccion, then=Stop.BRAKE, wait=False)
        else:
            self.motor_direccion.brake()
        self.motor_traccion.run(velocidad)

    def giro_izquierda(self, angulo_giro_i, kp, velocidad):
        angulo_actual = self.angulo_obtener()
        error = angulo_giro_i - angulo_actual
        correccion = error * kp
        print(correccion)
        if correccion != 0:
            self.motor_direccion.run_target(200, correccion, then=Stop.BRAKE, wait=False)
        else:
            self.motor_direccion.brake()
        self.motor_traccion.run(velocidad)
    
    def parar_robot(self):
        while True:
            robotito.avance_derecho(angulo_deseado=0, kpangulo=1.5, velocidad=0, distancia_deseada=300, kpdistance=0.7)
            print("Deteniendo el robot")
            # Detiene el motor de tracción
            self.motor_traccion.stop(Stop.BRAKE)
            # Detiene el motor de dirección (si está en movimiento)
            self.motor_direccion.stop(Stop.HOLD)
            wait(2000)
            break
    
    def esquivar_derecha(self):
        while True:
            self.avance_derecho_ang(0,1.5, 150)
            wait(750)
            self.giro_derecha(60, 1.5, 150)
            wait(1500)
            self.avance_derecho_ang( 0, 0.6, 150)
            wait(1500)
            break

    def esquivar_izquierda(self):
        while True:
            self.avance_derecho_ang( 0, 1.5, 150)
            wait(750)
            self.giro_izquierda( -90, 1.5, 150)
            wait(1500)
            self.avance_derecho_ang( 0, 0.6, 150)
            wait(1500)
            break
        
    def esquivar_izquierda2(self):
        while True:
            self.giro_izquierda( -65, 1.5, 150)
            wait(1000)
            self.avance_derecho_ang( 0, 0.6, 150)
            wait(800)
            self.giro_derecha( 65, 1.5, 150)
            wait(1000)
            break
    
    def esquivar_derecha2(self):
        while True:
            self.giro_derecha(65, 1.5, 150)
            wait(1000)
            self.avance_derecho_ang( 0, 0.6, 150)
            wait(1400)
            self.giro_izquierda(-65, 1.5, 150)
            wait(1000)
            break

    def timeout(self, tiempo_max):
        # True si superó el tiempo en ms
        return self.contador.time() > tiempo_max

    def ultrasonido_elegido(self):
        """Devuelve la distancia del sensor del lado elegido (-1 izq, 1 der)."""
        if self.control_direccion == 1:
            return self.sensorderecha.distance()
        elif self.control_direccion == -1:
            return self.sensorizquierda.distance()
        else:
            # Si no está definido, por seguridad devolvemos un número alto
            return 10_000
    
# ------------------- CONFIGURACIÓN INICIAL -----------------------

robotito = Robot()

robotito.angulo_resetear()

robotito.direccion_centrar()

direccion = 0

robotito.sentido_giro = 1

# ----------------- PRIMER AVANCE PARA DEFINIR LA DIRECCION ------------------

robotito.timer1.reset()

while True:
    id_blob_elegido, x_blob_elegido, y_blob_elegido = pr.call('cam')
    ''' Avance en zona de inicio para determinar dirección '''
    color_detectado = robotito.get_color()

    robotito.avance_derecho(angulo_deseado=0, kpangulo=1.5, velocidad=400, distancia_deseada=460, kpdistance=0.7, direction=direccion, id_blob_detectado=id_blob_elegido, id_x=x_blob_elegido)
    
    if color_detectado in ("Violeta", "Naranja"):
        robotito.control_direccion = 1 if color_detectado == "Naranja" else -1
        break

while True:  
    # Girar 90° en el sentido que corresponda
    direccion += -90 if robotito.control_direccion == -1 else 90
    
    # Avance inicial para alinearse con la próxima pared
    robotito.contador.reset()
    contador_grados_inicio = robotito.motor_traccion.angle()

    # contracurva inicial para encarar por callejon central 300 ticks de motor de tracción
    if direccion == -90 or direccion == 90:
        while robotito.motor_traccion.angle() <= contador_grados_inicio + 20:
            id_blob_elegido, x_blob_elegido, y_blob_elegido = pr.call('cam')
            robotito.direccion_controlar(direccion - 180, kp=1.2, velocidad=400, id_blob_detectado=id_blob_elegido) #kp_original = 1.1
            print("otro ciclo ")
    else:
        while robotito.motor_traccion.angle() <= contador_grados_inicio + 105:
            id_blob_elegido, x_blob_elegido, y_blob_elegido = pr.call('cam')
            robotito.direccion_controlar(direccion - 180, kp=1.2, velocidad=400, id_blob_detectado=id_blob_elegido) #kp_original = 1.1
            print("otro ciclo")


    # Avanza ~1000 ticks de motor de tracción
    ''' Secuencia para los giros en las esquinas '''
    while robotito.motor_traccion.angle() <= contador_grados_inicio + 1600:
        id_blob_elegido, x_blob_elegido, y_blob_elegido = pr.call('cam')
        robotito.direccion_controlar(direccion, kp=1.3 , velocidad=400, id_blob_detectado=id_blob_elegido) #kp_original = 1.1
        print("ciclo 3")

    distancia_actual_promedio = 0
    # Avanza hasta acercarse a la pared (distancia < 950 mm)
    while distancia_actual_promedio < 950:
        id_blob_elegido, x_blob_elegido, y_blob_elegido = pr.call('cam')
        robotito.avance_derecho(angulo_deseado=direccion, kpangulo=1.5, velocidad=400, distancia_deseada=460, kpdistance=0.06, direction=direccion, id_blob_detectado=id_blob_elegido, id_x=x_blob_elegido)

        distancia_actual_promedio = (robotito.ultrasonido_elegido() +  distancia_actual_promedio) / 3
        print("otro ciclo")
 
    # Salida: tras ~4 giros (± 360°); margen por acumulación
    if abs(direccion) > 989:
        robotito.pip(5000)
        break


robotito.motor_traccion.hold()
   