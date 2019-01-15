#!/usr/bin/env python3

import smtplib

"""
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("tangimds@gmail.com", "Showtime8/g")
 
msg = "coucou c'est moi !!"
server.sendmail("tangimds@gmail.com", "tangimds@gmail.com", msg)
server.quit()
print("message sent")
"""


"""
fromaddr = "tangimds@gmail.com"
toaddr = "tangimds@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Nouvelle NOTE"
 
body = "wallah ya une nouvelle note"
msg.attach(MIMEText(body, 'plain'))
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "Showtime8/g")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
"""


"""
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("tangimds@gmail.com", "Showtime8/g")
def test():
    

    fromaddr = 'tangimds@gmail.com'
    toaddrs = ['tangimds@gmail.com'] # On peut mettre autant d'adresses que l'on souhaite
    sujet = "Un Mail avec Python"
    message = u""\
    Velit morbi ultrices magna integer.
    Metus netus nascetur amet cum viverra ve cum.
    Curae fusce condimentum interdum felis sit risus.
    Proin class condimentum praesent hendrer
    it donec odio facilisi sit.
    Etiam massa tempus scelerisque curae habitasse vestibulum arcu metus iaculis hac.
    "
    msg = "\
    From: %s\r\n\
    To: %s\r\n\
    Subject: %s\r\n\
    \r\n\
    %s
    " % (fromaddr, ", ".join(toaddrs), sujet, message)
    try:
        server.sendmail(fromaddr, toaddrs, msg)
    except smtplib.SMTPException as e:
        print(e)
    # {} # Réponse du serveur
    server.quit()

test()
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def envoyer(mat="none",note=0):
    de = "tangimds@gmail.com"
    pour = "tangimds@gmail.com"
    mail = MIMEText("Nouvelle note")
    mail['From'] = de
    mail['Subject'] = mat +" : "+note
    mail['To'] = pour
    username = 'tangimds@gmail.com' # votre login ici
    password = 'Showtime8/g' # votre password ici
    smtp = smtplib.SMTP('smtp.gmail.com:587')
    smtp.starttls()
    smtp.login(username,password)
    smtp.sendmail(de, [pour], mail.as_string())
    smtp.close()
    print ("Message envoyé !")

envoyer()