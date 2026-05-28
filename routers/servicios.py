# routers/servicios.py — Endpoints de servicios

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Servicio, Cliente
from schemas import ServicioCreate, ServicioOut, ServicioUpdate

router = APIRouter(prefix="/servicios", tags=["Servicios"])


# ── POST /servicios ── Registrar nuevo servicio ──
@router.post("/", response_model=ServicioOut, status_code=201)
def crear_servicio(
    servicio: ServicioCreate,
    db: Session = Depends(get_db)
):
    """Registra un nuevo servicio/reparación para un cliente"""
    
    # Verificar que el cliente existe
    cliente = db.query(Cliente).filter(
        Cliente.id == servicio.cliente_id
    ).first()
    
    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )
    
    nuevo = Servicio(**servicio.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ── GET /servicios ── Listar servicios ────────────
@router.get("/", response_model=List[ServicioOut])
def listar_servicios(
    facturado: bool = None,
    cliente_id: int = None,
    descripcion: str = None,
    db: Session = Depends(get_db)
):
    """
    Lista servicios con filtros opcionales.
    Parámetros:
    - facturado: filtrar por estado (True/False)
    - cliente_id: servicios de un cliente específico
    """
    query = db.query(Servicio)
    
    if facturado is not None:
        query = query.filter(Servicio.facturado == facturado)
    
    if cliente_id is not None:
        query = query.filter(Servicio.cliente_id == cliente_id)
    
    if descripcion is not None:
        query = query.filter(Servicio.descripcion.ilike(f"%{descripcion}%"))
    
    return query.all()


# ── GET /servicios/{id} ── Obtener servicio por ID
@router.get("/{servicio_id}", response_model=ServicioOut)
def obtener_servicio(
    servicio_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene los detalles de un servicio específico"""
    servicio = db.query(Servicio).filter(
        Servicio.id == servicio_id
    ).first()
    
    if not servicio:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )
    return servicio


# ── PATCH /servicios/{id}/facturar ────────────
@router.patch("/{servicio_id}/facturar", response_model=ServicioOut)
def facturar_servicio(
    servicio_id: int,
    db: Session = Depends(get_db)
):
    """Marca un servicio como facturado/terminado"""
    servicio = db.query(Servicio).filter(
        Servicio.id == servicio_id
    ).first()
    
    if not servicio:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )
    
    servicio.facturado = True
    db.commit()
    db.refresh(servicio)
    return servicio


# ── PUT /servicios/{id} ── Actualizar servicio ────
@router.put("/{servicio_id}", response_model=ServicioOut)
def actualizar_servicio(
    servicio_id: int,
    servicio_actualizado: ServicioUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un servicio existente"""
    servicio = db.query(Servicio).filter(
        Servicio.id == servicio_id
    ).first()
    
    if not servicio:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )
    
    datos = servicio_actualizado.model_dump(exclude_unset=True)
    for campo, valor in datos.items():
        setattr(servicio, campo, valor)
    
    db.commit()
    db.refresh(servicio)
    return servicio


# ── DELETE /servicios/{id} ── Eliminar servicio ──
@router.delete("/{servicio_id}", status_code=204)
def eliminar_servicio(
    servicio_id: int,
    db: Session = Depends(get_db)
):
    """Elimina un servicio del sistema"""
    servicio = db.query(Servicio).filter(
        Servicio.id == servicio_id
    ).first()
    
    if not servicio:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )
    
    db.delete(servicio)
    db.commit()