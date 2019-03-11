import fs
import procesos as pr
from califica import Califica 
import os

envia=True
if input('desea enviar lo resultados a base de datos? Y/N').upper()!='Y':
    envia=False
folder=input(' ingrese nombre del folder ')
dir=fs.listFolder(folder,'.jpg')

if folder[-1]!='/':
        folder+='/'
for file in dir:
    name=folder+file
    th=(100,50,230)
    idp,ide,res=Califica(name,th,'./origen/procesados/')
    if envia:
        pr.send(idp,ide,res)
    else:
        print(idp,ide,res)