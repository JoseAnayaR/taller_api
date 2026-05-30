# main.py - Punto de enrada de la API del Taller
# Ejecuttar: uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import clientes, servicios, reportes

# Crea todas las tablas en SQLite al iniciar
Base.metadata.create_all(bind=engine)

app=FastAPI(
    title="API Taller mecanico",
    description="Sistema de gestion de clientes y servicios",
    version="1.0.0"
)

#Permite peticiones desde el naveegador (úti endesarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

#Registra las rutas
app.include_router(clientes.router)
app.include_router(servicios.router)
app.include_router(reportes.router)

@app.get("/")
def raiz():
    """Endpoints de prueba"""
    return {
        "mensaje": "¡API del Taller activa",
        "docs": "http://localhost:8000/docs",
        "redoc": "/redoc",
        "versión": "1.0.0"
    }
    
@app.get("/health")
def health_check():
    """Verificar que la API está funcionando"""
    return {"status": "healthy"}