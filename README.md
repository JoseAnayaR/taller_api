# Taller API — Auto Repair Shop Management System
 
A REST API built with **FastAPI** and **SQLAlchemy** to manage clients, repair services, and payments for an auto repair shop.
 
Built as a real-world portfolio project — currently running in production at a mechanic shop in Tlaquepaque, Jalisco 🇲🇽
 
## Tech Stack
 
- **FastAPI** — modern async REST API framework with automatic documentation
- **SQLAlchemy** — ORM with SQLite (dev) / PostgreSQL (prod)
- **Pydantic v2** — data validation and serialization
- **pandas + openpyxl** — automated weekly reports in Excel
- **APScheduler** — task automation and scheduled jobs
## Quick Start
 
```bash
# Clone and navigate
git clone https://github.com/your-username/taller-api
cd taller-api
 
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
 
# Install dependencies
pip install -r requirements.txt
 
# Run the server
uvicorn main:app --reload
```
 
The API will be available at **http://127.0.0.1:8000**
 
## API Endpoints
 
### Clients (Clientes)
 
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/clientes/` | Register a new client |
| GET | `/clientes/` | List all clients (with pagination) |
| GET | `/clientes/{id}` | Get client details by ID |
| PUT | `/clientes/{id}` | Update client information |
| DELETE | `/clientes/{id}` | Delete a client |
 
**Example: Create a client**
```bash
curl -X POST "http://localhost:8000/clientes/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan García",
    "telefono": "+52 123 456 7890",
    "email": "juan@example.com"
  }'
```
 
### Services (Servicios)
 
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/servicios/` | Register a new repair service |
| GET | `/servicios/` | List all services (with filters) |
| GET | `/servicios/{id}` | Get service details by ID |
| PUT | `/servicios/{id}` | Update service information |
| PATCH | `/servicios/{id}/completar` | Mark service as completed |
| DELETE | `/servicios/{id}` | Delete a service |
 
**Example: Create a service**
```bash
curl -X POST "http://localhost:8000/servicios/" \
  -H "Content-Type: application/json" \
  -d '{
    "descripcion": "Oil change and filter replacement",
    "costo": 450.00,
    "cliente_id": 1
  }'
```
 
## Interactive Documentation
 
FastAPI automatically generates interactive API documentation:
 
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
Use Swagger to test all endpoints directly in your browser.
 
## Database Schema
 
### Clientes (Clients)
```
id (INT) - Primary Key
nombre (STRING) - Client name
telefono (STRING) - Phone number
email (STRING) - Email address (unique)
activo (BOOLEAN) - Active status
creado_en (DATETIME) - Creation timestamp
```
 
### Servicios (Services)
```
id (INT) - Primary Key
descripcion (STRING) - Service description
costo (FLOAT) - Service cost
completado (BOOLEAN) - Completion status
fecha (DATETIME) - Service date
cliente_id (INT) - Foreign Key to Cliente
```
 
### Pagos (Payments)
```
id (INT) - Primary Key
monto (FLOAT) - Payment amount
metodo (STRING) - Payment method
servicio_id (INT) - Foreign Key to Servicio
fecha (DATETIME) - Payment date
```
 
## Project Structure
 
```
taller-api/
├── main.py              # Entry point, FastAPI app setup
├── database.py          # Database configuration (SQLite/PostgreSQL)
├── models.py            # SQLAlchemy models (tables)
├── schemas.py           # Pydantic validation schemas
├── routers/
│   ├── clientes.py      # Client endpoints
│   └── servicios.py     # Service endpoints
├── requirements.txt     # Python dependencies
└── README.md           # This file
```
 
## Deployment
 
### Local Development
```bash
uvicorn main:app --reload
```
 
### Production Deployment
 
For production, change the database URL in `database.py`:
 
```python
DATABASE_URL = "postgresql://user:password@host:5432/dbname"
```
 
Then deploy with a production-grade server:
 
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```
 
Recommended platforms:
- **Railway** (easiest, free tier available)
- **Render** (simple deployment, good free plan)
- **AWS EC2** (traditional option, more control)
## Features Implemented
 
✅ Full CRUD for clients and services  
✅ Automatic data validation with Pydantic  
✅ SQLAlchemy ORM with relationships  
✅ Interactive API documentation (Swagger UI)  
✅ CORS support for cross-origin requests  
✅ Production-ready project structure  
✅ Ready for PostgreSQL migration  
 
## Future Enhancements
 
- 📊 Automated Excel report generation (weekly/monthly)
- 📧 Email notifications for completed services
- 🔐 User authentication and authorization
- 💰 Payment tracking and invoicing
- 📱 Mobile app companion
- 📈 Analytics dashboard
## License
 
This project is open source and available for educational and commercial use.
 
## Author
 
Built by a backend developer transitioning to remote work from Mexico 🇲🇽
 
---
 
**Ready to deploy?** Start with Railway or Render — they handle Python/PostgreSQL perfectly and deployment takes 5 minutes.