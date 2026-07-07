import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional

from predictor import carregar_modelos, classificar_transacoes, classificar_perfil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

modelos_carregados = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    global modelos_carregados
    carregar_modelos()
    modelos_carregados = True
    yield


app = FastAPI(title="Nidus ML Service", lifespan=lifespan)


class Transacao(BaseModel):
    descricao: str = Field(..., min_length=1, max_length=120)
    valor: float = Field(..., gt=0)


class AnaliseRequest(BaseModel):
    renda_mensal: float = Field(..., gt=0)
    nivel_endividamento: float = Field(..., ge=0, le=100)
    frequencia_poupanca: str = Field(...)
    transacoes: List[Transacao] = Field(..., min_length=1)


class TransacaoClassificada(BaseModel):
    descricao: str
    valor: float
    categoria: str


class AnaliseResponse(BaseModel):
    perfil_financeiro: str
    probabilidade: float
    transacoes_classificadas: List[TransacaoClassificada]


class ErroDetail(BaseModel):
    codigo: str
    mensagem: str
    campo: Optional[str] = None
    timestamp: str


class ErroResponse(BaseModel):
    erro: ErroDetail


@app.get("/ml/health")
def health():
    if modelos_carregados:
        return {"status": "ok"}
    return JSONResponse(status_code=503, content={"status": "loading"})


@app.post("/ml/analise", response_model=AnaliseResponse)
def analise(request: AnaliseRequest):
    if request.frequencia_poupanca not in ("Nenhuma", "Baixa", "Media", "Alta"):
        raise HTTPException(
            status_code=422,
            detail={
                "codigo": "ENUM_INVALIDO",
                "mensagem": "Frequencia de poupanca invalida",
                "campo": "frequencia_poupanca",
            },
        )

    transacoes_dict = [t.model_dump() for t in request.transacoes]

    classificadas = classificar_transacoes(transacoes_dict)

    perfil, prob = classificar_perfil(
        request.renda_mensal,
        request.nivel_endividamento,
        request.frequencia_poupanca,
        classificadas,
    )

    return AnaliseResponse(
        perfil_financeiro=perfil,
        probabilidade=prob,
        transacoes_classificadas=[
            TransacaoClassificada(**t) for t in classificadas
        ],
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "erro": exc.detail
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error("Erro interno: %s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "erro": {
                "codigo": "FALHA_INTERNA_PROCESSAMENTO",
                "mensagem": "Erro inesperado no servico de ML",
                "campo": None,
                "timestamp": None,
            }
        },
    )
