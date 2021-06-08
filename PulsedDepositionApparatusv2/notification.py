import smtplib
import time
import datetime
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

 
def send_notification(title, message, cc):
    msg = MIMEMultipart()
    msg['Subject'] = title
    msg['From'] = 'illya.nayshevsky@gmail.com'
    
    msg['To'] = 'condensationtestsCSICUNY@gmail.com'
    sendto = ['condensationtestsCSICUNY@gmail.com']+[cc]


    text = MIMEText(message)
    msg.attach(text)

    s = smtplib.SMTP('smtp.gmail.com',587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('illya.nayshevsky@gmail.com','tkaqtllgvmpvdbwo')
    s.sendmail('illya.nayshevsky@gmail.com',sendto,msg.as_string())
    s.quit()
    
    print(" - - - ")
    print("Email Notification Sent")
    print(" - - - ")
