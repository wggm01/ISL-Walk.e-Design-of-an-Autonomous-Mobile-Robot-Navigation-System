<<<<<<< HEAD:distance.py
import smbus
import time
slaveAddress2 = 0x40
slaveAddress1 = 0x50
bus = smbus.SMBus(1)

#def writeNumber(value):
 #   bus.write_byte(slaveAddress2, value) #Funcion
  #  bus.write_byte(slaveAddress1, value)
   # bus.write_byte_data(address, 0, value)
   # return -1
#def readnumber():
 #   bus.read_byte(0X60)
  #  return -1

while True:
#    var = input("")
 #   if not var:
  #      continue
     if bus.read_byte(0X60) == 1:
	bus.write_byte(slaveAddress1,1)
	bus.write_byte(slaveAddress2,1)
	print(bus.read_byte(0X40))
     if bus.read_byte(0X60) == 2:
	bus.write_byte(slaveAddress1,2)
	bus.write_byte(slaveAddress2,2)
    	print(bus.read_byte(0X50))

     if bus.read_byte(0X60) == 7:
	bus.write_byte(slaveAddress1,7)
	bus.write_byte(slaveAddress2,7)
	print(bus.read_byte(0X60))
 #   writeNumber(var)
=======
import smbus
import time
slaveAddress2 = 0x40
slaveAddress1 = 0x50
bus = smbus.SMBus(1)

#def writeNumber(value):
 #   bus.write_byte(slaveAddress2, value) #Funcion
  #  bus.write_byte(slaveAddress1, value)
   # bus.write_byte_data(address, 0, value)
   # return -1
#def readnumber():
 #   bus.read_byte(0X60)
  #  return -1

while True:
#    var = input("")
 #   if not var:
  #      continue
     if bus.read_byte(0X60) == 1:
	bus.write_byte(slaveAddress1,1)
	bus.write_byte(slaveAddress2,1)
	print("Drive")
     if bus.read_byte(0X60) == 2:
	bus.write_byte(slaveAddress1,4)
	bus.write_byte(slaveAddress2,4)
    	print("Reverse")

     if bus.read_byte(0X60) == 7:
	bus.write_byte(slaveAddress1,7)
	bus.write_byte(slaveAddress2,7)
	print("Turn")
 #   writeNumber(var)
>>>>>>> cf7c35abf6ca5cfaa9f19fdcb37a91205f5c8427:Wallicontrol/distance.py