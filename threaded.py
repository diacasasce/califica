import threading as thread
import procesos as pr
from time import sleep

scanned=False
while not scanned:
    scanned=pr.scanAll()
    pr.calificaFolder('origen/','origen/procesados/')

