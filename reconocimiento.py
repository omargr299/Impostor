
from cv2 import face,CascadeClassifier,VideoCapture
from cv2 import destroyAllWindows,flip,cvtColor,putText,rectangle,imencode,imdecode,resize
from cv2 import CAP_DSHOW,LINE_AA,COLOR_BGR2GRAY, COLOR_GRAY2BGR,IMREAD_GRAYSCALE,INTER_CUBIC
from os import remove
from os.path import exists
from numpy import array
from threading import Thread
from parametros import NFOTOS,GetError
from base import Base
from modos import *
from numpy import frombuffer,uint8,ndarray
from colores import COLORDESC,COLORDETEC,COLORINFO

def Salir() -> None:
    destroyAllWindows()

class Reconocedor():
    def __init__(self,base:Base) -> None:
        self.modo = RECONOCIMIENTO
        self.count = 0 
        self.cantidadFotos = 0

        self.cap = VideoCapture(0,CAP_DSHOW)

        self.personasDetectadas = {}

        self.base = base
        self.ActualizarPersonas()

        print('imagePaths = ',self.personas)

        self.reconocedor = face.LBPHFaceRecognizer_create()
        if exists('modeloLBPHFace.xml'):
            self.reconocedor.read('modeloLBPHFace.xml')

        self.clasificador = CascadeClassifier('haarcascade_frontalface_default.xml')

    def Captura(self) -> ndarray:
        try:
            _, frame = self.cap.read()
            frame = flip(frame,1)
            self.foto = frame
            self.fotoGray = cvtColor(frame,COLOR_BGR2GRAY)

            return self.foto
        except:
            pass

    def ActualizarPersonas(self):
        self.personas = self.base.ObtenerAlumnos()
        self.personasDetectadas.clear()

    def SetID(self,id:int):
        self.alumID = id
        self.modo = REGISTRO

    def Resgistrar(self,nombre:str,carrera:str,semestre:int):
        self.base.AgregarAlumno(nombre,carrera,semestre)
        self.ActualizarPersonas()
        self.SetID(self.personas[-1][0])

    def AgregarFotos(self,rostro: ndarray,x: int,y: int,w: int,h: int):

        if self.base.CantidadFotos(self.alumID)>NFOTOS:
            self.cantidadFotos = self.base.CantidadFotos(self.alumID)

        rostro = cvtColor(rostro,COLOR_GRAY2BGR)

        putText(self.foto,'Registrando'+'.'*(self.count%3),(x,y-20),2,0.8,(255,0,0),1,LINE_AA)
        rectangle(self.foto, (x,y),(x+w,y+h),(255,0,0),2)
        rostro_str = imencode('.jpg', rostro)[1].tostring()
        self.base.AgregarFoto(self.alumID,rostro_str)

        self.count+=1

        if self.count>=NFOTOS:
            self.Entrenar(True)
            self.count = 0
    
    def Reconocimineto(self,rostros: list) -> ndarray:
        results = []
        for rost,x,y,w,h in rostros:
            try:
                result = self.reconocedor.predict(rost)
                if len(result)<2: raise
                results.append((*result,rost,x,y,w,h))
            except:
                results.append((-1,0,rost,x,y,w,h))
        
        for tag,porc,_,_,_,_,_ in results:
            if tag < 0: continue

            if tag not in self.personasDetectadas or self.personasDetectadas[tag] < porc:
                self.personasDetectadas[tag] = porc

        ultmRostro = None
        for tag,error,rostro,x,y,w,h in results:
            print(tag, error)

            if  error < GetError() and len(self.personas)>0 and tag<=len(self.personas)-1  and  tag>-1 and error == self.personasDetectadas[tag]:
            
                putText(self.foto, f'{self.personas[tag][1]}', (x,y-25), 2, 1.1, COLORDETEC, 1, LINE_AA)
                putText(self.foto, f'Parentezco: {round(100-error,2)}%', (x,y-5), 1, 0.8, COLORINFO, 1, LINE_AA)
                print(self.personas[tag][2])
                putText(self.foto, f'Id: {self.personas[tag][0]}', (x+w+10,y+20), 1, 1.3, COLORINFO, 1, LINE_AA)
                putText(self.foto, f'Carrera: {self.personas[tag][2]}', (x+w+10,y+40), 1, 1.3, COLORINFO, 1, LINE_AA)
                putText(self.foto, f'Semestre: {self.personas[tag][3]}', (x+w+10,y+60), 1, 1.3, COLORINFO, 1, LINE_AA)
                rectangle(self.foto, (x,y), (x+w,y+h), COLORDETEC,2)
            else:
                putText(self.foto, f'???', (x,y-5), 1, 1.3, COLORINFO, 1, LINE_AA)
                putText(self.foto, 'Desconocido', (x,y-20), 2, 0.8, COLORDESC, 1, LINE_AA)
                rectangle(self.foto, (x,y), (x+w,y+h), COLORDESC,2)

            ultmRostro = rostro

        return ultmRostro

    def Entrenar(self,eliminar: bool=False):
        if exists('.\\modeloLBPHFace.xml') and not eliminar: remove('.\\modeloLBPHFace.xml')
        self.ActualizarPersonas()
        if len(self.base.ObtenerNombres())<1: 
            self.reconocedor = face.LBPHFaceRecognizer_create()
            return
        
        t = Thread(target=self.Entrenamiento)
        t.start()
        self.modo = ENTRENAMIENTO


    def Entrenamiento(self):
        labels = []
        facesData = []
        self.ActualizarPersonas()
        
        for persona in self.personas:

            print('Leyendo las imágenes')
            print(persona[1])
            for foto in self.base.ObtenerFotos(persona[0]):
                imgarray = frombuffer(foto[1],dtype=uint8)
                img = imdecode(imgarray, IMREAD_GRAYSCALE) 
                facesData.append(img)
                labels.append(foto[0])

        print("Entrenando...")
        self.reconocedor.train(facesData, array(labels))
        self.reconocedor.write('modeloLBPHFace.xml')
        self.reconocedor.read('modeloLBPHFace.xml')
        print("Modelo almacenado...")   
        self.ActualizarPersonas()
        self.modo = RECONOCIMIENTO
    
    def Detecccion(self) -> ndarray:
        faces = self.clasificador.detectMultiScale(self.fotoGray,1.2,5)
        imgrostro = None
        self.ActualizarPersonas()
        rostros = []

        for (x,y,w,h) in faces: 
            rostro = self.fotoGray[y:y+h,x:x+w]
            rostro = resize(rostro,(150,150),interpolation= INTER_CUBIC)
            
            if self.modo == RECONOCIMIENTO: rostros.append((rostro,x,y,w,h))
            elif self.modo == REGISTRO: self.AgregarFotos(rostro,x,y,w,h)
            
        if self.modo == RECONOCIMIENTO: imgrostro = self.Reconocimineto(rostros)

        return imgrostro