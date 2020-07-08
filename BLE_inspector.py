import bluetooth
import datetime
import smtplib, ssl
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



'''
BLE Inspector code 

'''

#Variable for counting number of scan cycles 
scanCount = 0
#Variable for output message to user
outMessage = {}

#Function for sending email message through gmail account
#Needs to be customized with sender and receiver email addresses + password

def send_email(the_message):

### CHANGE THE SENDER_EMAIL, RECEIVER_EMAIL, AND PASSWORD VALUES ####

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
    #message["Bcc"] = receiver_email  

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


#Loop for running the BLE Inspector

while True:
    
    scanCount += 1

    # Scans for bluetooth devices in vicinity for desired duration in 20 second intervals
    #Returns a list of tuples, e.g. [(address)(device name)]
    parkScan = bluetooth.discover_devices(duration=20,lookup_names=True)
   
    # Parking Enforcement shows up as 'XXRAJ' in my city.
    # Insert prefix of whatever device you are scanning for.

    ### CHANGE THE NAME OF THE DEVICE YOU ARE SCANNING FOR, USE YOUR CELL PHONE BLUETOOTH NAME FOR TESTING ###
    ### CURRENTLY USING 'iPhone', CHANGE BELOW IN TWO PLACES TO CUSTOMIZE ###

    if 'iPhone' in str(parkScan):
        print('Found')
        print(scanCount)
        print(parkScan)

        #Variable for returning only the desired Bluetooth device instead of all found.
        parkScanKeep = ""
        for names in parkScan:
            if 'iPhone' in names:
                parkScanKeep = names

        #The output message as a dictionary containing 'Time', 'Bluetooth info'
        outMessage = {'Time':str(datetime.datetime.now().strftime("%H:%M:%S")),"Bluetooth":str(parkScanKeep)}
        try:
            send_email(outMessage)
        except:
            print("Configure email")
            
        print(outMessage)
        break
     
    else:
        print('Not Found')
        print(parkScan)
        

