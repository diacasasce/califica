# Aplicacion completa hasta validad usuario y clave con marianitas
# Enero 17 de 2019

import procesos as pr
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk, font, messagebox
import requests # Para las llamadas GET y Post
import threading
from time import sleep


#from funciones.py import *
#pop up
def popupmsg(msg):
    NORM_FONT = ("Helvetica", 10)
    popup = tk.Tk()
    popup.iconbitmap("./img/zigma.ico")
    popup.wm_title("Finalizado")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

class Application(tk.Frame):

    permiso = "No"

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        #self.hi_there = tk.Button(self)
        #self.hi_there["text"] = "Hello World\n(click me)"
        #self.hi_there["command"] = self.say_hi
        #self.hi_there.pack(side="top")

        #self.entrar = tk.Button(self)
        #self.entrar["text"] = "Entrar"
        #self.entrar["command"] = self.Entrar
        #self.entrar.pack(side="top")

        #self.quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        #self.quit.pack(side="bottom")

        self.imgEnt = PhotoImage(file="./img/btEntrarp.png")
        self.imgSal = PhotoImage(file="./img/btSalirp.png")
        self.imgEsc = PhotoImage(file="./img/btEscanearp.png")

        self.btEntrar = tk.Button(root,command=self.Entrar,text='Entrar',width=100)
        self.btEntrar.place(x=300,y=300)
        self.btEntrar.config(image=self.imgEnt)

        self.btEscanear = tk.Button(root,command=lambda: self.Escanear("dato"),text='Escanear')
        self.btEscanear.place(x=420,y=300)
        self.btEscanear.config(image=self.imgEsc)
        ##self.btEscanear.config(state="disabled") ## Habilita el boton

        btSalir = tk.Button(root,command=self.Salir,text='Salir')
        btSalir.place(x=540,y=300)
        btSalir.config(image=self.imgSal)
        
    def say_hi(self):
        print("hi there, everyone!")

    def Salir(self):
        root.destroy()

    #def Escanear(self,dt):
    #    messagebox.showinfo("Escanear", "MessageBox "+dt) 
    #    print("Escaneando")
        
    def Validar(self,dt):
        usu = self.txt1.get()
        pas = self.txt2.get()
        nom = ""
        entra = "NO"
        
        #Realiza la llamada POST
        url = "http://www.gec.zigmadatos.com/academico/leer.php"
        args = {'usuario':usu,'clave':pas}
        response = requests.get(url,params=args)
        print (response.url)
        #print(response.status_code)        

        if response.status_code == 200:
            response_json = response.json()
            contenido = response.content
            print(response_json)
            #x = "0" in response_json 
            x=1
            if len(response_json) ==0:
                x= 0
            if x == 1:
                nom = response_json[0]["apellidos"] + response_json[0]["nombres"]
                entra="SI"
            else:
                print("Clave erronea")
                entra="NO"
        else:
            print("No hay conexión ")

            

        
        if entra=="NO":
            self.etiq3.config(foreground='red')
            self.etiq3.config(text="Usuario incorrecto "+ usu)
        else:
            self.etiq3.config(foreground='blue')
            self.etiq3.config(text="Bienvenido "+ nom)
            self.dialogo.destroy()
            self.btEscanear.config(state="normal")
        #print("hi there, everyone! " +dt )  


    def Entrar(self):
        self.dialogo = Toplevel()
        self.dialogo.withdraw()
        self.dialogo.title("Ingreso al sistema")
        self.dialogo.iconbitmap("zigma.ico")
        self.dialogo.geometry("403x253+300+250")
        self.dialogo.resizable(0,0)
        fondod=PhotoImage(file="./img/Fondo250-400.png")
        lblFondo=Label(self.dialogo,image=fondod).place(x=0,y=0) #fondo 
        self.dialogo.grab_set()
        self.dialogo.deiconify()

        #Usuario y clave
        etiq1 = Label(self.dialogo, text="Usuario: ",foreground='Black',font=("Arial", 15),background='#9ba8da')
        etiq1.place(x=40,y=60)
        etiq2 = Label(self.dialogo, text="Contraseña: ",foreground='Black',font=("Arial", 15),background='#9ba8da')
        etiq2.place(x=40,y=100)
        self.etiq3 = Label(self.dialogo,text="Ingrese usuario y contraseña ",foreground='Black',font=("Arial", 15),background='#9ba8da')
        self.etiq3.place(x=40,y=200)

        vartxt1 = StringVar()
        self.txt1 = Entry(self.dialogo,textvariable=vartxt1,font=("Arial", 15),width=15) #Campo para el nombre de usuario
        self.txt1.pack()
        self.txt1.place(x=155,y=62) #x=izq-derecha  y=arriba,abajo
        self.txt1.focus()

        vartxt2 = StringVar()
        self.txt2 = Entry(self.dialogo,textvariable=vartxt2,font=("Arial", 15),width=15,show="*") #Campor para la clave
        self.txt2.pack()
        self.txt2.place(x=155,y=102) #x=izq-derecha  y=arriba,abajo

        imgEnt2 = PhotoImage(file="./img/entrar5.png")
        btEntra = Button(self.dialogo,command=lambda:self.Validar("dato"),text='Entrar')
        btEntra.place(x=70,y=150)
        btEntra.config(image=imgEnt2)
    
        imgCan = PhotoImage(file="./img/cancelar.png")
        btCancela = Button(self.dialogo,command=self.dialogo.destroy,text='Entrar')
        btCancela.place(x=180,y=150)
        btCancela.config(image=imgCan)
        self.dialogo.bind('<Return>', (lambda e, btEntra=btEntra: btEntra.invoke())) # b is your button
        self.wait_window(self.dialogo)
    def califica(self):
        done=False
        while not done:
            done=pr.calificaFolder('origen/','origen/procesados/',True)
        popupmsg(' Se han procesado todas las pruebas')
    def Escanear(self,dt):
        th1 = threading.Thread(target=self.califica, name='califica')
        th1.start()
        th2 = threading.Thread(target=pr.scanAll, name='scanner')
        th2.start()
        
    def EscanearOK(self,dt):
        #Muestra la ventana para ingresar codigo de prueba y escanear
        self.dialogo = Toplevel()
        self.dialogo.withdraw()
        self.dialogo.title("Escanear respuestas")
        self.dialogo.iconbitmap("zigma.ico")
        self.dialogo.geometry("603x423+120+120")
        self.dialogo.resizable(0,0)
        fondod=PhotoImage(file="./img/Fondo420-600.png")
        lblFondo=Label(self.dialogo,image=fondod).place(x=0,y=0) #fondo 
        self.dialogo.grab_set()
        self.dialogo.deiconify()

        #Usuario y clave
        etiq1 = Label(self.dialogo, text="Codigo de la prueba: ",foreground='Black',font=("Arial", 15),background='#9ba8da')
        etiq1.place(x=40,y=60)
        etiq2 = Label(self.dialogo, text="Datos de la prueba: ",foreground='red',font=("Arial 12 bold"),background='#9ba8da')
        etiq2.place(x=40,y=100)
        self.etiq2a = Label(self.dialogo, text="",foreground='green',font=("Arial 12 bold"),background='#9ba8da')
        self.etiq2a.place(x=200,y=100)
        self.etiq3 = Label(self.dialogo,text="Intitución: ",foreground='Black',font=("Arial 12 bold"),background='#9ba8da')
        self.etiq3.place(x=40,y=130)
        self.etiq3a = Label(self.dialogo,text="",foreground='Green',font=("Arial 12 bold"),background='#9ba8da')
        self.etiq3a.place(x=220,y=130)
        self.etiq4 = Label(self.dialogo,text="Fecha de aplicación : ",foreground='Black',font=("Arial 12 bold"),background='#9ba8da')
        self.etiq4.place(x=40,y=160)
        self.etiq4a = Label(self.dialogo,text="",foreground='Green',font=("Arial 12 bold"),background='#9ba8da')
        self.etiq4a.place(x=220,y=160)
        self.etiq5 = Label(self.dialogo,text="Detalle : ",foreground='Black',font=("Arial 12 bold"),background='#9ba8da')
        self.etiq5.place(x=40,y=190)
        self.etiq5a = Label(self.dialogo,text="",foreground='Green',font=("Arial 12 bold"),background='#9ba8da')
        self.etiq5a.place(x=220,y=190)
        self.etiq6 = Label(self.dialogo,text="Número de preguntas: ",foreground='Black',font=("Arial 12 bold"),background='#9ba8da')
        self.etiq6.place(x=40,y=220)
        self.etiq6a = Label(self.dialogo,text="",foreground='Green',font=("Arial 12 bold"),background='#9ba8da')
        self.etiq6a.place(x=220,y=220)
        self.varCodp = StringVar()
        self.codp = Entry(self.dialogo,textvariable=self.varCodp,font=("Arial", 15),width=15) #Campo para el nombre de usuario
        self.codp.pack()
        self.codp.place(x=250,y=62) #x=izq-derecha  y=arriba,abajo
        self.codp.focus()

        
        imgEnt3 = PhotoImage(file="./img/btConsultar.png")
        btEntra = Button(self.dialogo,command=lambda:self.Consultap("dato"),text='Consultar')
        btEntra.place(x=430,y=56)
        btEntra.config(image=imgEnt3)
        self.dialogo.bind('<Return>', (lambda e, btEntra=btEntra: btEntra.invoke())) # Boton por defecto
    
        imgEsc = PhotoImage(file="./img/btEscanear.png")
        btEscanea = Button(self.dialogo,command=lambda:self.Escanea("codigodePrueba"),text='Escanea')
        btEscanea.place(x=180,y=350)
        btEscanea.config(image=imgEsc)        
        #self.wait_window(self.dialogo)

        imgCan = PhotoImage(file="./img/btRegresar.png")
        btCancela = Button(self.dialogo,command=self.dialogo.destroy,text='Cancela')
        btCancela.place(x=300,y=350)
        btCancela.config(image=imgCan)
        #self.dialogo.bind('<Return>', (lambda e, btCancela=btCancela: btCancela.invoke()) # b is your button
        self.wait_window(self.dialogo)

    def Escanea(self,dt):
        #Ejecuta el proceso de escanear documento
        codip = self.codp.get()
        if codip =="":
            messagebox.showinfo("Escanear", "Ingrese primero el codigo de la prueba "+codip) 
        else:
            print("Escaneando prueba: " + codip + "  Id de la prueba: "+self.idprueba)
            print(self.prueba_json) 


    def Consultap(self,dt):
        #Invocado desde escanear, para verificar los datos de la prueba
        codip = self.codp.get()
        if codip =="":
            messagebox.showinfo("Escanear", "Ingrese primero el código de la prueba "+codip) 
        else:        
            print("Consultando datos de la prueba")
            #Realiza la llamada POST
            url = "http://www.gec.zigmadatos.com/academico/consultap.php"
            args = {'prueba':codip}
            response = requests.get(url,params=args)
            print (response.url)
            #print(response.status_code)        

            if response.status_code == 200:
                response_json = response.json()
                contenido = response.content
                print(response_json)
                #x = "0" in response_json 
                x=1
                if len(response_json) ==0: #Verifica si el json tiene elementos
                    x=0
                if x == 1:
                    idp = response_json[0]["id"]                    
                    ins = response_json[0]["nombre"]
                    fec = response_json[0]["fecha"]
                    det = response_json[0]["detalle"]
                    pre = response_json[0]["preguntas"]
                    #print("Tipo de variable "+type(idp).__name__) ## Tipo de naviable NULL o NoneType
                    if type(idp).__name__ != "NoneType" :
                        self.etiq2a.config(text = "")
                        self.etiq3a.config(text = ins)
                        self.etiq4a.config(text = fec)
                        self.etiq5a.config(text = det)
                        self.etiq6a.config(text = pre)
                        self.respuesta = response_json
                        #Trae la configuracion de la prueba
                        #Realiza la llamada POST - trae los datos de la prueba
                        url = "http://www.gec.zigmadatos.com/academico/datosp.php"
                        args = {'prueba':idp}
                        response = requests.get(url,params=args)
                        #print (response.url)
                        #print("Codigo de respuesta recibido: "+response.status_code) 
                        if response.status_code == 200:
                            self.prueba_json = response.json()
                            self.idprueba = idp
                            #print(prueba_json)
                    else:
                        self.etiq2a.config(text = "Prueba Inexistente: " + codip )
                        self.etiq3a.config(text = "")
                        self.etiq4a.config(text = "")
                        self.etiq5a.config(text = "")
                        self.etiq6a.config(text = "")
                        self.varCodp.set("")
                        #self.codp.insert(0, "x")
                        #self.codp = ""
                else:
                    print("No existe la prueba")
                    entra="NO"
            else:
                print("No hay conexión ")


root = tk.Tk()
root.title('Calificación de examenes tipo Icfes')
root.geometry('803x603+10+10')
root.iconbitmap("./img/zigma.ico")
fondo=PhotoImage(file="./img/fondo.png")
lblFondo=Label(root,image=fondo).place(x=0,y=0) #fondo 

app = Application(master=root)
app.mainloop()
