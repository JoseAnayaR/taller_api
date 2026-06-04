# routers/clientes.py — Endpoints de clientes

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Cliente
from schemas import ClienteCreate, ClienteOut

router = APIRouter(prefix="/clientes", tags=["Clientes"])


# ── POST /clientes ── Registrar nuevo cliente ────
@router.post("/", response_model=ClienteOut, status_code=201)
def crear_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):
    """Registra un nuevo cliente en el sistema"""
    
    # Verificar que el email no esté duplicado
    if cliente.email:
        existente = db.query(Cliente).filter(
            Cliente.email == cliente.email
        ).first()
        if existente:
            raise HTTPException(
                status_code=400,
                detail="Email ya registrado"
            )
    
    nuevo = Cliente(**cliente.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ── GET /clientes ── Listar todos los clientes ───
@router.get("/", response_model=List[ClienteOut])
def listar_clientes(
    skip: int = 0,
    limit: int = 100,
    activo: bool = None,
    nombre: str = None,
    email: str = None,
    db: Session = Depends(get_db)
):
    """
    Lista clientes con filtros opcionales.
    Parámetros:
    - activo: true/false para clientes activos/inactivos
    - nombre: Busca clientescyo nombre CONTIENE este texto (case-insensitive)
    - email: Busca clientes cuyo email CONTIENE este texto (case-insensitive)   
    """
    #Aqui comienza la busqueda
    query = db.query(Cliente)
    #-----------------------------------------------
    #APLICAR FILTROS(Solo si el usuario los indicó)
    #-----------------------------------------------
    if activo is not None:
        query = query.filter(Cliente.activo == activo)
        
    if nombre is not None:
        query = query.filter(Cliente.nombre.ilike(f"%{nombre}%"))
        
    if email is not None:
        query = query.filter(Cliente.email.ilike(f"%{email}%"))
        
    return query.offset(skip).limit(limit).all()


# ── GET /clientes/{id} ── Buscar cliente por ID ──
@router.get("/{cliente_id}", response_model=ClienteOut)
def obtener_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene los datos de un cliente específico por ID"""
    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()
    
    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )
    return cliente


# ── PUT /clientes/{id} ── Actualizar cliente ────
@router.put("/{cliente_id}", response_model=ClienteOut)
def actualizar_cliente(
    cliente_id: int,
    cliente_actualizado: ClienteCreate,
    db: Session = Depends(get_db)
):
    """Actualiza los datos de un cliente existente"""
    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()
    
    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )
    
    # Actualizar solo los campos no nulos
    datos = cliente_actualizado.model_dump(exclude_unset=True)
    for campo, valor in datos.items():
        setattr(cliente, campo, valor)
    
    db.commit()
    db.refresh(cliente)
    return cliente


# ── DELETE /clientes/{id} ── Eliminar cliente ────
@router.patch("/{cliente_id}/desactivar")
def desactivar_cliente(cliente_id: int, db: Session = Depends(get_db)
):
    """Desactiva un cliente del sistema sin eliminar sus datos"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    
    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )
    
    cliente.activo =  False
    
    db.commit()
    db.refresh(cliente)
    
    return {
        "mensaje": f"Cliente '{cliente.nombre}' desactivado",
        "cliente": cliente
    }