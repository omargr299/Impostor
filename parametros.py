NFOTOS = 50
ERROR = 50

def AumentarError():
    global ERROR
    ERROR+=5

def ReducirError():
    global ERROR
    ERROR-=5

def GetError():
    global ERROR
    return ERROR
