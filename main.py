from fastapi import FastAPI

app = FastAPI()

#Endpoint de prueba
@app.get("/")
def inicio():
    return{"mensaje": "¡Api del taller funcionando!"}

#Endpoint con parametro
@app.get("/cliente/{nombre}")
def saludo(nombre: str):
    return {"cliente": nombre, "estado": "registrado"}