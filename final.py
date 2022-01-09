import time
from grove.gpio import GPIO
import smbus
import sys
import time
import RPi.GPIO as GPIO
from seeed_dht import DHT
import requests
import logging
import csv
import subprocess
import json
import requests

#Comprobamos que esta correctamente la conexión con el sistema
if sys.platform != 'linux':
    sys.exit(1)
i2c = smbus.SMBus(1)
#Definimos la información de la base de datos
url = 'https://corlysis.com:8086/write' 
#Url de escritura (también puede ser 8087)
#Parametros de la base de datos de corlisys
class variables:
    params = {"db": "g13", "u": "token", "p": "d706c5b07a9982b351ea7cace7ba5921"}
    humi = 0
    temp = 0
    t = 0
    sData = []
    pulso = 0     

class MMA7660FC:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.mma7660fcAddr = addr
        self.i2c.write_byte_data( self.mma7660fcAddr, 0x07, 0x01 )
        self.i2c.write_byte_data( self.mma7660fcAddr, 0x08, 0x07 )
        time.sleep(0.01)
    def acceleration_read(self):
        data = self.i2c.read_i2c_block_data(self.mma7660fcAddr, 0x68, 3)
        # Convert the data to 6-bits
        xAccl = data[0] & 0x3F
        if xAccl > 31 :
            xAccl -= 64
        yAccl = data[1] & 0x3F
        if yAccl > 31 :
            yAccl -= 64
        zAccl = data[2] & 0x3F
        if zAccl > 31 :
            zAccl -= 64
        variables.sData = [xAccl,yAccl,zAccl]
        print("Acceleration ({},{},{})".format(variables.sData[0],variables.sData[1],variables.sData[2]))
class grove_fingerclip_heart_sensor:
    address = 0x50
    def pulse_read(self):
        variables.pulso = i2c.read_byte(0x50)
        print("Pulso:", variables.pulso)
 
def main():
    # Aqui comprobamos si existe inclinacion del usuario
    channel = 16
    GPIO.setmode(GPIO.BCM)       
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #Posteamos los datos en la base de datos utilizando una petición http a través de la librería request
    def alert(ev=None):
        variables.t= 1
        print("Tilt Detected")

    def loop():
        GPIO.add_event_detect(channel, GPIO.FALLING, callback=alert, bouncetime=100) 
        variables.t= 0
        print("Nothing Detected")
                    
    loop()

def hum_temp_read():
    # Hacemos la lectura de humedad y temperatura
    sensor = DHT('11', 5)
    variables.humi, variables.temp = sensor.read()
    print('Temperature {}C, Humidity {}%'.format(variables.temp, variables.humi))

def datos():
    p = subprocess.Popen(['iostat','-c','-o','JSON'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out, err = p.communicate()
    data = json.loads(out)
    system = data['sysstat']['hosts'][0]['statistics'][0]['avg-cpu']['system']
    idle = data['sysstat']['hosts'][0]['statistics'][0]['avg-cpu']['idle']
    p = subprocess.Popen(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out, err = p.communicate()
    temp = out[5:9]
    print("Datos del sistema: %s CPU: %s Temperatura de la raspberry: %s" %(system,idle,temp))
 
if __name__=='__main__':
     #lectura de fichero csv
    myFile = open('log.csv', 'w')
    #mostramos los datos del pc
    datos()
    #declaramos los diferentes sensores que vamosa  a utilizar
    sensorAcelerometro = MMA7660FC(i2c)
    sensorPulsometro = grove_fingerclip_heart_sensor()
    # el while no creo que haga falta porque solo se quiere hacer cuando se mande una señal
    while True:
        # Guardar en csv Un log de inicio de programa
        my=logging.info('Iniciamos las mediciones')
        with open("log.csv", "a+", newline ='\n') as csvfile:
           wr = csv.writer(csvfile, dialect='excel', delimiter='.', lineterminator="\n")
           wr.writerow("Entrada correcta en el bucle")
        try:
            pulso = sensorPulsometro.pulse_read()
            sData = sensorAcelerometro.acceleration_read()
            main()
            hum_temp_read()
            payload = "values,place=miCasa humi{},temp={},tilt={},pulse={},ac1={},ac2={},ac3={}\n".format(variables.humi,variables.temp,variables.t,variables.pulso,variables.sData[0],variables.sData[1],variables.sData[2])
            r = requests.post(url, params=variables.params, data=payload)
            GPIO.cleanup()
            time.sleep(1)
        except IOError:
        # Guardado en csv de un log de error
            myFields=logging.warning('Se ha generado un error del tipo IoErr, por lo que hemos tenido problemas en las mediciones')
            with myFile: 
                writer = csv.DictWriter(myFile, fieldnames=myFields) 
        time.sleep(1)
