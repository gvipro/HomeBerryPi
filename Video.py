import time
import cv2
from threading import Thread

class Video:
    def __init__(self,resolution=(1280,720),framerate=30):
        
        self.device_index = 0 # 0 Represents the Camera Module
        self.fps = 30               # fps
        self.fourcc = "MJPG"       # file format
        self.frameSize = (1280,720) # Set frame size
        
        # Tell system where to store video file, use current date and time as a name and save as format avi
        self.video_filename = "SmartCamera/videos/" + (time.strftime("%b%d-%H:%M-20%y")) + ".avi" 
        self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc) #Write the codec for video file
    
        #Tell camera to use Nigh-Vision Camera as input
        self.video = cv2.VideoCapture(self.device_index)
        #Set video to use codec FOURCC - MJPG 
        ret = self.video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.video.set(3,resolution[0])#Set resolution from argument 
        ret = self.video.set(4,resolution[1])#Set resolution from argument
            
        
        # Read first frame from the video
        (self.capture, self.frame) = self.video.read()

        # Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
        # Start the thread that reads frames from the video 
        Thread(target=self.update,args=()).start()
        return self 
        
    def update(self):    
        # Loop until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.video.release()
                return

            # Capture next frame
            (self.capture, self.frame) = self.video.read()
            
    def newVideo(self):
        self.video_out = cv2.VideoWriter(self.video_filename, self.video_writer, self.fps, self.frameSize)
    
    def saveVideo(self):
        self.video_out.write(self.frame)
    
    
    # Return the most recent frame
    def read(self):
        return self.frame
    
    
    #Change stopped value to True to stop thread and camera
    def stop(self):
        self.stopped = True
