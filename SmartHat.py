from sense_hat import SenseHat
import time

#Initialising variables
sense = SenseHat()              #Creating object from SenseHat library

temp = sense.get_temperature()  #Storing temperature  from SenseHat function
humidity = sense.get_humidity() #Storing humidity     from SenseHat function


#Function to detect if the SenseHat is moving
#If SenseHat is moving, measure the temperature and humidity
#Print the temperature and humidity on the 8 pin Board
class SmartHatPi():
    def checkTemAndHum():
        
        #Colors RGB codes to be used when displaying text on Pins.
        white  = (200, 200, 200) 
        blue   = (  0, 102, 102) 
        pink   = (204,   0, 204)
        red    = (255,   0,   0)
        yellow = (255, 255,   0)
        purple = (127,   0, 255)
        green  = (  0, 255,   0)
        black  = (  0,   0,   0)

        #Text moving speed
        lspeed = 0.10 # Slow   speed
        mspeed = 0.15 # Medium speed
        fspeed = 0.20 # Fast   speed
        
        detectNum = 0.1                 #Storing a float number, to be compared against x value of the accelerometer
            
        #Initialise Loop to True
        Loop = True 
            
        while Loop: #While Loop equals to True, do the following:
            acc  = sense.get_accelerometer_raw()#Get the values of the accelerometer
            x = acc['x']#Save the X value of the accelerometer
            y = acc['y']#Save the Y value of the accelerometer
            z = acc['z']#Save the Z value of the accelerometer
            print("x {0} ".format(x))#Print the values in the console
            time.sleep(1)                            #Screen sleep
            
            
            #Check if SenseHat module is moving
            if x>detectNum:                         
                print("Measuring temperature and humidty")#Print message
                print("Temp: %s C" % temp)               # Shows temperature   value  on console
                print("Humidity: %s %%rH" % humidity)    # Shows humidity      value  on console
                sense.set_rotation(0)        # Set LED matrix to scroll from right to left
                
                #Displaying temperature
                sense.show_message(
                                    text_string  = "%.1f C" % temp, #Temperature value
                                    scroll_speed =          mspeed, #Text scrolling speed
                                    text_colour  =             green, #Text colour
                                    back_colour  =            white #Text background colour
                                  )
                
                # Wait 1 second
                time.sleep(1)           
                
                #Display humidity
                sense.show_message(
                                    text_string  = "%.1f %%rH" % humidity, #Humidity value
                                    scroll_speed = 0.15,                   #Text scrolling speed
                                    text_colour  = blue,                       #Text colour
                                    back_colour  = white                      #Text background colour
                                   ) 
                #Set loop back to True
                sense.clear()
                Loop = True
            
SmartHatPi.checkTemAndHum()        
sense.clear()