import os
import time
import uuid
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .database import get_db, init_db
from .models import SpeedTest
from .schemas import SpeedTestCreate, SpeedTestResponse

DOWNLOAD_SIZE = 100 * 1024 * 1024  # 100 MB
CHUNK_SIZE    = 64 * 1024           # 64 KB por chunk


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="ArretadoSpeed API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host


# ── Ping ─────────────────────────────────────────────────────────────────────

@app.get("/api/ping")
async def ping():
    return {"ts": time.time() * 1000}  # milissegundos


# ── Download ──────────────────────────────────────────────────────────────────

@app.get("/api/download")
async def download(request: Request):
    """Serve um stream de dados aleatórios para medir velocidade de download."""

    async def data_generator():
        sent = 0
        while sent < DOWNLOAD_SIZE:
            remaining = DOWNLOAD_SIZE - sent
            chunk = min(CHUNK_SIZE, remaining)
            yield os.urandom(chunk)
            sent += chunk
            await asyncio.sleep(0)  # cede o loop para não bloquear

    headers = {
        "Content-Length": str(DOWNLOAD_SIZE),
        "Cache-Control": "no-store",
        "Content-Type": "application/octet-stream",
    }
    return StreamingResponse(data_generator(), headers=headers)


# ── Upload ────────────────────────────────────────────────────────────────────

@app.post("/api/upload")
async def upload(request: Request):
    """Recebe payload do cliente e retorna bytes recebidos e tempo em ms."""
    start = time.perf_counter()
    body  = await request.body()
    elapsed_ms = (time.perf_counter() - start) * 1000
    return {
        "bytes_received": len(body),
        "elapsed_ms": elapsed_ms,
    }


# ── Salvar resultado ──────────────────────────────────────────────────────────

@app.post("/api/result", response_model=SpeedTestResponse, status_code=201)
async def save_result(
    payload: SpeedTestCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    record = SpeedTest(**payload.model_dump())
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


# ── Buscar resultado por ID ───────────────────────────────────────────────────

@app.get("/api/result/{test_id}", response_model=SpeedTestResponse)
async def get_result(test_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SpeedTest).where(SpeedTest.test_id == test_id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Teste não encontrado")
    return record


# ── Gerar ID único ────────────────────────────────────────────────────────────

@app.get("/api/new-test-id")
async def new_test_id():
    return {"test_id": str(uuid.uuid4())}


# ── Info do cliente ───────────────────────────────────────────────────────────

@app.get("/api/client-info")
async def client_info(request: Request):
    ip = get_client_ip(request)
    return {"ip": ip, "user_agent": request.headers.get("user-agent", "")}
