# Taller API

Auto repair shop management API built with FastAPI.

## 🚀 Live Demo

**API está VIVA:** https://tu-api-taller-xxxxx.railway.app
**Documentación:** https://tu-api-taller-xxxxx.railway.app/docs

Pruébalo ahora mismo en tu navegador o celular.

## Features

✅ REST API con FastAPI
✅ Filtros avanzados de búsqueda
✅ 6 reportes Excel automáticos (análisis de negocio)
✅ Base de datos PostgreSQL
✅ Deploy automático desde GitHub
✅ Documentación interactiva (Swagger UI)

## Endpoints Disponibles

### Clientes
- `GET /clientes/` - Listar con filtros (activo, nombre, email)
- `POST /clientes/` - Crear cliente
- `PUT /clientes/{id}` - Actualizar
- `DELETE /clientes/{id}` - Eliminar

### Servicios
- `GET /servicios/` - Listar con filtros (facturado, cliente_id, descripción)
- `POST /servicios/` - Crear servicio
- `PATCH /servicios/{id}/facturar` - Marcar como facturado
- `DELETE /servicios/{id}` - Eliminar

### Reportes
- `GET /reportes/clientes-activos` - Excel con clientes activos
- `GET /reportes/ingresos-mes` - Excel con ingresos por mes
- `GET /reportes/servicios-facturados` - Excel servicios facturados
- `GET /reportes/servicios-no-facturados` - Excel servicios sin facturar
- `GET /reportes/top-clientes` - Excel ranking de clientes (80/20)
- `GET /reportes/resumen` - Excel con dashboard ejecutivo

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Pydantic
- **Database:** PostgreSQL (production), SQLite (development)
- **Reports:** pandas, openpyxl
- **Deployment:** Railway (Docker, automated)
- **Version Control:** Git, GitHub

## Desarrollo Local

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/taller-api.git
cd taller-api

# Crear ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn main:app --reload

# Abrir documentación
# http://localhost:8000/docs
```

## Producción

La API está desplegada automáticamente en Railway.
Cada `git push` actualiza automáticamente la aplicación en vivo.