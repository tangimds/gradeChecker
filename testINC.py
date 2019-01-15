#!/usr/bin/env python3
import time as t
import getpass

user = input("user : ")
password = getpass.getpass("mdp : ")

print(user)
print(password)

i=0
while True:
    print(i)
    i = i+1
    t.sleep(10)