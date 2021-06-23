import smtplib
import time
 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
 
#Email Variables
SMTP_SERVER = 'smtp.gmail.com' #Email Server 
SMTP_PORT = 587 #Server Port 

#Gmail login details
gmail_username = 'smartberrypi2021@gmail.com' #change this to match your gmail account
gmail_password = '9907021405Aa'  #change this to match your gmail password

class Emailer:
    def sendMail(self, image):
        
        sendTo           = 'up898793@myport.ac.uk' 
        emailSubject     = "Person Detected!"
        emailContent     = "SmartBerryPi has detected a person at: " + time.ctime() + "." + " The security camera has started recording."
        
        #Create Headers
        emailData = MIMEMultipart()
        emailData['Subject'] = emailSubject
        emailData['To'] = sendTo
        emailData['From'] = gmail_username
 
        #Attach our text data  
        emailData.attach(MIMEText(emailContent))
   
        #Create our Image Data from the defined image
        imageData = MIMEImage(open(image, 'rb').read(), 'jpg') 
        imageData.add_header('Content-Disposition', 'attachment; filename="image.jpg"')
        emailData.attach(imageData)
  
        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
  
        #Login to Gmail
        session.login(gmail_username, gmail_password)
  
        #Send Email & Exit
        session.sendmail(gmail_username, sendTo, emailData.as_string())
        session.quit
 