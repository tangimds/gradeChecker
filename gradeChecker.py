#!/usr/bin/env python3

from robobrowser import RoboBrowser
import re
import filecmp
import os
import smtplib
import unicodedata
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time as t
import getpass
import datetime

#gérer la mauvaise connection ?

formatUserIncorrect = True
while True:
    if formatUserIncorrect :
        INSAuser = input("user : ")
        formatUserIncorrect = not re.match("^[a-zA-Z]*\.*[a-zA-Z]*$",INSAuser)
        if formatUserIncorrect :
            print ("> format user incorrect. Merci de réessayer.")
    else :
        break
INSApassword = getpass.getpass("mdp : ")


def sendGrade(mat="Pas de nouvelle note",note=""):
    if note == "" :
        de = "GradeChecker <tangimds@gmail.com>"
        pour = INSAuser+"@insa-rennes.fr"        
        mail = MIMEText("tristesse")
        mail['Subject'] = mat
        mail['From'] = de
        mail['To'] = pour
    else :
        de = "GradeChecker <tangimds@gmail.com>"
        pour = INSAuser+"@insa-rennes.fr"        
        mail = MIMEText("Nouvelle note !!\n>"+mat+", avec un 'beau' "+str(note)+"\nFélicitations !")
        mail['Subject'] = mat+" : "+str(note)
        mail['From'] = de
        mail['To'] = pour
    username = 'tangimds@gmail.com' # votre login ici
    password = 'Showtime8/g' # votre password ici
    smtp = smtplib.SMTP('smtp.gmail.com:587')
    smtp.starttls()
    smtp.login(username,password)
    smtp.sendmail(de, [pour], mail.as_string())
    smtp.close()
    print ("********************\n* Message envoyé ! *\n********************")


def deleteAccent(mstr):
    accent = ['é', 'è', 'ê', 'à', 'ù', 'û', 'ç', 'ô', 'î', 'ï', 'â']
    sans_accent = ['e', 'e', 'e', 'a', 'u', 'u', 'c', 'o', 'i', 'i', 'a']
    for i in range(len(accent)):
        mstr = mstr.replace(accent[i], sans_accent[i])
    return mstr



while True:
    newGrade = False
    fileGrades = open('grades.txt','r')
    tempFile = open('tempgrades.txt','w')
    browser = RoboBrowser()
    browser.open('https://ent.insa-rennes.fr/uPortal/f/infosperso/p/dossierAdmEtu.u18l1n17/max/render.uP?pCp#portlet-DossierAdmEtu-tab2')


    # Get the signup form
    signup_form = browser.get_form()

    # Fill it out
    signup_form['username'].value = INSAuser
    signup_form['password'].value = INSApassword

    # Submit the form
    browser.submit_form(signup_form)
    #print('> form submit DONE')

    resHtml = browser.find_all(class_="fl-tab-content")
    tabGrades = re.findall("[\d,]*\s/\s20",str(resHtml))
    tabMatieres = re.findall("left\">.*\-\s(.*)\s:",str(resHtml))
    for i in range(len(tabGrades)):
        tempFile.write(tabMatieres[i]+" : "+ tabGrades[i] +"\n")
    tempFile.close()
    #print('> all grades fetched')

    tempFile = open('tempgrades.txt','r')
    lines1=fileGrades.readlines()
    lines2=tempFile.readlines()
    for i in range(len(lines2)):
        if len(lines1)<2 or lines1[i] != lines2[i] :
            newGrade = True
            print ('nouvelle note >> '+lines2[i])
            # envoyer mail avec note et matiere
            #print(lines2[i])
            newmatiere = re.findall("(.*):",lines2[i])
            newnote = re.findall(":(.*)",lines2[i])
            newmatiere[0] = deleteAccent(newmatiere[0])
            #print("mat : ",newmatiere)
            #print("note : ",newnote)
            sendGrade(newmatiere[0],newnote[0])
            fileGrades.close()
            fileGrades = open('grades.txt','w')
            for j in range(len(tabGrades)):
                fileGrades.write(tabMatieres[j]+" : "+ tabGrades[j] +"\n")

    if not newGrade :
        print ('pas de nouvelle note')
        sendGrade()    
        
    print('done at '+str(datetime.datetime.now())+'\n\n')

    #clearing
    os.remove('tempgrades.txt')
    tempFile.close()
    fileGrades.close()

    t.sleep(7200)


# version fonctionnel avec twitter
"""
from robobrowser import RoboBrowser

browser = RoboBrowser()
browser.open('http://twitter.com/login')

# Get the signup form
signup_form = browser.get_form(class_='signin')
#signup_form         # <RoboForm user[name]=, user[email]=, ...
print('get form ...')

# Inspect its values
print('authenticity_token : ',signup_form['authenticity_token'].value)

# Fill it out
signup_form['session[username_or_email]'].value = 'tangimds'
signup_form['session[password]'].value = '6KyY$o7&B7GN'

# Submit the form
#browser.submit_form(signup_form)
print('form submit DONE')

res = browser.find(class_="text-input")
print('res : ', res)
"""

"""
if filecmp.cmp("grades.txt","gradesDirty.txt"):
    print ("Pas de nouvelles notes")
else :
    fileGrades.close()
    fileGrades = open('grades.txt','w')
    for i in range(len(tabGrades)):
        fileGrades.write(tabMatieres[i]+" : "+ tabGrades[i] +"\n")

    # envoyer email

    print ("nouvelle note")

"""