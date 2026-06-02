import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#SQLite para desarrollo local
#Para producción: "postgresql://user:pass@host/dbname"
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL is None:
    DATABASE_URL = "sqlite:///./taller.db"
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://",1)
    
if DATABASE_URL.startswith("sqlite"):
    
    engine = create_engine(
        DATABASE_URL,
        # Solo necesario para SQLite
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True
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