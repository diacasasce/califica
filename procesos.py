from califica import Califica 
from fs import listFolder,checkFolder
import os
import requests # Para las llamadas GET y Post
from time import sleep
import datetime
import pyautogui
import psutil
import threading

def send(idp,ide,res,retry=0):
	try:
		##Realiza la llamada POST - trae los datos de la prueba
		#idp="1" #id de la prueba
		#ide="1020777040" #cedula del estudiante
		#res="1,2,3,4,0,0,0,0" #Respuestas leidas
		url = "http://www.gec.zigmadatos.com/academico/enviar.php"
		args = {'prueba':idp,'estudiante':ide,'respuestas':res}
		response = requests.get(url,params=args)
		print (response.url)
		#print("Codigo de respuesta recibido: "+response.status_code) 
		if response.status_code == 200:
			prueba_json = response.json()
			print(prueba_json)
		print("Listo")
	except :
		if retry <1:
			print("error de conexion")
			send(idp,ide,res,retry+1)
		else:
			print(str(idp)+"-"+str(ide)+" se reintento "+str(retry)+" veces")
			print("error de conexion")

def calificaFolder(folder,baseDir='./',envia=False):
	sleep(10)
	f = open("registro.txt", "a")		
	print(datetime.datetime.now())
	checkFolder(baseDir)
	lst=listFolder(folder,".jpg")
	while len(lst)<1:
		lst=listFolder(folder,".jpg")	
	#th=(100,170,210)
	th=(100,50,230)
	sleep(2)
	while len(lst)>0:
		sleep(1)
		#print(lst[0])
		file_name=folder+lst[0]
		idp,ide,res=Califica(file_name,th,baseDir)
		if envia:
			send(idp,ide,res)
		else:
			f.write(str(idp)+','+str(ide)+','+str(res)+'\r\n') 
			print(idp,ide,res)
		#if ide!='':
			#print(lst[0])
		lst=listFolder(folder,".jpg")
		#print(lst)
	print(datetime.datetime.now())
	return True
#calificaFolder('origen/','origen/procesados/')
#proceso de scan

#x,y=pyautogui.position()
#print(x,y)
#pyautogui.click(224,62)
def scanAll():
	window = pyautogui.pygetwindow.getWindowsWithTitle("epson Scan 2")
	if not window:
		os.startfile("C:\Program Files (x86)\EPSON\Epson Scan 2\Core\es2launcher.exe")
		print('open epson')
		sleep(5)
	print('starting')
	focused= pyautogui.pygetwindow.getFocusedWindow()
	while focused.title!="Epson Scan 2":
		window = pyautogui.pygetwindow.getWindowsWithTitle("epson Scan 2")
		focused= pyautogui.pygetwindow.getFocusedWindow()
		#print(focused.title)
		if window:
			window[0].focus()
	opn=0
	pyautogui.typewrite(["enter"])
	print('wait proceso')
	while opn<1:
		window = pyautogui.pygetwindow.getWindowsWithTitle("En proceso")
		window1 = pyautogui.pygetwindow.getWindowsWithTitle("Modo de alimentación automática")
		focused= pyautogui.pygetwindow.getFocusedWindow()
		#print('wait proceso ->',focused.title,opn)
		if window:
			window[0].focus()
			opn=len(window)
		elif window1:
			window1[0].focus()
			opn=len(window1)
	print('en proceso')
	while focused.title!="En proceso":
		window = pyautogui.pygetwindow.getWindowsWithTitle("En proceso")
		focused= pyautogui.pygetwindow.getFocusedWindow()
		#print('En proceso -->',focused.title)
		if window:
			window[0].focus()
	## se mantiene en proceso
	print('stay proceso')
	opn=2
	while opn>0:
		try:
			window = pyautogui.pygetwindow.getWindowsWithTitle("En proceso")
			focused= pyautogui.pygetwindow.getFocusedWindow()
			#print('stay proceso ->',focused.title,opn)
			opn=len(window)
			if window:
				
					window[0].focus()
		except:
			print('except procesos')
	print('wait for MODO')
	sleep(1)
	print('finish')
	while focused.title!="Modo de alimentación automática":
		window = pyautogui.pygetwindow.getWindowsWithTitle("Modo de alimentación automática")
		focused= pyautogui.pygetwindow.getFocusedWindow()
		#print('automatico -->',focused.title)
		if window:
			window[0].focus()
	opn=2
	while opn>0:
		pyautogui.typewrite(["enter"])
		window = pyautogui.pygetwindow.getWindowsWithTitle("Modo de alimentación automática")
		focused= pyautogui.pygetwindow.getFocusedWindow()
		if window:
			window[0].focus()
		#print('wait automatico ->',focused.title,opn)
		opn=len(window)

	sleep(2)
	pyautogui.hotkey("alt","f4")
	pyautogui.hotkey("alt","f4")
	
	while focused.title!="Epson Scan 2":
		window = pyautogui.pygetwindow.getWindowsWithTitle("epson Scan 2")
		focused= pyautogui.pygetwindow.getFocusedWindow()
		#print(focused.title)
		if window:
			window[0].focus()
			pyautogui.hotkey("alt","f4")
	return True
	

#print(scanAll())
#calificaFolder('origen/','origen/procesados/',True)
#th=(100,170,210)
#idp,ide,res=Califica('origen/pic0001.jpg',th,'origen/procesados/')
#print((idp,ide,res))

