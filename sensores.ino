#include "DHT.h"
#include "pt.h"
#define DHTPIN 13 

#define DHTTYPE DHT11 
#define SensorPin A0
struct pt hilo1; // se define un objeto tipo pt

unsigned long int avgValue;
int senal[10], temp;
DHT dht(DHTPIN, DHTTYPE);
float phValue;
String  h, temperatura, cadenaDatos;

// Se ubica función para tener valores de pH
float medidorPh(struct pt  *pt) {
PT_BEGIN(pt); // se inicia la estructura del hilo con un puntero
do{
for(int i=0; i<10; i++){
senal[i]= analogRead(SensorPin);
delay(10);}
for(int i=0;i<9;i++){
for(int j=i+1;j<10;j++){
if(senal[i]>senal[j]){
temp=senal[i];
senal[i]=senal[j];
senal[j]=temp;
}
}
}
avgValue=0;
for(int i=2;i<8;i++){
   avgValue+=senal[i];}
float ph= (float) avgValue*5.0/1024/6;
ph= 3.5*ph;
 return ph;} while(true);
 PT_END(pt); // se termina el hilo
}
// se optiene el valor de humedad
String medidorHumedad() {
String humedad = (String) dht.readHumidity();
return humedad;
} 
// se optiene el valor de temperatura
String medidorTemperatura() {

String temp= (String) dht.readTemperature();
return temp;
}

void EnvioDatos(){
phValue= medidorPh(&hilo1);
h=medidorHumedad();
temperatura=medidorTemperatura();
cadenaDatos= (String) h+ ","+ phValue + "," + temperatura + "\r";
Serial.print(cadenaDatos); // se envia los datos por puerto serial
}
void setup() {
PT_INIT(&hilo1); //Se inicializa el thread
 Serial.begin(9600);
  dht.begin();
}

void loop() {
EnvioDatos();
delay(1000);
  
}
