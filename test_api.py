import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

# ─────────────────────────────────────────────────────────────
# SETUP: Configurar BD de tests
# ─────────────────────────────────────────────────────────────

# BD en memoria para tests 
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear y borrar las tablas en la BD para evitar colision de datos 
@pytest.fixture(autouse=True)
def limpiar_base_de_datos():
    """
    Borra y recrea todas las tablas antes de cada test.
    Así garantizamos que la BD siempre esté limpia y no halla colisión de datos.
    """
    Base.metadata.drop_all(bind=engine)   # Borra las tablas y sus datos
    Base.metadata.create_all(bind=engine)  # Las vuelve a crear
    yield

def override_get_db():
    """Función que usa BD de tests en lugar de la real"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Reemplazar get_db con la versión de tests
app.dependency_overrides[get_db] = override_get_db

# Cliente HTTP para probar endpoints
client = TestClient(app)




# ─────────────────────────────────────────────────────────────
# TESTS PARA CLIENTES
# ─────────────────────────────────────────────────────────────

def test_crear_cliente_valido():
    """
    TEST 1: Verifica que puedes crear un cliente con datos válidos.
    
    Flujo:
    1. Enviar POST a /clientes/ con datos
    2. Verificar que retorna 201 (Created)
    3. Verificar que los datos están correctos
    4. Verificar que se generó un ID
    """
    response = client.post(
        "/clientes/",
        json={
            "nombre": "Juan García",
            "telefono": "+52 123 456 7890",
            "email": "juan@test.com"
        },
    )
    
    # Verificaciones
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    
    data = response.json()
    
    assert data["nombre"] == "Juan García"
    assert data["email"] == "juan@test.com"
    
    assert data["id"] is not None, "ID debe ser generado"


def test_crear_cliente_email_duplicado():
    """
    TEST 2: Verifica que NO permite 2 clientes con mismo email.
    
    Flujo:s
    1. Crear cliente #1
    2. Intentar crear cliente #2 con mismo email
    3. Verificar que rechaza (error 400 o 409)
    """
    # Crear primer cliente
    client.post(
        "/clientes/",
        json={
            "nombre": "Juan",
            "telefono": "+52 123",
            "email": "juan@test.com"
        },
    )
    
    # Intentar crear otro con mismo email
    response = client.post(
        "/clientes/",
        json={
            "nombre": "Pedro",
            "telefono": "+52 456",
            "email": "juan@test.com"  # ← Mismo email
        },
    )
    
    # Debe rechazar
    assert response.status_code in [400, 409], f"Should reject duplicate email, got {response.status_code}"


def test_listar_clientes():
    """
    TEST 3: Verifica que puedes listar todos los clientes.
    
    Flujo:
    1. Crear 2 clientes
    2. Listar GET /clientes/
    3. Verificar que retorna lista con clientes
    """
    # Crear 2 clientes
    for i in range(2):
        client.post(
            "/clientes/",
            json={
                "nombre": f"Cliente {i}",
                "telefono": f"+52 {i}",
                "email": f"cliente{i}@test.com"
            },
        )
    
    # Listar
    response = client.get("/clientes/")
    
    assert response.status_code == 200
    clientes = response.json()
    assert len(clientes) >= 2, "Debería haber al menos 2 clientes"


def test_filtrar_clientes_activos():
    """
    TEST 4: Verifica que el filtro por activo=true funciona.
    
    Flujo:
    1. Crear cliente (por defecto activo=true)
    2. Listar con filtro ?activo=true
    3. Verificar que TODOS tienen activo=true
    """
    # Crear cliente
    response = client.post(
        "/clientes/",
        json={
            "nombre": "Cliente Activo",
            "telefono": "+52 123",
            "email": "activo@test.com"
        },
    )
    
    assert response.status_code == 201
    
    # Listar con filtro activo=true
    response = client.get("/clientes/?activo=true")
    
    assert response.status_code == 200
    clientes = response.json()
    
    # Todos deben tener activo=true
    for cliente in clientes:
        assert cliente["activo"] == True, f"Cliente {cliente['id']} tiene activo={cliente['activo']}"


def test_filtrar_clientes_nombre():
    """
    TEST 5: Verifica que la búsqueda por nombre funciona.
    
    Flujo:
    1. Crear cliente con nombre "Juan García"
    2. Buscar con ?nombre=juan (minúsculas)
    3. Verificar que encuentra al cliente
    """
    # Crear cliente
    client.post(
        "/clientes/",
        json={
            "nombre": "Juan García",
            "telefono": "+52 123",
            "email": "juan@test.com"
        },
    )
    
    # Buscar (icase - sin importar mayúsculas)
    response = client.get("/clientes/?nombre=juan")
    
    assert response.status_code == 200
    clientes = response.json()
    assert len(clientes) >= 1, "Debería encontrar cliente con 'juan'"
    assert "juan" in clientes[0]["nombre"].lower()


def test_obtener_cliente_por_id():
    """
    TEST 6: Verifica que puedes obtener un cliente específico por ID.
    
    Flujo:
    1. Crear cliente
    2. Obtener el ID de la respuesta
    3. Hacer GET /clientes/{id}
    4. Verificar que retorna ese cliente
    """
    # Crear cliente
    create_response = client.post(
        "/clientes/",
        json={
            "nombre": "Jose",
            "telefono": "+52 123",
            "email": "jose@test.com"
        },
    )
    
    cliente_id = create_response.json()["id"]
    
    # Obtener por ID
    response = client.get(f"/clientes/{cliente_id}")
    
    assert response.status_code == 200
    assert response.json()["id"] == cliente_id


def test_actualizar_cliente():
    """
    TEST 7: Verifica que puedes actualizar un cliente.
    
    Flujo:
    1. Crear cliente
    2. Hacer PUT con datos nuevos
    3. Verificar que cambiaron
    """
    # Crear
    create_response = client.post(
        "/clientes/",
        json={
            "nombre": "Juan1",
            "telefono": "+52 123",
            "email": "juan1@test.com"
        },
    )
    
    cliente_id = create_response.json()["id"]
    
    # Actualizar
    response = client.put(
        f"/clientes/{cliente_id}",
        json={
            "nombre": "Juan Actualizado",
            "telefono": "+52 456",
            "email": "juan.nuevo@test.com"
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Juan Actualizado"
    assert data["email"] == "juan.nuevo@test.com"


def test_eliminar_cliente():
    """
    TEST 8: Verifica que puedes eliminar un cliente.
    
    Flujo:
    1. Crear cliente
    2. DELETE /clientes/{id}
    3. Intentar obtenerlo nuevamente
    4. Verificar que retorna 404 (no existe)
    """
    # Crear
    create_response = client.post(
        "/clientes/",
        json={
            "nombre": "JuanT8",
            "telefono": "+52 123",
            "email": "juanT8@test.com"
        },
    )
    
    cliente_id = create_response.json()["id"]
    
    # Eliminar
    response = client.delete(f"/clientes/{cliente_id}")
    assert response.status_code == 204
    
    # Verificar que ya no existe
    response = client.get(f"/clientes/{cliente_id}")
    assert response.status_code == 404, "Cliente eliminado debería retornar 404"


# ─────────────────────────────────────────────────────────────
# TESTS PARA SERVICIOS
# ─────────────────────────────────────────────────────────────

def test_crear_servicio():
    """
    TEST 9: Verifica que puedes crear un servicio.
    
    Flujo:
    1. Crear cliente (necesario para servicio)
    2. Crear servicio con cliente_id
    3. Verificar que se creó correctamente
    4. Verificar que facturado=false por defecto
    """
    # Primero crear cliente
    cliente_response = client.post(
        "/clientes/",
        json={
            "nombre": "JuanT9",
            "telefono": "+52 123",
            "email": "juant9@test.com"
        },
    )
    cliente_id = cliente_response.json()["id"]
    
    # Crear servicio
    response = client.post(
        "/servicios/",
        json={
            "descripcion": "Cambio de aceite",
            "costo": 450.50,
            "cliente_id": cliente_id
        },
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["descripcion"] == "Cambio de aceite"
    assert data["costo"] == 450.50
    assert data["facturado"] == False, "Nuevo servicio debe estar no facturado"


def test_crear_servicio_sin_cliente():
    """
    TEST 10: Verifica que rechaza servicio sin cliente válido.
    
    Flujo:
    1. Intentar crear servicio con cliente_id que no existe
    2. Verificar que rechaza (400 o 404)
    """
    response = client.post(
        "/servicios/",
        json={
            "descripcion": "Cambio de aceite",
            "costo": 450.50,
            "cliente_id": 99999  # Cliente que no existe
        },
    )
    
    assert response.status_code in [400, 404], f"Should reject invalid cliente_id, got {response.status_code}"


def test_listar_servicios():
    """
    TEST 11: Verifica que puedes listar servicios.
    
    Flujo:
    1. Crear cliente
    2. Crear servicio
    3. GET /servicios/
    4. Verificar que aparece en lista
    """
    # Crear cliente
    cliente_response = client.post(
        "/clientes/",
        json={
            "nombre": "JuanT11",
            "telefono": "+52 123",
            "email": "juant11@test.com"
        },
    )
    cliente_id = cliente_response.json()["id"]
    
    # Crear servicio
    client.post(
        "/servicios/",
        json={
            "descripcion": "Cambio de aceite",
            "costo": 450.50,
            "cliente_id": cliente_id
        },
    )
    
    # Listar
    response = client.get("/servicios/")
    
    assert response.status_code == 200
    servicios = response.json()
    assert len(servicios) >= 1


def test_filtrar_servicios_no_facturados():
    """
    TEST 12: Verifica que filtro por facturado=false funciona.
    
    Flujo:
    1. Crear servicio (por defecto facturado=false)
    2. GET /servicios/?facturado=false
    3. Verificar que TODOS tienen facturado=false
    """
    # Crear cliente y servicio
    cliente_response = client.post(
        "/clientes/",
        json={
            "nombre": "JuanT12",
            "telefono": "+52 123",
            "email": "juant12@test.com"
        },
    )
    cliente_id = cliente_response.json()["id"]
    
    client.post(
        "/servicios/",
        json={
            "descripcion": "Cambio de aceite",
            "costo": 450.50,
            "cliente_id": cliente_id
        },
    )
    
    # Filtrar no facturados
    response = client.get("/servicios/?facturado=false")
    
    assert response.status_code == 200
    servicios = response.json()
    
    for servicio in servicios:
        assert servicio["facturado"] == False


def test_marcar_servicio_facturado():
    """
    TEST 13: Verifica que puedes marcar un servicio como facturado.
    
    Flujo:
    1. Crear cliente y servicio (facturado=false)
    2. PATCH /servicios/{id}/facturar
    3. Verificar que ahora facturado=true
    """
    # Crear cliente y servicio
    cliente_response = client.post(
        "/clientes/",
        json={
            "nombre": "JuanT13",
            "telefono": "+52 123",
            "email": "juant13@test.com"
        },
    )
    cliente_id = cliente_response.json()["id"]
    
    servicio_response = client.post(
        "/servicios/",
        json={
            "descripcion": "Cambio de aceite",
            "costo": 450.50,
            "cliente_id": cliente_id
        },
    )
    servicio_id = servicio_response.json()["id"]
    
    # Marcar como facturado
    response = client.patch(f"/servicios/{servicio_id}/facturar")
    
    assert response.status_code == 200
    assert response.json()["facturado"] == True


# ─────────────────────────────────────────────────────────────
# TESTS PARA REPORTES
# ─────────────────────────────────────────────────────────────

def test_reporte_clientes_activos():
    """
    TEST 14: Verifica que se puede generar reporte de clientes activos.
    
    Flujo:
    1. Crear cliente
    2. GET /reportes/clientes-activos
    3. Verificar que retorna archivo Excel
    """
    # Crear cliente
    client.post(
        "/clientes/",
        json={
            "nombre": "JuanT14",
            "telefono": "+52 123",
            "email": "juant14@test.com"
        },
    )
    
    # Descargar reporte
    response = client.get("/reportes/clientes-activos")
    
    assert response.status_code == 200
    # Verificar que es Excel (content-type contiene "spreadsheetml")
    content_type = response.headers.get("content-type", "")
    assert "spreadsheetml" in content_type or "application/vnd" in content_type, f"Should return Excel file, got {content_type}"


def test_reporte_ingresos():
    """
    TEST 15: Verifica que se genera reporte de ingresos.
    
    Flujo:
    1. Crear cliente
    2. Crear servicio
    3. Marcar como facturado
    4. GET /reportes/ingresos-mes
    5. Verificar que retorna Excel
    """
    # Crear cliente y servicio facturado
    cliente_response = client.post(
        "/clientes/",
        json={
            "nombre": "JuanT15",
            "telefono": "+52 123",
            "email": "juant15@test.com"
        },
    )
    cliente_id = cliente_response.json()["id"]
    
    servicio_response = client.post(
        "/servicios/",
        json={
            "descripcion": "Cambio de aceite",
            "costo": 450.50,
            "cliente_id": cliente_id
        },
    )
    servicio_id = servicio_response.json()["id"]
    
    # Marcar como facturado
    client.patch(f"/servicios/{servicio_id}/facturar")
    
    # Descargar reporte
    response = client.get("/reportes/ingresos-mes")
    
    assert response.status_code == 200
    content_type = response.headers.get("content-type", "")
    assert "spreadsheetml" in content_type or "application/vnd" in content_type