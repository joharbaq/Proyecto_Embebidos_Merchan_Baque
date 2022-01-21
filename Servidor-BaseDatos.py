import os
import socket

from http.server import BaseHTTPRequestHandler, HTTPServer
import RPi.GPIO as GPIO
from time import*
from wiringpi import Serial
from firebase import firebase
import _thread
#Carla Merchan-JohnnyBaque
motor1Anti=5
motor1Hora=6
motor2Anti=12
motor2Hora=13
Enable1=16
Enable2=17
Comedor1=19
Comedor2=20
Fr1Motor1=26
Fr2Motor1=21
Fr1Motor2=24
Fr2Motor2=25
baud=9600
ser  = Serial("/dev/serial0",baud)
firebase = firebase.FirebaseApplication('https://proyecto-embebidos-28b51-default-rtdb.firebaseio.com/', None)
myip = socket.gethostbyname(socket.gethostname())
print (myip)
# se define una función para recibir datos por el puerto serial
def recibir():
 data = ""
 while True:
  input = ser.getchar()
  if input == "\r":
   return (data)
  data += input
 sleep(0.2)
 
def printsln(menss):
 ser.puts(menss+"\r")
 sleep(0.2)

def prints(menss):
 ser.puts(menss)
 sleep(0.2)
#Función para el registro de datos
def registroBaseDatos(item,nombre,medidas):
 firebase.put("/"+item, "/"+nombre, medidas)

def datosRecibidos():
 while (ser.dataAvail() <= 0):
   pass
 mensaje= recibir()
 lista= mensaje.split(",") #Se recibe los datos y se crea una lista para recorrerla 
 nombres= ["Humedad","Ph","Temperatura"]
 printsln(mensaje)
 for i in range (len(nombres)):
  registroBaseDatos("Mediciones",nombres[i],lista[i])
  printsln("Dato Guardado")
# funcion ubica a datosRecibidos en un bucle infinitp
def datos_thread():
 while 1:
  datosRecibidos()

_thread.start_new_thread(datos_thread, ()) # se crea un hilo para evitar condiciones de carrera
 
def peripheral_setup():
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(motor1Anti, GPIO.OUT)
 GPIO.setup(motor1Hora, GPIO.OUT)
 GPIO.setup(motor2Hora, GPIO.OUT)
 GPIO.setup(motor2Anti, GPIO.OUT)
 GPIO.setup(Enable1, GPIO.OUT)
 GPIO.setup(Enable2, GPIO.OUT)
 GPIO.setup(Comedor1, GPIO.OUT)
 GPIO.setup(Comedor2, GPIO.OUT)
 GPIO.setup(Fr1Motor1, GPIO.IN)
 GPIO.setup(Fr2Motor1, GPIO.IN)
 GPIO.setup(Fr1Motor2, GPIO.IN)
 GPIO.setup(Fr2Motor2, GPIO.IN)

 # se crea un servidor
def servidor():
 Request = None
 
 class RequestHandler_httpd(BaseHTTPRequestHandler):
  def do_GET(self):
   global Request

   messagetosend = bytes('Solicitando',"utf")
   self.send_response(200)
   self.send_header('Content-Type', 'text/plain')
   self.send_header('Content-Length', len(messagetosend))
   self.end_headers()
   self.wfile.write(messagetosend)
   Request = self.requestline
   Request = Request[5 : int(len(Request)-9)]
    #print(Request)
   if Request == 'motor1Anti':
    GPIO.output(Enable1,True)
    GPIO.output(motor1Anti,True)
    registroBaseDatos("Estados","Puerta 1" , "Abriendo")
    sleep(5);
    GPIO.output(Enable1,False)
    GPIO.output(motor1Hora,False)
    GPIO.output(motor1Anti,False)
    registroBaseDatos("Estados","Puerta 1" , "Abierto")
   if Request == 'motor1Hora':
    GPIO.output(Enable1,True)
    GPIO.output(motor1Hora,True)
    registroBaseDatos("Estados","Puerta 1" , "Cerrando")
    sleep(5);
    GPIO.output(Enable1,False)
    GPIO.output(motor1Hora,False)
    GPIO.output(motor1Anti,False)
    registroBaseDatos("Estados","Puerta 1" , "Cerrado")
   if Request == 'motor1Stop':
    GPIO.output(Enable1,False)
    GPIO.output(motor1Hora,False)
    GPIO.output(motor1Anti,False)
    registroBaseDatos("Estados","Puerta 1" , "Parada")
   if Request == 'motor2Anti':
    GPIO.output(Enable2,True)
    GPIO.output(motor2Anti,True) 
    registroBaseDatos("Estados","Puerta 2" , "Abriendo")
    sleep(5);
    GPIO.output(Enable2,False) 
    GPIO.output(motor2Hora,False)
    GPIO.output(motor2Anti,False)
    registroBaseDatos("Estados","Puerta 2" , "Abierto")
   if Request == 'motor2Hora':
    GPIO.output(Enable2,True)
    GPIO.output(motor2Hora,True)
    registroBaseDatos("Estados","Puerta 2" , "Cerrando")
    sleep(5);
    GPIO.output(Enable2,False)
    GPIO.output(motor2Hora,False)
    GPIO.output(motor2Anti,False)
    registroBaseDatos("Estados","Puerta 2" , "Cerrado")
   if Request == 'motor2Stop':
    GPIO.output(Enable2,False)
    GPIO.output(motor2Hora,False)
    GPIO.output(motor2Anti,False)
    registroBaseDatos("Estados","Puerta 2" , "Parada")
   if Request == 'Comedor1on':
    GPIO.output(Comedor1,True)
    registroBaseDatos("Estados","Comedor 1" , "Prendido")
   if Request == 'Comedor1off':
    GPIO.output(Comedor1,False)
    registroBaseDatos("Estados","Comedor 1" , "Apagado")
   if Request == 'Comedor2on':
    GPIO.output(Comedor2,True)
    registroBaseDatos("Estados","Comedor 2" , "Prendido")
   if Request == 'Comedor2off':
    GPIO.output(Comedor2,False)
    registroBaseDatos("Estados","Comedor 2" , "Apagado")
      
      
    
 server_address_httpd = (myip,8001) #Se define una tupla con la ip y el puerto 8081
 httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
 print('conectando a servidor')
 print(httpd.fileno())
 httpd.serve_forever()
 
def servidor_thread():
 while 1:
  servidor()
_thread.start_new_thread(servidor_thread, ())   # se crea otro hilo para trabajar con el servidor
 
def main () :

# Setup
 peripheral_setup()
 
# Infinite loop
 try:
  while 1 :
   pass
 except(KeyboardInterrupt,SystemExit):
  print ("BYE")
  GPIO.cleanup()
# Command line execution
if __name__ == '__main__' :
   main()