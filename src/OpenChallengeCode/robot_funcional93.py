# robot_modules.py
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Color, Direction, Port, Stop
from pybricks.tools import StopWatch


class Robot:
    def __init__(self):
        # --- Hub e IMU ---
        self.spike = PrimeHub()
        self.spike.imu.ready()
        self.spike.imu.reset_heading(0)

        # --- Motores ---
        self.motor_direccion = Motor(
            Port.B,
            positive_direction=Direction.COUNTERCLOCKWISE,
            gears=None,
            reset_angle=True,
            profile=None,
        )
        self.motor_traccion = Motor(
            Port.A,
            positive_direction=Direction.CLOCKWISE,
            gears=None,
            reset_angle=True,
            profile=None,
        )

        # --- Sensores ---
        self.sensorcolor = ColorSensor(Port.D)
        self.sensorizquierda = UltrasonicSensor(Port.F)
        self.sensorderecha = UltrasonicSensor(Port.C)

        # --- Reloj / utilidades ---
        self.contador = StopWatch()

        # --- Estado ---
        self.control_direccion = None  # -1 izquierda, 1 derecha

        # --- Colores detectables (calibrados) ---
        # Ajusta estos HSV a tu lona / iluminación real
        Color.NARANJA = Color(h=5, s=64, v=96)
        Color.VIOLETA = Color(h=227, s=58, v=65)
        Color.BLANCO = Color(h=49, s=1, v=99)
        Color.CELESTE  = Color(h=40, s=1, v=99)

        self.sensorcolor.detectable_colors(
            (Color.NARANJA, Color.VIOLETA, Color.BLANCO, Color.CELESTE, Color.NONE)
        )

    # ----------------- Utilidades de tiempo / beeps -----------------
    def pip(self):
        self.spike.speaker.beep(frequency=400, duration=20)

    def contador_obtener(self):
        return self.contador.time()

    def contador_resetear(self):
        self.contador.reset()

    def timeout(self, tiempo_max):
        # True si superó el tiempo en ms
        return self.contador.time() > tiempo_max

    # ----------------- IMU / Ángulo -----------------
    def angulo_resetear(self):
        self.spike.imu.reset_heading(0)

    def angulo_obtener(self):
        return self.spike.imu.heading()

    # ----------------- Dirección / Steering -----------------
    def direccion_centrar(self, speed=150, limite_ms=2500):
        """Busca topes mecánicos izquierda/derecha y centra el ángulo del servo."""
        # Buscar tope izquierdo
        self.contador_resetear()
        while (not self.motor_direccion.stalled()) and (not self.timeout(limite_ms)):
            self.motor_direccion.run(-abs(speed))
        self.motor_direccion.hold()
        self.pip()
        maximo_izquierda = self.motor_direccion.angle()

        # Buscar tope derecho
        self.contador_resetear()
        while (not self.motor_direccion.stalled()) and (not self.timeout(limite_ms)):
            self.motor_direccion.run(abs(speed))
        self.motor_direccion.hold()
        self.pip()
        maximo_derecha = self.motor_direccion.angle()

        # Calcular centro
        centro_absoluto = (maximo_derecha + maximo_izquierda) / 2
        self.motor_direccion.run_target(abs(speed), centro_absoluto, then=Stop.HOLD, wait=True)
        self.pip()

        # Guardar límites relativos y poner 0 en el centro
        self.limite_derecha = maximo_derecha - centro_absoluto
        self.limite_izquierda = maximo_izquierda - centro_absoluto
        self.motor_direccion.reset_angle(0)

    def direccion_controlar(self, angulo_deseado, kp, velocidad_traccion, speed_servo=200):
        """Control simple P sobre heading para orientar dirección y avanzar."""
        angulo_actual = self.angulo_obtener()
        error = angulo_deseado - angulo_actual
        correccion = error * kp  # grados en el servo

        # Opcional: limitar corrección al rango mecánico conocido (si ya se midió)
        try:
            if correccion > self.limite_derecha:
                correccion = self.limite_derecha
            if correccion < self.limite_izquierda:
                correccion = self.limite_izquierda
        except AttributeError:
            # Si aún no se definieron límites, seguimos sin clamp
            pass

        if abs(correccion) > 0.01:
            self.motor_direccion.run_target(speed_servo, correccion, then=Stop.BRAKE, wait=False)
        else:
            self.motor_direccion.brake()

        self.motor_traccion.run(velocidad_traccion)

    # ----------------- Sensores de distancia -----------------
    def ultrasonido_elegido(self):
        """Devuelve la distancia del sensor del lado elegido (-1 izq, 1 der)."""
        if self.control_direccion == 1:
            return self.sensorderecha.distance()
        elif self.control_direccion == -1:
            return self.sensorizquierda.distance()
        else:
            # Si no está definido, por seguridad devolvemos un número alto
            return 10_000

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

    # ----------------- Secciones -----------------
    def get_section(self):
        if self.control_direccion == -1:
            selected_measure = self.sensorizquierda.distance()/10
        elif self.control_direccion == 1:
            selected_measure = self.sensorderecha.distance()/10
        
        if selected_measure > 1 and selected_measure < 37:
            return "SECTION_3"
        if selected_measure > 37 and selected_measure < 51.6:
            return "SECTION_2"
        if selected_measure > 51.6 and selected_measure < 90:
            return "SECTION_1"

    

