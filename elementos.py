from tkinter import Tk, Toplevel,Canvas,messagebox, Event
from tkinter.ttk import Label,Frame,Style,Entry,Combobox,Button
from PIL import Image, ImageTk
from fotos import *
from base import Base
from parametros import *
from colores import *
from cv2 import cvtColor, resize, COLOR_BGR2RGB
from base import Base
from reconocimiento import Reconocedor

def Styles(padre) -> None:
    style = Style()

    style.theme_use("alt")

    style.configure('Camara.TFrame', background=fondoCam)
    style.configure('Imagen.TLabel', background=fondoCam)

    style.configure('TFrame.TLabel', background=fondoCon, foreground=font, font=('Arial',16))
    style.configure('Frame.TLabel', background=high)

    style.configure('Control.TFrame', background=fondoCon)
   
    style.configure('Botones.TFrame', background=fondoCon)
    
    style.configure('Botones.TButton', background=high,foreground=font,focuscolor='none')
    style.map('Botones.TButton',
                background= [('pressed',highpress),('active',highover),('disabled',highdesc)],
                foreground= [('disabled',fontdesc)]
    )

    style.configure('TFide.TLabel', background=fondoCon, foreground=font, font=('Arial',18))
    style.configure('TModo.TLabel', background=fondoCon, foreground=font, font=('Arial',12))

    padre.option_add('*TCombobox*Listbox*Background', fondoCon)
    padre.option_add('*TCombobox*Listbox*Foreground', font)
    padre.option_add('*TCombobox*Listbox*selectBackground', high)
    padre.option_add('*TCombobox*Listbox*selectForeground', font)
    style.configure('Form.TCombobox',foreground=font)
    style.map('Form.TCombobox', 
            fieldbackground=[('readonly',fondoCon)],
            selectbackground=[('readonly', fondoCon)],
            background=[('readonly', high)],
            )
    
class imagen():
    def __init__(self,url:str,widht,height) -> None:
        
        self.Establecer(widht=widht,height=height)

    def Establecer(self,url:str=NO,widht=0,height=0) -> ImageTk:
        try:
            foto = Image.open(url)
        except:
            foto = Image.open(NO)
        finally:
            self.foto = foto.resize((widht,height),Image.ANTIALIAS)
            self.imagen = ImageTk.PhotoImage(self.foto)

    def EstablecerArray(self,array,widht,height):
        try:
            array = cvtColor(array,COLOR_BGR2RGB)
            array = resize(array,(widht,height))
            self.foto = Image.fromarray(array)
        except:
            pass
        else:
            self.imagen = ImageTk.PhotoImage(self.foto)

    def Redimensionar(self,width,height):
        self.foto = self.foto.resize((width,height),Image.ANTIALIAS)
        self.imagen = ImageTk.PhotoImage(self.foto)

class Camara(Frame):
    def __init__(self, padre:Tk) -> None:
        self.modo = ""
        self.foto = None
        super().__init__(padre,style='Camara.TFrame')  
        self.pack(side='left', fill='y',expand=True)
        self.bind('<Configure>',self.CentrarImagen)
        
        self.canvas = Canvas(self,width=600, height=20, background="white")
        self.canvas.create_rectangle(0,0,0,20,fill=high)
        self.canvas.create_text(15,10,text="0%",fill=fondoCon)
        
        self.update()
        self.relacion = 500/self.winfo_height()
        self.foto = imagen(NO,padre.winfo_width()-200,self.winfo_height())
        self.imagen = Label(self,image=self.foto.imagen,style='Imagen.TLabel')
        self.imagen.pack()
        self.update()
        self.CentrarImagen(None)

    def Ajustar(self,width):
        self.configure(width=width)

    def CentrarImagen(self,event:Event) -> None:
        if self.foto == None : return
        self.update()
        self.foto.Redimensionar(self.winfo_width(),int(self.winfo_height() * self.relacion))
        self.imagen.configure(image=self.foto.imagen)
        self.imagen.update()

        wi = self.winfo_width()//2 - self.imagen.winfo_width()//2
        hi = self.winfo_height()//2 - self.imagen.winfo_height()//2
        self.imagen.place(y=hi,x=wi)

    def ActualizarImagen(self,cam) -> None:
        self.update()
        try:
            self.foto.EstablecerArray(cam,self.winfo_width(),int(self.winfo_height()*self.relacion))
        except:
            self.foto.EstablecerArray(widht=self.winfo_width(),height=int(self.winfo_height()*self.relacion))

        self.imagen.configure(image=self.foto.imagen)

    def ActualizarBarra(self,num:int):
        porc = num/NFOTOS
        self.canvas.delete("all")
        x,y = self.canvas.winfo_width()*porc,20
        self.canvas.create_rectangle(0,0,x,y,fill=high)
        color = fondoCon
        if x>10: color = font
        self.canvas.create_text(15,10,text=f"{int(porc*100)}%",fil=color)
    
    def ActivarBarra(self):
        self.canvas.pack(side='top',pady=10)

    def DesactivarBarra(self):
        self.canvas.pack_forget()
        
         
class panelControl(Frame):
    def __init__(self, padre:Tk,base:Base,recon:Reconocedor) -> None:
        super().__init__(padre,style='Control.TFrame',width=200)
        self.pack(side='right',fill='y')
        self.pack_propagate(False)
        self.update()

        padiy = 10

        self.foto = imagen(NO,100,100)
        self.captura = Label(self,image=self.foto.imagen,style='Frame.TLabel',border=10)
        self.captura.pack(side='top')
        self.capText = Label(self,text='Ultimo rostro:',style='TFrame.TLabel')
        self.capText.pack(before=self.captura,pady=padiy)
        
        self.panelbotones = Frame(self,style='Botones.TFrame',width=100,height=100)
        self.panelbotones.pack(pady=20)

        self.botones = []
        self.registro = Button(self.panelbotones,
                                text='Resgistrar',
                                command= lambda: self.NuevoPanel(padre,panelRegistro,'Registrar',recon.Resgistrar),
                                style='Botones.TButton'
                                )
        self.registro.pack(pady=padiy)
        self.botones.append(self.registro)

        self.agregar = Button(self.panelbotones,
                                text='Agregar fotos',
                                command= lambda: self.NuevoPanel(padre,panelAgregar,'Agregar fotos',recon.SetID,base.ObtenerNombres),
                                style='Botones.TButton'
                                )
        self.agregar.pack(pady=padiy)
        self.botones.append(self.agregar)

        self.eliminar  = Button(self.panelbotones,
                                text='Eliminar',
                                command= lambda: self.NuevoPanel(padre,panelEliminar,"Eliminar",base.BorrarAlumno,base.BorrarFotos,base.ObtenerNombres,recon.Entrenar),
                                style='Botones.TButton'
                                )
        self.eliminar.pack(pady=padiy)
        self.botones.append(self.eliminar)

        self.entrenar = Button(self.panelbotones,
                                text='Entrenar',
                                command= lambda: recon.Entrenar(),
                                style='Botones.TButton'
                                )
        self.entrenar.pack(pady=padiy)
        self.botones.append(self.entrenar)       

        self.error = Label(self.panelbotones,
                        text=f"Parentesco: {100-ERROR}%",
                        style='TFide.TLabel')
        self.error.pack(pady=padiy*1.5)

        self.modo = Label(self.panelbotones,
                        text=f"Modo: reconocimiento",
                        style='TModo.TLabel')
        self.modo.pack(pady=padiy*1.5)
        
        self.panelbotones.update()
        xc= self.winfo_width()//2 - self.panelbotones.winfo_width()//2
        yc= self.winfo_height()//2 - self.panelbotones.winfo_height()//2
        self.panelbotones.place(x=xc,y=yc+padiy*2)

        self.salir = Button(self,
                            text='Salir',
                            style='Botones.TButton'
                            )
        self.salir.pack(side='bottom',pady=padiy)
        self.botones.append(self.salir)
        
        self.config(width=200)

    def Ajustar(self,event:Event):
        self.configure(height=event.height)

    def ActualizarImagen(self,rostro) -> None:
        self.foto.EstablecerArray(rostro,100,100)
        self.captura.configure(image=self.foto.imagen)

    def ActualizarError(self):
        self.error.configure(text=f"Parentesco: {100-GetError()}%")

    def ActualizarModo(self,modo:str):
        self.modo.configure(text=f"Modo: {modo}")

    def NuevoPanel(self,padre:Tk,panel,nombre:str,*funcs):
        panel(padre,nombre,self.botones,*funcs)
        self.DesactivarBotones()

    def DesactivarBotones(self):
        for boton in self.botones:
            boton.configure(state="disable")

class panelEmergente(Toplevel):
    def __init__(self, padre:Tk,titulo:str,lbotones:list) -> None:
        super().__init__(padre,background=fondoCon)
        self.title(titulo) 
        w, h = 300,130
        self.attributes('-topmost', 'true')

        self.bind('<Key>',lambda event: self.Esc(event,lbotones))
        self.bind('<Destroy>', lambda event: self.Terminar(lbotones))


        cartel = Label(self,text="Nombre",style='TFrame.TLabel')
        cartel.grid(row=0,column=0,pady=10)

        self.aceptar = Button(self,text='Aceptar',style='Botones.TButton')
        self.aceptar.grid(row=1,column=0,rowspan=2,sticky='we',padx=20,pady=10)

        self.cancel = Button(self,text='Cancelar',command=lambda: self.Terminar(lbotones),style='Botones.TButton')
        self.cancel.grid(row=1,column=2,rowspan=2,sticky='we',padx=20,pady=10)

    def Centrar(self,padre):
        padre.update()
        self.update()
        xc = (padre.winfo_screenwidth()//2) - (self.winfo_width()//2)
        yc = (padre.winfo_screenheight()//2) - (self.winfo_height()//2)
        self.geometry(f"{self.winfo_width()}x{self.winfo_height()}+{xc}+{yc}")

    def Terminar(self,botones:list):

        for boton in botones:
            boton.configure(state='normal')
        self.destroy()

    def Esc(self,event:Event,botones:list):
        key = event.keysym
        print(key)
        if key=='Escape':
            self.Terminar(botones)

    def Aceptar(self,botones:list[Button],*funcs):
        pass

    def Enter(self,event:Event,botones:list[Button],*funcs):
        key = event.keysym
 
        if key=='Return':
            self.Aceptar(botones,*funcs)
        
class panelRegistro(panelEmergente):
    def __init__(self, padre: Tk, titulo: str,lbotones:list[Button], registrar) -> None:
        super().__init__(padre, titulo,lbotones)
        self.nombre = Entry(self)
        self.nombre.grid(row=0,column=1,columnspan=3,padx=10)
        self.nombre.bind('<Key>',lambda event: self.Enter(event,lbotones,registrar))
        self.nombre.focus_set() 

        cartel = Label(self,text="Semestre",style='TFrame.TLabel')
        cartel.grid(row=2,column=0,pady=10)
        self.semestre = Combobox(self,state='disabled',style='Form.TCombobox')
        self.semestre.grid(row=2,column=1,columnspan=3,padx=10)

        cartel = Label(self,text="Carrera",style='TFrame.TLabel')
        cartel.grid(row=1,column=0,pady=10)
        self.carrera = Combobox(self,state='readonly',style='Form.TCombobox',values=('IIA','LCD','ICA'))
        self.carrera.bind("<<ComboboxSelected>>", 
                            lambda event: self.semestre.configure(
                                state='readonly',
                                values = list(range(1,11) if self.carrera.get()=='ICA' else list(range(1,9)))
                                )
                        )
        self.carrera.grid(row=1,column=1,columnspan=3,padx=10)

        self.cancel.grid(row=3,column=2,rowspan=2,sticky='we',padx=20,pady=10)
        self.aceptar.grid(row=3,column=0,rowspan=2,sticky='we',padx=20,pady=10)
        self.aceptar.configure(command = lambda:self.Aceptar(lbotones,registrar))

        self.Centrar(padre)

    def Aceptar(self,botones:list,registrar):
        if self.nombre.get()=='' or self.carrera.get()=='' or self.semestre.get()=='': 
            messagebox.showerror("Falta de datos","Debes de completar todos los campos")
            return
        registrar(self.nombre.get(),self.carrera.get(), self.semestre.get())
        self.Terminar(botones)

class panelSeleccion(panelEmergente):
    def __init__(self, padre: Tk, titulo: str, botones: list,personas) -> None:
        super().__init__(padre, titulo, botones)
        self.opciones = Combobox(self,state='readonly',values=self.GetPersonas(personas),style='Form.TCombobox')
        self.opciones.grid(row=0,column=1,columnspan=3,padx=10)
        self.opciones.bind("<FocusIn>", lambda event: self.opciones.master.focus_set())
        self.opciones.bind("<<ComboboxSelected>>", self.SetSeleccion)

    def SetSeleccion(self,event:Event):
        self.seleccion = self.opciones.current()
    
    def GetPersonas(self,personas):
        nombres = []
        for persona in personas():
            nombres.append(persona[1])
        return nombres

class panelEliminar(panelSeleccion):
    def __init__(self, padre: Tk, titulo: str, botones:list,elmnNombres,elmnFotos,personas,entrenar) -> None:
        super().__init__(padre, titulo, botones,personas)
        self.opciones.bind('<Key>',lambda event: self.Enter(event,elmnNombres,elmnFotos,entrenar,botones))
        self.aceptar.configure(command = lambda:self.Aceptar(elmnNombres,elmnFotos,entrenar,botones))

        self.Centrar(padre)

    def Aceptar(self,elmnNombres,elmnFotos,entrenar,botones:list):
        if self.opciones.get()=='': 
            messagebox.showerror("Nombre","Tienes que ingresar un nombre")
            return
        elmnNombres(self.seleccion)
        elmnFotos(self.seleccion)
        self.Terminar(botones)
        entrenar()

class panelAgregar(panelSeleccion):
    def __init__(self, padre: Tk, titulo: str, botones:list,set,personas) -> None:
        super().__init__(padre, titulo, botones, personas)
        self.opciones.bind('<Key>',lambda event: self.Enter(event,botones,set))
        self.aceptar.configure(command = lambda:self.Aceptar(botones,set))

        self.Centrar(padre)

    def Aceptar(self,botones:list,set):
        if self.opciones.get()=='': 
            messagebox.showerror("Nombre","Tienes que ingresar un nombre")
            return
        set(self.seleccion)
        self.Terminar(botones)