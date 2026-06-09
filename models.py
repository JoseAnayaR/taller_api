# models.py — Tablas de la base de datos

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


# ─── Tabla de Clientes ───────────────────────────
class Cliente(Base):
    __tablename__ = "clientes"

    id          = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String(100), nullable=False)
    telefono    = Column(String(20), nullable=True)
    email       = Column(String(120), unique=True, nullable=True)
    activo      = Column(Boolean, default=True)
    creado_en   = Column(DateTime, default=datetime.utcnow)

    # Relación: un cliente tiene muchos servicios
    servicios   = relationship("Servicio", back_populates="cliente")


# ─── Tabla de Servicios ──────────────────────────
class Servicio(Base):
    __tablename__ = "servicios"

    id           = Column(Integer, primary_key=True, index=True)
    descripcion  = Column(String(255), nullable=False)
    costo        = Column(Float, nullable=False)
    facturado   = Column(Boolean, default=False)
    fecha        = Column(DateTime, default=datetime.utcnow)
    cliente_id   = Column(Integer, ForeignKey("clientes.id"))

    cliente      = relationship("Cliente", back_populates="servicios")


