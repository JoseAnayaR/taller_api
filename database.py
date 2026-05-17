from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLite para desarrollo local
#Para producción: "postgresql://user:pass@host/dbname"
DATABASE_URL = "sqlite:///./taller.db"

engine = create_engine(
    DATABASE_URL,
    # Solo necesario para SQLite
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para todos los modelos
Base = declarative_base()

# Dependencia: crea y cierra sesión por cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()