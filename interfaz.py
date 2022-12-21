from tkinter import Tk
import elementos as elm
import reconocimiento as rc
from fotos import *
from base import Base
from parametros import AumentarError,ReducirError,GetError
from modos import *

def Salir(event,destroy=False):
    global loop,base,ventana
    loop = False
    ventana = destroy
    base.Incompletos()
    rc.Salir()
    
def Ajustar(event,width):
    control.Ajustar(event)
    camara.Ajustar(width-200)


def Key(event):
    key = event.keysym

    if key=='q':
        Salir(None)
    elif key=='c':
        rc.Salir()
    elif key=='Up':
        ReducirError()
        print("Error",GetError())
        control.ActualizarError()
    elif key=='Down':
        AumentarError()
        print("Error",GetError())
        control.ActualizarError()

if __name__ == '__main__':
    base = Base()
    recon = rc.Reconocedor(base)

    root = Tk()

    root.title('Impostor')
    w, h = 1000,600
    xc = root.winfo_screenwidth()//2 - w//2
    yc = root.winfo_screenheight()//2 - h//2
    root.geometry(f"{w}x{h}+{xc}+{yc}")
    root.configure(padx=0,pady=0)
    root.bind('<Destroy>',Salir)
    root.bind('<Key>',Key)
    root.update()


    elm.Styles(root)
    control = elm.panelControl(root,base,recon)
    control.salir.configure(command= lambda: Salir(None,True))
    camara = elm.Camara(root)
    root.bind('<Configure>',lambda event: Ajustar(event,root.winfo_width()))
    root.update()


    loop = True
    barra = False
    ventana = True
    while loop:
        root.update()
        cam = recon.Captura()
        rostro = recon.Detecccion()
        if loop: camara.ActualizarImagen(cam)
        if not barra:
            if recon.modo==REGISTRO: 
                camara.ActivarBarra()
                barra = True
        else:
            if recon.count>0 and barra: 
                camara.ActualizarBarra(recon.count)
            if recon.modo!=REGISTRO: 
                camara.DesactivarBarra()
                barra = False
        if loop: control.ActualizarImagen(rostro)
        control.ActualizarModo(recon.modo)
    if ventana: root.destroy()