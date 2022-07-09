
#!/usr/bin/python3
# -*- coding:utf-8 -*-
import serial  # Més informació --> https://pyserial.readthedocs.io/en/latest/pyserial.html

def checksum(strText):
    checksum= 0
    for letter in strText:
        checksum ^= ord(letter)
    
    str_checksum=hex(checksum).upper()[2:] 
    return str_checksum

def info_freq_set(time_in_ms=1000):
    #The time between means must be greater than 100 ms.
    #Example for 300ms ControlCode= '$PMTK300,300,0,0,0,0*3E'
    #More info: https://www.quectel.com/UploadImage/Downlad/Quectel_L80_GPS_Protocol_Specification_V1.2.pdf
    
    ControlCode= 'PMTK300,'+ str(time_in_ms) + ',0,0,0,0'
    Command_ControlCode= '$' + ControlCode + '*' + checksum(ControlCode)
    return Command_ControlCode.encode()


def set_type_info_todisplay_GPGLL():
    #Example for GPGLL ControlCode= '$PMTK314,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29'
    #More info: https://www.quectel.com/UploadImage/Downlad/Quectel_L80_GPS_Protocol_Specification_V1.2.pdf
    
    ControlCode= 'PMTK314,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'
    Command_ControlCode= '$' + ControlCode + '*' + checksum(ControlCode) + '\r\n'
    return Command_ControlCode.encode()

def read_Latitude_Longitude_time_on_GPGLL(strPacket):
    #More info: https://www.quectel.com/UploadImage/Downlad/Quectel_L80_GPS_Protocol_Specification_V1.2.pdf
   
    strPacket= strPacket.decode('utf-8')
    aux = strPacket.split(',')
    if(aux[0]=='$GPGLL'):
        # We have a valid GPGLL packet
        if (aux[6] == 'A'):
            # We have a valid packet
            #Latitude
            Latitude= float(aux[1][0:2]) + float(aux[1][2:])/60
            if(aux[2]=='N'):
                #(N) -> the sign must be positive
                Latitude= Latitude
            else:
                #(S) -> the sign must be negative
                Latitude= -Latitude
            
            Longitude= float(aux[3][0:3]) + float(aux[3][3:])/60
            if(aux[4]=='E'):
                #(E) -> the sign must be positive
                Longitude= Longitude
            else:
                #(W) -> the sign must be negative
                Longitude= -Longitude

            timeinfo= aux[5]
            
            return Latitude, Longitude, timeinfo
        else:
            # It is not a GPGLL packet
            timeinfo= aux[5]
            
            return 0, 0, timeinfo
    else:
        #It is not a valid packet
        return 0,0,0





def main():
    
    port= '/dev/ttyS0'  # Uart -> '/dev/ttyS0'   USB -> '/dev/ttyUSB0'
    COM = serial.Serial(port, 9600)

    # Set type of information to display.
    COM.write(set_type_info_todisplay_GPGLL())

    # Set information frequency.
    COM.write(info_freq_set(1000))

    while True:
        COM_txt= COM.readline()
        if (COM_txt[0:6] == b'$GPGLL'):
            # GPGLL information package 
            Latitude, Longitude, timeinfo= read_Latitude_Longitude_time_on_GPGLL( COM_txt )
            print('Latitude: ', Latitude, ' Longitude: ', Longitude, ' Time: ', timeinfo)

    COM.close()

if __name__=="__main__":
   main()


    


        
