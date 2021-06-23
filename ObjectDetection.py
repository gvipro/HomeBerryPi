import os
import argparse
import cv2
import numpy as np
import sys
import time
import importlib.util

from Mail      import Emailer
from Video     import Video


# Setting up arguments################
parser = argparse.ArgumentParser()
parser.add_argument('--coraledgetpu', help='EDGE TPU ',action='store_true') #Check if true
parser.add_argument('--graphname', help='Name of the tflite file', default='detect.tflite')#Default tflite file
parser.add_argument('--labelmap', help='Name of the labelmap file', default='labelmap.txt') #Default labelmap
parser.add_argument('--minthreshold', help='Minimum confidence threshold', default=0.5) #Default value is 0.5
parser.add_argument('--modeldirectory', help='Location of tflite file', required=True) #Required to run the system
parser.add_argument('--resolution', help='Resolution of input', default='1280x720') #Default resolution is 1280x720

#Parse arguments######################################################
args = parser.parse_args()

isEdgeTPU = args.coraledgetpu
confMinThreshold = float(args.minthreshold)
InputGraph = args.graphname
CoralModelName = args.modeldirectory
LabelMap = args.labelmap

#Parse screen resolution#############################################
scrWidth, scrHeight = args.resolution.split('x')
intWidth, intHeight = int(scrWidth), int(scrHeight)

#####################################################################

TFLite = importlib.util.find_spec('tflite_runtime')#importing tensorflow library

if TFLite: #Check if library is used
    
    #From tflite import the interpreter
    from tflite_runtime.interpreter import Interpreter 
    
    #If Coral Edge TPU is used 
    if isEdgeTPU:
        
        #From tflite runtime import load_delegate
        from tflite_runtime.interpreter import load_delegate 

#Otherwise:
else:
    #From tensorflow lite import interpreter
    from tensorflow.lite.python.interpreter import Interpreter
    
    #If Edge TPU is used:
    if isEdgeTPU:
        
        #From tensorflow lite import load_delegate
        from tensorflow.lite.python.interpreter import load_delegate

######################################################################

# If using Edge TPU
if isEdgeTPU:
    
    #Use edgetpu.tflite by default 
    InputGraph = 'edgetpu.tflite'       

# The path to file directory 
PathToDirectory = os.getcwd()

# The path to the tflite model
PathToTFLite = os.path.join(PathToDirectory,CoralModelName,InputGraph)

# The path to the labelmap
LabelPath = os.path.join(PathToDirectory,CoralModelName,LabelMap)

# Load the label map
with open(LabelPath, 'r') as b:
    labels = [line.strip() for line in b.readlines()]

#Check if first label is "???" if so:
if (labels[0] == '???'):
    
    #Deconstruct the first label in the array
    del(labels[0])


if isEdgeTPU:
    
    #Loading tensorflow model with special load delegate
    interpreter = Interpreter(model_path=PathToTFLite, experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    
else:
    interpreter = Interpreter(model_path=PathToTFLite)

interpreter.allocate_tensors()

# Acquire Model details
outModel    = interpreter.get_output_details() #Output
inModel     = interpreter.get_input_details() #Input 
modelHeight = inModel[0]['shape'][1] #Model modelHeight
modelWidth  = inModel[0]['shape'][2] #Model modelWidth
isNonQuan   = (inModel[0]['dtype'] == np.float32)
inmean      = 127.5
instd       = 127.5

#----------------------- Creating objects from classes ------------------------------------------#

#Camera Setup
videostream = Video(resolution=(intWidth,intHeight),framerate=30).start()#Create an object based on Video class 

#Email Setup
sender = Emailer() #Create an object from Emailer object

#stopRecording = False #Variable to check if video recording has been stopped
cameraWorking = True  #Variable to check if camera is working



#Captured Directory + name + format
imgPath = "SmartCamera/images/" + (time.strftime("%b%d-%H:%M-20%y")) + ".jpg"#Specify the directory and the name where to image to be saved


def detectingObjects():
    
    #----------------------- Camera & Video Setup ------------------------------------------#
    
    #Call Video class function to create video path 
    videostream.newVideo()
    
    #Camera variable 
    cameraWorking = True  #Variable to check if camera is working
    validLabel = ['person','cat', 'dog']

    #----------------------- Timers settup ------------------------------------------#
    #Camera Timer Setup
    updateTimer = 600 #Set email update timer to 10 minutes 
    currentTime = 0   #Set current time to 0 

    #FPS
    getFrequency = cv2.getTickFrequency()
    fpsCounter = 1
   
    
    while cameraWorking:
        
        # Start timer (for calculating frame rate)
        t1            = cv2.getTickCount()
        objDetected   = False #Variable to check if an object has been detected
        stopRecording = False 
           
        #Prepare input for object detection
        firstFrame           = videostream.read()#Get the first frame
        capImg               = firstFrame.copy()#Make a copy of the frame
        imageRGB             = cv2.cvtColor(capImg, cv2.COLOR_BGR2RGB)#Change color space to gray
        resizeImage          = cv2.resize(imageRGB, (modelWidth, modelHeight))#Resize the image
        objDetectionInput    = np.expand_dims(resizeImage, axis=0)#Input Data for Object Detection
        
        #Checking if model pixels are not quantised
        if isNonQuan:
                
                #if they are make them normal
                objDetectionInput = (np.float32(objDetectionInput) - inmean) / instd

        #Start detection
        interpreter.set_tensor(inModel[0]['index'],objDetectionInput)#Use resized image as input
        interpreter.invoke()
        objDetectedCoordinates = interpreter.get_tensor(outModel[0]['index'])[0] # Coordinates 
        objDetectedClass = interpreter.get_tensor(outModel[1]['index'])[0] # Class index 
        objDetectedAccuracy = interpreter.get_tensor(outModel[2]['index'])[0] # Confidence

        #Check for objects      
        for j in range(len(objDetectedAccuracy)):
            
            #If the confidence is greater than 0.5 activate:
            if (objDetectedAccuracy[j] > confMinThreshold):
                
                #If an object has been detected set objDetected to True
                objDetected = True    
                
                #Get coordinates
                yMinValue = int(max(1  ,(objDetectedCoordinates[j][0] * intHeight)))
                xMinValue = int(max(1  ,(objDetectedCoordinates[j][1] * intWidth)))
                yMaxValue = int(min(intHeight,(objDetectedCoordinates[j][2] * intHeight)))
                xMaxValue = int(min(intWidth,(objDetectedCoordinates[j][3] * intWidth)))
                
                #Draw frame around object
                cv2.rectangle (capImg, (xMinValue,yMinValue),
                              (xMaxValue,yMaxValue),
                              (200, 230, 0),             3)
                
                objectLabel            = labels[int(objDetectedClass[j])] #Check list with detections
                label                  = '%s' % (objectLabel)#Set template
                getLabelSize, txtline  = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 0.9, 4)#Get Text String    
                
                #Create white box for text
                cv2.rectangle (capImg, (xMinValue,  yMinValue-getLabelSize[1]),
                              (xMinValue+getLabelSize[0], yMinValue+txtline),
                              (255, 255, 255),                   cv2.FILLED) 
                
                #Draw label text
                cv2.putText   (capImg, label,
                              (xMinValue, yMinValue), cv2.FONT_HERSHEY_PLAIN,
                               0.9, (0, 0, 0), 2                            )
    
                #-----------------------Send an email to the user if an object has been detected------------------------------------------#
                 
                #If object detected is in list with valid labels and the current time in seconds is greather than the update timer: 
                if ((objectLabel in validLabel) and (time.time() - currentTime) > updateTimer):
                    currentTime = time.time()   #Set currentTime equal to current time
                    cv2.imwrite(imgPath, capImg) #From cv2 library call function imwrite to save image to specified directory
                    sender.sendMail(imgPath)    #Calling sendMail function from Mail class to send an email with the image
                    #print(objectLabel + " has been detected. Sending email.")  #Test line to check if email is sent.
                    break #Break the loop and continue with next function
                            
                              
                #---------------------------- Start video recording if an object has been detected-------------------------------------#
                #If an object has been detected and the object is a person do the following:
                if (objectLabel in validLabel) and (objDetected == True):
                    videostream.saveVideo()
                    #print(objectLabel + " has been detected, recording video.")#Test command printing object class name in console
                   
                    if (objDetectedAccuracy[j] < 0.5):
                        #Break the function
                        break
                    
                #Break the loop 
                break
            #Break the loop 
            break

        # Draw framerate in corner of frame
        cv2.putText(capImg,'FPS: {0:.2f}'.format(fpsCounter),(50,50),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2,cv2.LINE_AA)
        cv2.imshow('HomeBerrPi - Smart Security Camera', capImg)

        # Calculate framerate
        timer2 = cv2.getTickCount()
        time1 = (timer2-t1)/getFrequency
        fpsCounter= 1/time1
     
        if cv2.waitKey(1) == ord('s'):
            break

detectingObjects()
    
    






