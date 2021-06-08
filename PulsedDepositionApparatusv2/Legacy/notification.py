import smtplib
import time
import datetime
from email.mime.text import MIMEText
 
def send_notification(experiment):
   
   
    content = ("Experiment Complete")
    msg = MIMEText("""Soiling experiment is complete.""")
    sender = 'illya.nayshevsky@gmail.com'
    recipients = ['illya.nayshevsky@gmail.com']
    msg['Subject'] = "Experiment Complete on: "+str(datetime.datetime.now())
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login('illya.nayshevsky@gmail.com','tkaqtllgvmpvdbwo')
    mail.sendmail('illya.nayshevsky@gmail.com','illya.nayshevsky@gmail.com',msg.as_string()) 
    mail.close()
    print("Sent")
