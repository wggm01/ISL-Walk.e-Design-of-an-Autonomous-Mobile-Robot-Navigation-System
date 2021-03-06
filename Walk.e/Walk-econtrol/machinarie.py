
#Inicializacion de librerias
import datetime
import time
import serial
import csv
import math
import smbus

#Variables y Esclavos (visto desde la pcb)
mizq = 0x40                     #LIBRERIAS, ESCLAVOS Y INSTRUCCIONES
mder = 0x50
dist_sensoraddr = 0x60
bus = smbus.SMBus(1)
ins = [1,2,4,3,5,6,7,8,9,10,11,12,13]

#banderas para regiones

callreg0=1
callreg1=1
callreg2=1
callreg3=1

callreg0c=1
callreg1c=1
callreg2c=1
callreg3c=1

global callreg
callreg = [1,1,1,1,1,1,1,1]

delay = 1 #LO USARE.
limit = 9
#Connecion al puerto serial
#gps = serial.Serial('COM14', 4800)

gps = serial.Serial("/dev/ttyACM2", baudrate = 4800)
ard_gyro = serial.Serial("/dev/ttyACM1", baudrate = 9600)
ard_ultra = serial.Serial("/dev/ttyACM0", baudrate = 9600)


#Vectores como variables globales incializdas en 0 para luego ser modi.
global p
global xa
global ya
global q
global drp
global coordntp

p = [0,0] #Posicion dinamica
xa = [-79.53169299,-79.53152138,-79.53177739,-79.53184155] #X1 Y X2 corresponden a abcisas del punto inicio y finalsel.
ya = [9.023410836,9.023175628,9.022897331,9.023147334] #Y1 Y Y2 corresponden a ordenadas del punto inicio y finalsel.
q = [0,0] # Puntos virtual trasladado
drp = [0,0,0,0] #una para cada modelo y0,y1,y2,y3
coordntp = [0,0]

#Envio de Instruciones
def hardrst(inst):
	bus.write_byte(mizq,inst)
	bus.write_byte(mder,inst)

def wr_i2c (instruction, flag):
	if flag == 1:
		data = instruction
		bus.write_byte(mizq,data)
		bus.write_byte(mder,data)
	else:
		#wr_i2c.func_code = (lambda:None).func_code
		print("instruccion enviada")

#Latitud(x), Longitud(y) evitar coordenadas iguales



def not_repeatcoord (latitud,longitud):


	if latitud != coordntp[0] and longitud != coordntp[1] :
		return latitud, longitud
	else:
		coordntp[0]= latitud
		coordntp[1] = longitud

def get_data_gyro() :
	ard_gyro_data= ard_gyro.readline()
	time= datetime.datetime.now()
	with open ("gyrodata.csv", "a") as pos:
            pos.write("%s, %s \n" % ( ard_gyro_data,time))

def get_data_ultra() :
        ard_ultra_data= ard_ultra.readline()
        time= datetime.datetime.now()
        with open ("ultradata.csv", "a") as pos:
            pos.write("%s, %s \n" % ( ard_ultra_data,time))

#def check_gps():
#	gps_sentence = gps.readline()
#	gps_sentences_fields = gps_sentece.split(",")
#	if gps_sentences_fields[0]=="$GPRMC" and gps_sentences_fields[2] == "A":
#        	lock=1
#	else:
#		lock =0
#	return lock
    	


def Data():

	gps_sentece = gps.readline()
	gps_sentences_fields = gps_sentece.split(",")
	#FILTRO DE LA SENTENCIA $GPRMC
	if gps_sentences_fields[0] == "$GPRMC" and  gps_sentences_fields[2] == "A":
        	get_unformated_latitude = float(gps_sentences_fields[3])
       		get_unformated_longitude = float(gps_sentences_fields[5])
		
        	latdeg = int(get_unformated_latitude/100)
        	latmin = get_unformated_latitude - latdeg*100
        	lat = latdeg + (latmin/60)
        	latitud = round(lat,7)

        	longdeg = int(get_unformated_longitude/100)
        	longmin = get_unformated_longitude - longdeg*100
        	longi = longdeg + (longmin/60)
        	longitud = round(longi,7)

        	if gps_sentences_fields[4] == "S":
            		latitud = -latitud
        	if  gps_sentences_fields[6] == "W":
            		longitud = -longitud
        	now = datetime.datetime.now()
		with open ("raw_coords.csv", "a") as pos:
            		pos.write("%s, %s, %s\n" % ( latitud, longitud,now))
	
 		return latitud,longitud 

#Calculo de de distancia para cada region (cambiar referencia en cada uno)
def distReg0(latitud,longitud):
    latref =9.023175628
    longref = -79.53152138 #UTP
    radius = 6371 # km
    dlat = math.radians(latref-latitud)
    dlon = math.radians(longref-longitud)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(latitud)) \
    * math.cos(math.radians(latref)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d_raw = float((radius*c)*1000)
    d = int(d_raw)
    re= "Region 0"
    with open ("logreg0.csv", "a") as pos:
        pos.write("%s, %s, %s, %s\n" % ( latitud, longitud, d, re ))
    return d

def distReg1(latitud,longitud):
    latref2=9.022897331#UTP
    lonref2=-79.53177739
    radius = 6371 # km
    dlat = math.radians(latref2-latitud)
    dlon = math.radians(lonref2-longitud)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(latitud)) \
    * math.cos(math.radians(latref2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d_raw = float((radius*c)*1000)
    d = int(d_raw)
    re= "Region 1"
    with open ("logreg1.csv", "a") as pos:
        pos.write("%s, %s, %s, %s\n" % ( latitud, longitud, d, re ))
    return d

def distReg2(latitud,longitud):
    latref =9.023147334
    longref = -79.53184155 #UTP
    radius = 6371 # km
    dlat = math.radians(latref-latitud)
    dlon = math.radians(longref-longitud)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(latitud)) \
    * math.cos(math.radians(latref)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d_raw = float((radius*c)*1000)
    d = int(d_raw)
    re= "Region 2"
    with open ("logreg2.csv", "a") as pos:
        pos.write("%s, %s, %s, %s\n" % ( latitud, longitud, d, re ))
    return d

def distReg3(latitud,longitud):
    latref2=9.023410836 #UTP
    lonref2=-79.53169299
    radius = 6371 # km
    dlat = math.radians(latref2-latitud)
    dlon = math.radians(lonref2-longitud)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(latitud)) \
    * math.cos(math.radians(latref2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d_raw = float((radius*c)*1000)
    d = int(d_raw)
    re= "Region 3"
    with open ("logreg3.csv", "a") as pos:
        pos.write("%s, %s, %s, %s\n" % ( latitud, longitud, d, re ))
    return d

#Limites de desplazamiento del robot
def region0Bounds(d,reg0):
    min1=200 #colocar
    max1=2
    min2=3

    #ed0 = enco_check_reg0(d)
    if d < min1 and d >= max1: #Establece hasta donde se movera en linea recta
		#wr_i2c(int(ins[0]))
		if callreg[0] == 1:
			wr_i2c(ins[0],1) #envio la distancia para que el robot se mueva la convierta en pasos
			print("Wall-i acutalmente se esta moviendo reg0")
			callreg[0]=callreg[0]+1
		else:
			wr_i2c(14,2)

    if d <= min2:#Establece cuando curvara
		if callreg[1] == 1:
			wr_i2c(ins[3],1)
			print("Wall-i actualmente esta curvandoreg0")
        		time.sleep(delay) #correccion de region curvara y luego avanzara para obligarlo
			callreg[1]=callreg[1]+1

		else:
			wr_i2c(14,2) #dummy ins

def region1Bounds(d,reg1):
    min1=200 #colocar
    max1=2
    min3=3
    #ed1 = enco_check_reg1(d)
    if d < min1 and d >= max1: #Establece hasta donde se movera en linea recta
		if callreg[2] == 1:
			wr_i2c(ins[0],1) #envio la distancia para que el robot se mueva la convierta en pasos
			print("Wall-i acutalmente se esta moviendo reg1")
			callreg[2]=callreg[2]+1
		else:
			wr_i2c(14,2)

    if d <= min3:#Establece cuando curvara

		if callreg[3] == 1:
			wr_i2c(ins[3],1)
			print("Wall-i actualmente esta curvandoreg1")
        		time.sleep(delay) #obligando a cambio de region
			callreg[3]=callreg[3]+1
		else:
			wr_i2c(14,2) #dummy ins

def region2Bounds(d,reg2):
    min1=200 #colocar
    max1=2
    min2=3
    #ed2 = enco_check_reg2(d)
    if d < min1 and d >= max1: #Establece hasta donde se movera en linea recta
		if callreg[4] == 1:
			wr_i2c(ins[8],1) #envio la distancia para que el robot se mueva la convierta en pasos
			print("Wall-i acutalmente se esta moviendo reg2")
			callreg[4]=callreg[4]+1
		else:
			wr_i2c(14,2)

    if d <= min2:#Establece cuando curvara
		if callreg[5] == 1:
			wr_i2c(ins[8],1)
			print("Wall-i actualmente esta curvandoreg2")
        		time.sleep(delay) #obligando a cambio de region
			callreg[5]=callreg[5]+1
		else:
			wr_i2c(14,2) #dummy ins

def region3Bounds(d,reg3):
    min1=200 #colocar
    max1=2
    min3=3
    #ed3 = enco_check_reg3(d)
    if d < min1 and d >= max1: #Establece hasta donde se movera en linea recta
		if callreg[6] == 1:
			wr_i2c(ins[0],1) #envio la distancia para que el robot se mueva la convierta en pasos
			print("Wall-i acutalmente se esta moviendo reg3")
			callreg[6]=callreg[6]+1
		else:
			wr_i2c(14,2)

    if d <= min3:#Establece cuando curvara
		if callreg[7] == 1:
			wr_i2c(ins[4],1)
			print("Wall-i actualmente esta curvandoreg3")
        		time.sleep(delay) #obligando a cambio de region
			callreg[7]=callreg[7]+1
		else:
			wr_i2c(14,2) #dummy ins
        #time.sleep(delay)

#Traslacion de coordenadas
def virtual_pos0 (latitud,longitud):
    p[0]=longitud#x
    p[1]=latitud

    #Calculo de pendientes:
    m1 =(ya[1]-ya[0])/(xa[1]-xa[0])
    m2 = -1/m1
    #calculo de interseccion de ambas rectas,esto me da la lat,long (virtual)
    x = (m1*xa[0]-ya[0]+p[1]-m2*p[0])/(m1-m2)
    y = m1*(x-xa[0])+ya[0]
    q[0]=x#Longitud
    q[1]=y#Latitud
    #calculo de distancia entre punto virtual trasladado y punto de referenciaself.
    #d_rest = math.sqrt(math.pow(xa[1]-q[0],2)+ math.pow(ya[1]-q[1],2))

    return q[1],q[0]

def virtual_pos1 (latitud,longitud):
    p[0]=longitud#x
    p[1]=latitud
    #Calculo de pendientes:
    m1 =(ya[2]-ya[1])/(xa[2]-xa[1])
    m2 = -1/m1
    #calculo de interseccion de ambas rectas,esto me da la lat,long (virtual)
    x = (m1*xa[1]-ya[1]+p[1]-m2*p[0])/(m1-m2)
    y = m1*(x-xa[1])+ya[1]
    q[0]=x#Longitud
    q[1]=y#Latitud
    #calculo de distancia entre punto virtual trasladado y punto de referenciaself.
    #d_rest = math.sqrt(math.pow(xa[1]-q[0],2)+ math.pow(ya[1]-q[1],2))

    return q[1],q[0]

def virtual_pos2 (latitud,longitud):
    p[0]=longitud#x
    p[1]=latitud
    #Calculo de pendientes:
    m1 =(ya[3]-ya[2])/(xa[3]-xa[2])
    m2 = -1/m1
    #calculo de interseccion de ambas rectas,esto me da la lat,long (virtual)
    x = (m1*xa[2]-ya[2]+p[1]-m2*p[0])/(m1-m2)
    y = m1*(x-xa[2])+ya[2]
    q[0]=x#Latitud
    q[1]=y#Longitud
    #calculo de distancia entre punto virtual trasladado y punto de referenciaself.
    #d_rest = math.sqrt(math.pow(xa[1]-q[0],2)+ math.pow(ya[1]-q[1],2))

    return q[1],q[0]

def virtual_pos3 (latitud,longitud):
    p[0]=longitud#x
    p[1]=latitud
    #Calculo de pendientes:
    m1 =(ya[0]-ya[3])/(xa[0]-xa[3])
    m2 = -1/m1
    #calculo de interseccion de ambas rectas,esto me da la lat,long (virtual)
    x = (m1*xa[3]-ya[3]+p[1]-m2*p[0])/(m1-m2)
    y = m1*(x-xa[3])+ya[3]
    q[0]=x#Latitud
    q[1]=y#Longitud
    #calculo de distancia entre punto virtual trasladado y punto de referenciaself.
    #d_rest = math.sqrt(math.pow(xa[1]-q[0],2)+ math.pow(ya[1]-q[1],2))

    return q[1],q[0]

#Chequeo de punto actual del robot a recta
def check_0drp (latitud,longitud,latref,longref):
    #Calculo de distancia a los modelos
    #latv0=latref
    #lonv0=longref
    #print(latitud,longitud,latref,longref)
    radius = 6371 # km
    dlat = math.radians(latref-latitud)
    dlon = math.radians(longref-longitud)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(latitud)) \
    * math.cos(math.radians(latref)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d_raw = float((radius*c)*1000)
    d = int(d_raw)
    drp[0]= d

    return drp[0]

def check_1drp (latitud,longitud,latv1,lonv1):
    #Calculo de distancia a los modelos
    latref = latv1
    longref = lonv1
    radius = 6371 # km
    dlat = math.radians(latref-latitud)
    dlon = math.radians(longref-longitud)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(latitud)) \
    * math.cos(math.radians(latref)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d_raw = float((radius*c)*1000)
    d = int(d_raw)
    drp[1]=d

    return drp[1]

def check_2drp (latitud,longitud,latv2,lonv2):
    #Calculo de distancia a los modelos
    latref = latv2
    longref = lonv2
    radius = 6371 # km
    dlat = math.radians(latref-latitud)
    dlon = math.radians(longref-longitud)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(latitud)) \
    * math.cos(math.radians(latref)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d_raw = float((radius*c)*1000)
    d = int(d_raw)
    drp[2]=d

    return drp[2]

def check_3drp (latitud,longitud,latv3,lonv3):
    #Calculo de distancia a los modelos
    latref = latv3
    longref = lonv3
    radius = 6371 # km
    dlat = math.radians(latref-latitud)
    dlon = math.radians(longref-longitud)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(latitud)) \
    * math.cos(math.radians(latref)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d_raw = float((radius*c)*1000)
    d = int(d_raw)
    drp[3]=d

    return drp[3]

"""
#------------------------
def enco_check_reg0(d):
	count_R=d
    count = (91*count_R)/31 # distancia de region en ticks
    CS1 = GPIO.input(clk1)
    DTS1 = GPIO.input(dt1)
    CS2 = GPIO.input(clk2)
    DTS2 = GPIO.input(dt2)
    if CS1 != CLS1:
        if DTS1 != CS1:
            derecha1 += 1
    if CS2 != CLS2:
        if DTS1 != CS1:
            derecha2 += 1
    if (derecha1 > count) or (derecha2 > count):
        edr0 = 1
        return edr0
    else:
        return edr0 = 0

	enco_check_reg0.func_code = (lambda:None).func_code

#--------------------------
def enco_check_reg1(d):

	count_R=d

    count = (91*count_R)/31 # distancia de region en ticks
    CS1 = GPIO.input(clk1)
    DTS1 = GPIO.input(dt1)
    CS2 = GPIO.input(clk2)
    DTS2 = GPIO.input(dt2)
    if CS1 != CLS1:
        if DTS1 != CS1:
            derecha1 += 1
    if CS2 != CLS2:
        if DTS1 != CS1:
            derecha2 += 1
    if (derecha1 > count) or (derecha2 > count):
        edr1 = 1
        return edr1
    else:
        return edr1 = 0
	enco_check_reg1.func_code = (lambda:None).func_code
#--------------------------
def enco_check_reg2(d):

	count_R=d

    count = (91*count_R)/31 # distancia de region en ticks
    CS1 = GPIO.input(clk1)
    DTS1 = GPIO.input(dt1)
    CS2 = GPIO.input(clk2)
    DTS2 = GPIO.input(dt2)
    if CS1 != CLS1:
        if DTS1 != CS1:
            derecha1 += 1
    if CS2 != CLS2:
        if DTS1 != CS1:
            derecha2 += 1
    if (derecha1 > count) or (derecha2 > count):
        edr2 = 1
        return edr2
    else:
        return edr2 = 0
	enco_check_reg2.func_code = (lambda:None).func_code

def enco_check_reg3(d):

	count_R=d

    count = (91*count_R)/31 # distancia de region en ticks
    CS1 = GPIO.input(clk1)
    DTS1 = GPIO.input(dt1)
    CS2 = GPIO.input(clk2)
    DTS2 = GPIO.input(dt2)
    if CS1 != CLS1:
        if DTS1 != CS1:
            derecha1 += 1
    if CS2 != CLS2:
        if DTS1 != CS1:
            derecha2 += 1
    if (derecha1 > count) or (derecha2 > count):
        edr3 = 1
        return edr3
    else:
        return edr3 = 0
	enco_check_reg3.func_code = (lambda:None).func_code

def flag_sensor_dist():
    if bus.read_byte(slave_dist_sensor)==8:
        return 8
    elif bus.read_byte(slave_dist_sensor)== 9:
        return 9
    else:
        return 1









    def secCorrec ():
        if bus.read_byte(sensorAdress) == 9:
            bus.write_byte(slaveAddress2, Stop)
            bus.write_byte(slaveAddress1, Stop)
            time.sleep(2)
            bus.write_byte(slaveAddress2,Backward )
            bus.write_byte(slaveAddress1,Backward)
            time.sleep(2)
            bus.write_byte(slaveAddress2,Stop)
            bus.write_byte(slaveAddress1,Stop)
            time.sleep(2)
            bus.write_byte(slaveAddress2,TurnLeftEje)
            bus.write_byte(slaveAddress1,TurnLeftEje)
            time.sleep(3.21)
            bus.write_byte(slaveAddress2,Stop)
            bus.write_byte(slaveAddress1,Stop)
            time.sleep(2)
            bus.write_byte(slaveAddress2,Forward)
            bus.write_byte(slaveAddress1,Forward)
            time.sleep(2)
            bus.write_byte(slaveAddress2,Stop)
            bus.write_byte(slaveAddress1,Stop)
            time.sleep(2)
            bus.write_byte(slaveAddress2, Turn)
            bus.write_byte(slaveAddress1, Turn)
            time.sleep(3)

        elif bus.read_byte(sensorAdress) == 8:
            checkD2=2
            return checkD2

        else:
            bus.write_byte(slaveAddress2, Forward)
            bus.write_byte(slaveAddress1, Forward)
"""
