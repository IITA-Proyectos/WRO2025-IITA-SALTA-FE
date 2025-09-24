import sensor
import time
from pupremote import PUPRemoteSensor
pr = PUPRemoteSensor()
pr.add_channel('cam',to_hub_fmt='hhh')
umbrales = [
        (10, 60, 20, 60, 0, 40),
        (10, 50, -30, -5, -10, 20),
    ]
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
sensor.set_auto_exposure(False, exposure_us=9000)
sensor.skip_frames(time=2000)
clock = time.clock()
while True:
	blob_elegido = None
	x_blob_elegido = 0
	y_blob_elegido = 0
	id_blob_elegido = None
	clock.tick()
	img = sensor.snapshot()
	contador = 0
	while contador < len(umbrales):
		umbral_recorrido = umbrales[contador]
		blobs = img.find_blobs([umbral_recorrido], pixels_threshold=500, area_threshold=1500)
		for blob in blobs:
			(cx, cy, r) = blob.enclosing_circle()
			img.draw_circle(cx, cy, r, color=(242,22,139))
			img.draw_edges(blob.min_corners())
			if contador == 0:
				id_unica = 0
				color = (255, 0, 0)
			elif contador == 1:
				id_unica = 1
				color = (0, 255, 0)
			if blob_elegido == None or blob.cy() > blob_elegido.cy():
				blob_elegido = blob
				id_blob_elegido = id_unica
				x_blob_elegido = int(blob.cx())
				y_blob_elegido = int(blob.cy())
			img.draw_cross(blob.cx(), blob.cy(), color=color)
			img.draw_string(blob.x(), blob.y() - 10, str(id_unica))
		contador += 1
	if blob_elegido == None:
		id_blob_elegido, x_blob_elegido, y_blob_elegido = -1, -1, -1
	print(id_blob_elegido, x_blob_elegido, y_blob_elegido)
	pr.update_channel('cam', id_blob_elegido, x_blob_elegido, y_blob_elegido)
	pr.process()
	print(clock.fps())
