# Proyecto silla inteligente
## Componentes 
 - Raspberry Pi 3b+
 - Tilt v1.1
 - Temperature&Humidity sensor v1.2
 - 3-Axis Digital Gyro v1.3
 - Finger-clip Heart Rate Sensor v1.0
 - 4 cables para los sensores
 
## Explicación

El proyecto que tenemos subido se trata de un script que permite la lectura de los sensores (acelerometro, pulsometro, humedad/temperatura e inclinación) 
y posteriormente subirlo a Corlysis (un servicio de almacenamiento en la nube). 

Además, empleamos Grafana para mostrar los datos recopilados de la Raspberry Pi 3 en formato de graficos y tener un muestreo constante de datos en todo 
momento que se este ejecutando el script. 

## Código

El codigo se inicia de forma que comprobemos que el sistema operativo alojado en el dispositivo que ejecuta el codigo sea linux, para no tener incovenientes con la compatibilidad. 
Después, introducimos los parametros para poder hacer posteriormente los "POST" al servidor de Corlysis. 

Declaramos dos clases, las cuales sirven para poder hacer la lectura del acelerometro y el pulsometro, incluyendo el metodo de subida para el servidor. Tambien incluimos un par 
de metodos que se encargan de hacer lo propio con los sensores de humedad/temperatura y muestran los datos sobre el comportamiento del hardware y su estado actual.

Al final, posteamos la información del acelerometro y añadimos un log en el que se mostrara la informacion de ejecucion y si en algun momento existe algún fallo. 
