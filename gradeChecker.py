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


#fonction qui envoie un mail
def sendGrade(mat="Pas de nouvelle note",note=""):
    if note == "" :
        de = "GradeChecker <"+INSAuser+"@insa-rennes.fr>"
        pour = INSAuser+"@insa-rennes.fr"        
        mail = MIMEText("tristesse")
        mail['Subject'] = mat
        mail['From'] = de
        mail['To'] = pour
    else :
        de = "GradeChecker <"+INSAuser+"@insa-rennes.fr>"
        pour = INSAuser+"@insa-rennes.fr"        
        mail = MIMEText("Nouvelle note !!\n>"+mat+", avec un 'beau' "+str(note)+"\nFélicitations !")
        mail['Subject'] = mat+" : "+str(note)
        mail['From'] = de
        mail['To'] = pour
    username = INSAuser+"@insa-rennes.fr" # votre login ici
    password = INSApassword # votre password ici
    smtp = smtplib.SMTP('mailhost.insa-rennes.fr:587')
    smtp.starttls()
    smtp.login(username,password)
    smtp.sendmail(de, [pour], mail.as_string())
    smtp.close()
    print ("********************\n* Message envoyé ! *\n********************\n")


#fonction qui retourne un string, sans les éventuels accents
def deleteAccent(mstr):
    accent = ['é', 'è', 'ê', 'à', 'ù', 'û', 'ç', 'ô', 'î', 'ï', 'â']
    sans_accent = ['e', 'e', 'e', 'a', 'u', 'u', 'c', 'o', 'i', 'i', 'a']
    for i in range(len(accent)):
        mstr = mstr.replace(accent[i], sans_accent[i])
    return mstr

# identification et teste de validité des valeurs rentrées par l'utilisateur
print("Merci de renseigner vos logins INSA.")

#user
formatUserIncorrect = True
while True:
    if formatUserIncorrect :
        INSAuser = input("user : ")
        formatUserIncorrect = not re.match("^[a-zA-Z]*\.*[a-zA-Z]*$",INSAuser)
        if formatUserIncorrect :
            print ("> format user incorrect. Merci de réessayer.")
    else :
        break

#password
INSApassword = getpass.getpass("password : ")

#wainting time (in minutes)
formatIntervalleIncorrect = True
while True:
    intervalle = input("intervalle de verification (en minutes) : ")
    try:
        int(intervalle)
        formatIntervalleIncorrect=False
        break
    except ValueError:
        print("Entrez un nombre entier.")

# creation du fichier grades.txt si besoin
f=open("grades.txt","a")
f.close()
    
# main
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
    a = browser.submit_form(signup_form)

    # break si, après identification, on se retrouve sur la page d'erreur
    if browser.find_all(class_="errors") :
        print("Mauvais identifiant ou Mot de Passe.")
        break

    # recuperation des notes et noms des matières
    resHtml = browser.find_all(class_="fl-tab-content")
    tabGrades = re.findall("[\d,]*\s/\s20",str(resHtml))
    tabMatieres = re.findall("left\">.*\-\s(.*)\s:",str(resHtml))
    for i in range(len(tabGrades)):
        tempFile.write(tabMatieres[i]+" : "+ tabGrades[i] +"\n")
    tempFile.close()

    # cas ou le fichier grades.txt est vide, i.e la premiere execution du script sur cet ordinateur
    nbLinesGrades = sum(1 for _ in fileGrades)
    if nbLinesGrades < 2 :
        print ('first writting')
        fileGrades.close()
        fileGrades = open('grades.txt','w')
        for j in range(len(tabGrades)):
            fileGrades.write(tabMatieres[j]+" : "+ tabGrades[j] +"\n")
        fileGrades.close()
        os.remove('tempgrades.txt')
        print('done at '+str(datetime.datetime.now())+'\n\n')
        t.sleep(int(intervalle)*60)
        continue


    # cas ou le fichier n'etait pas vide
    # comparaison du fichier temporaire (données à jour) avec le fichier sur l'ordinateur
    fileGrades = open('grades.txt','r')
    tempFile = open('tempgrades.txt','r')
    lines1=fileGrades.readlines()
    lines2=tempFile.readlines()
    for i in range(len(lines2)):
        if lines1[i] != lines2[i] :
            newGrade = True
            print ('nouvelle note >> '+lines2[i])
            newmatiere = re.findall("(.*):",lines2[i])
            newnote = re.findall("[\d,]*\s/\s20",lines2[i])
            newmatiere[0] = deleteAccent(newmatiere[0])
            sendGrade(newmatiere[0],newnote[0])

            # maj du fichier de notes local
            fileGrades.close()
            fileGrades = open('grades.txt','w')
            for j in range(len(tabGrades)):
                fileGrades.write(tabMatieres[j]+" : "+ tabGrades[j] +"\n")

    if not newGrade :
        print ('pas de nouvelle note')
        
    print('done at '+str(datetime.datetime.now())+'\n\n')

    #clearing
    os.remove('tempgrades.txt')
    tempFile.close()
    fileGrades.close()

    t.sleep(int(intervalle)*60)