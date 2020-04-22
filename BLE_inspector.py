import bluetooth
import smtplib, ssl
import datetime
import subprocess
import requests
import ipinfo
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
from ast import literal_eval


'''
BLE Inspector code 
TCSS 499 
Winter 2020
Gregory Gertsen 
'''

#Variable for counting number of scan cycles 
scanCount = 0
#Variable for output message to user
outMessage = {}

#Function returns the public IP as well as geolocation(latitude and longitude) of the machine running the code. 

def get_ip_latLon():
   
    #Gets public IP
    iP = requests.get('http://ip.42.pl/raw').text
   
    #Converts public IP to lat/lon
    handler = ipinfo.getHandler()
    ip_address = iP
    details = handler.getDetails(ip_address)
    details_text = str(details)
    Alist = details.loc.split(',')
    
    return (iP, Alist[0],Alist[1])


#Function for sending email message through gmail account
#Needs to be customized with sender and receiver email adresses + password

def send_email(the_message):

### STEP 2 - CHANGE THE SENDER_EMAIL, RECEIVER_EMAIL, AND PASSWORD VALUES. THESE ARE STRING VALUES  ####
### CHANGE ON LINE 55,56,57. ###

    subject = "BLE Inspector message"
    body = f"This is an email from the BLE Inspector {outMessage}"
    sender_email = "insert gmail address"
    receiver_email = "insert gmail address"
    password = 'insert sender account password'

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)



#Function for sending telemetry data to ThingsBoard.io IoT cloud platform 

def thingsBoard(the_message):

   
    telemetry = the_message
    #Second value is the key
    client = TBDeviceMqttClient("demo.thingsboard.io", "kOH7QFm7nQXC7OicneLt")
    # Connect to ThingsBoard
    client.connect()
    # Sending telemetry without checking the delivery status
    client.send_telemetry(telemetry) 
    # Sending telemetry and checking the delivery status (QoS = 1 by default)
    result = client.send_telemetry(telemetry)
    # get is a blocking call that awaits delivery status  
    success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
    # Disconnect from ThingsBoard
    client.disconnect()



#Loop for running the BLE Inspector

while True:
    
    scanCount += 1

    # Scans for bluetooth devices in vicinity for desired duration in 20 second intervals
    #Returns a list of tuples, e.g. [(address)(device name)]
    parkScan = bluetooth.discover_devices(duration=20,lookup_names=True)
   
    # Parking Enforcement shows up as XXRAJ.
    # Insert name of whatever device you are scanning for, e.g. iPhone

    ### STEP 1 - CHANGE THE NAME OF THE DEVICE YOU ARE SCANNING FOR, USE YOUR CELL PHONE BLUETOOTH NAME FOR TESTING ###
    ### CURRENTLY USING 'iPhone', CHANGE BELOW IN TWO PLACES, LINE 114 and 124. ###

    if 'iPhone' in str(parkScan):
        print('Found')
        print(scanCount)
        print(parkScan)
        #Calls function to retrieve IP and lat, lon
        ipLat = get_ip_latLon()

        #Variable for returning only the desired Bluetooth device instead of all found.
        parkScanKeep = ""
        for names in parkScan:
            if 'iPhone' in names:
                parkScanKeep = names

        #The output message as a dictionary containing 'Time', 'IP', 'Latitude', 'Longitude', 'Bluetooth info'
        outMessage = {'Time':str(datetime.datetime.now().strftime("%H:%M:%S")),"IP":str(ipLat[0]),"Latitude":str(ipLat[1]),"Longitude":str(ipLat[2]),"Bluetooth":str(parkScanKeep)}
        print(outMessage)
       
        
        output = None
     

        try:
            #uncomment send_email once you have configured send_email function. 

            ### STEP 3 - UNCOMMENT OUT BELOW LINE ### 
            #send_email(outMessage)
            thingsBoard(outMessage)
            print(outMessage)
         
        except subprocess.CalledProcessError as e:
            output = e.output
             
        break
    
        
    else:
        print('Not Found')
        print(parkScan)
        



