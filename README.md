# HomeBerryPi
Smart home device created on a Raspberry Pi 4 for my final year project at the University of Portsmouth. The smart device has two functions, the Smart Security Camera and the Smart Meter. 

The security camera can detect objects, if the object detected is a human/dog/cat, the camera will start video recording only for as long as the object is still being detected. The system will also take a picture, save it locally and send it over to an gmail email address to inform the user about the intruder. 

The Smart Meter measures the temperature, humidity and pressure. The user is able to triger the functions in two ways, first method requires the user to trigger the device physically by lifting the device, this will print the climate units on the display. The second method involves opening the web application by visiting localhost:5000.

The smart camera uses Tensorflow Lite and Google Coral Edge TPU for object detection. The smart meter uses the SenseHat sensor to measure the desired units.

The RTIMU library must be installed in the project directory to use the SenseHat. 
