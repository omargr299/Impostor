from os import makedirs, listdir,remove
from shutil import rmtree
from os.path import exists
from parametros import NFOTOS
import pyodbc
import configparser
import cv2
import numpy as np

class Base():

    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('.env')
        server = config["DATABASE"]["SERVER"] 
        user = config["DATABASE"]["USERNAME"] 
        password = config["DATABASE"]["PASSWORD"] 
        db = config["DATABASE"]["DBNAME"]

        if not server and not db: return

        if user:
            self.base = pyodbc.connect("Driver={SQL Server};"
                "Server=DESKTOP-097NNS9;"
                "Database=Impostor;"
                "Trusted_Connection=yes;")
        else:
            self.base = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};'+\
                                'SERVER='+server+
                                ';DATABASE='+db+
                                ';ENCRYPT=yes;UID='+
                                user+
                                ';PWD='+ password)

        self.cursor = self.base.cursor()

    def AgregarAlumno(self,nombre:str,carrera:str,semestre:int) -> str:
        sp = "exec [dbo].[AgregarAlumnos] ?,?,? "
        self.cursor.execute(sp,(nombre.capitalize(),carrera,semestre))
        self.cursor.commit()

    def BorrarAlumno(self,id):
        sp = "exec [dbo].[EliminarAlumnos] ? "
        self.cursor.execute(sp,(id))
        self.cursor.commit()

    def ObtenerAlumnos(self) -> list:
        self.cursor.execute("exec [dbo].[ObtenerAlumnos]")
        return self.cursor.fetchall()

    def ObtenerNombres(self) -> list[tuple[int,str]]:
        self.cursor.execute("exec [dbo].[ObtenerNombres]")
        return self.cursor.fetchall()

    def AgregarFoto(self,alumid:int,foto:str):
        sp = "exec [dbo].[AgregarFotos] ?,? "
        self.cursor.execute(sp,(alumid,foto))
        self.cursor.commit()

    def BorrarFotos(self,alumid:int):
        sp = "exec [dbo].[EliminarFotos] ? "
        self.cursor.execute(sp,(alumid))
        self.cursor.commit()

    def ObtenerFotos(self,alumid:int) -> list[tuple[int,str]]:
        self.cursor.execute("exec [dbo].[ObtenerFotos] ?",(alumid))
        return self.cursor.fetchall()

    def CantidadFotos(self,alumid:int) -> int:
        self.cursor.execute("exec [dbo].[CantidadFotos] ?",(alumid))
        return self.cursor.fetchall()[0][0]

    def Incompletos(self):
        for persona in self.ObtenerNombres():
            if len(self.ObtenerFotos(persona[0]))<NFOTOS:
                self.BorrarAlumno(persona[0])
                self.BorrarFotos(persona[0])

