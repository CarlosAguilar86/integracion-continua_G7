import os
from contextlib import asynccontextmanager
import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configuramos la conexión apuntando al contenedor de la base de datos
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://usuario_db:clave_secreta@postgres_db:5432/tareas_db"
)

def get_connection() -> psycopg.Connection:
    return psycopg.connect(DATABASE_URL)

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Creamos la tabla 'tasks' al iniciar la aplicación
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL
            )
            """
        )
    yield

app = FastAPI(title="Gestor de Tareas CI", lifespan=lifespan)

class TaskIn(BaseModel):
    title: str

class Task(TaskIn):
    id: int

@app.get("/health")
def health() -> dict:
    # Verifica la conectividad de la API y la base de datos
    try:
        with get_connection() as conn:
            version = conn.execute("SELECT version()").fetchone()[0]
    except psycopg.OperationalError as exc:
        raise HTTPException(status_code=503, detail=f"Base de datos inalcanzable: {exc}")
    return {"api": "ok", "database": "ok", "postgres_version": version}

@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    with get_connection() as conn:
        rows = conn.execute("SELECT id, title FROM tasks ORDER BY id").fetchall()
    return [Task(id=row[0], title=row[1]) for row in rows]

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskIn) -> Task:
    with get_connection() as conn:
        row = conn.execute(
            "INSERT INTO tasks (title) VALUES (%s) RETURNING id, title", (task.title,)
        ).fetchone()
    return Task(id=row[0], title=row[1])
