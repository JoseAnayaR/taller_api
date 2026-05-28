# schemas.py — Validación y serialización de datos con Pydantic

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ─── Esquemas de Cliente ─────────────────────────
class ClienteBase(BaseModel):
    """Campos comunes para crear y leer clientes"""
    nombre:   str
    telefono: Optional[str] = None
    email:    Optional[EmailStr] = None


class ClienteCreate(ClienteBase):
    """Para crear un cliente (POST)"""
    pass


class ClienteOut(ClienteBase):
    """Para responder con datos del cliente (GET)"""
    id:        int
    activo:    bool
    creado_en: datetime

    class Config:
        from_attributes = True  # Lee desde ORM


# ─── Esquemas de Servicio ────────────────────────
class ServicioBase(BaseModel):
    descripcion: str
    costo:       float
    cliente_id:  int


class ServicioCreate(ServicioBase):
    pass


class ServicioOut(ServicioBase):
    id:         int
    facturado: bool
    fecha:      datetime

    class Config:
        from_attributes = True


class ServicioUpdate(BaseModel):
    """Para actualizar un servicio"""
    descripcion: Optional[str] = None
    costo:       Optional[float] = None
    facturado:  Optional[bool] = None