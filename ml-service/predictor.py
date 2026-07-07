import joblib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

MODELO_TRANSACOES_PATH = Path("models/modelo_transacoes.pkl")
MODELO_PERFIL_PATH = Path("models/modelo_perfil.pkl")

modelo_transacoes = None
modelo_perfil = None
vectorizer = None


def carregar_modelos():
    global modelo_transacoes, modelo_perfil, vectorizer

    try:
        if MODELO_TRANSACOES_PATH.exists():
            data = joblib.load(MODELO_TRANSACOES_PATH)
            if isinstance(data, dict):
                modelo_transacoes = data.get("modelo")
                vectorizer = data.get("vectorizer")
            else:
                modelo_transacoes = data
            logger.info("Modelo de transacoes carregado")
        else:
            logger.warning("Modelo de transacoes nao encontrado: %s", MODELO_TRANSACOES_PATH)

        if MODELO_PERFIL_PATH.exists():
            modelo_perfil = joblib.load(MODELO_PERFIL_PATH)
            logger.info("Modelo de perfil carregado")
        else:
            logger.warning("Modelo de perfil nao encontrado: %s", MODELO_PERFIL_PATH)

    except Exception as e:
        logger.error("Erro ao carregar modelos: %s", e)


def classificar_transacoes(transacoes):
    CACHE_KEYWORDS = {
        "Alimentacao": ["supermercado", "restaurante", "padaria", "ifood", "feira",
                        "acougue", "hortifruti", "delivery", "comida", "almoco",
                        "jantar", "cafe", "lanche", "pizzaria", "sorvete"],
        "Transporte": ["combustivel", "uber", "gasolina", "estacionamento", "onibus",
                       "oficina", "pedagio", "metro", "taxi", "99", "mecanica",
                       "passagem", "trem", "bicicleta", "manutencao veicular"],
        "Saude": ["farmacia", "medico", "consulta", "plano de saude", "academia",
                  "hospital", "exame", "dentista", "psicologo", "remedio",
                  "medicamento", "clinica", "fisioterapia", "vacina", "oftalmologista"],
        "Moradia": ["aluguel", "condominio", "energia", "agua", "gas", "reforma",
                    "eletrica", "iptu", "ipva", "manutencao", "predial", "casa",
                    "apartamento", "imovel", "escritorio"],
        "Educacao": ["mensalidade", "curso", "escola", "faculdade", "livro",
                     "material didatico", "aula", "universidade", "matricula",
                     "intercambio", "idiomas", "tecnico", "graduacao", "pos graduacao"],
        "Lazer": ["streaming", "cinema", "show", "teatro", "viagem", "hotel",
                  "resort", "parque", "jogo", "game", "netflix", "spotify",
                  "youtube", "prime", "disney", "hbo", "festa", "bar"],
        "Servicos": ["cartao de credito", "tarifa", "assinatura", "seguro",
                     "convenio", "nubank", "inter", "itau", "bradesco", "santander",
                     "banco", "fatura", "financeira", "emprestimo"],
    }

    CATEGORIA_PADRAO = "Outras"

    resultados = []
    for t in transacoes:
        desc = t.get("descricao", "").lower().strip()
        desc = "".join(c for c in desc if c.isalnum() or c.isspace()).strip()

        categoria = CATEGORIA_PADRAO
        maior_pontuacao = 0

        for cat, keywords in CACHE_KEYWORDS.items():
            pontuacao = sum(1 for kw in keywords if kw in desc)
            if pontuacao > maior_pontuacao:
                maior_pontuacao = pontuacao
                categoria = cat

        resultados.append({
            "descricao": t.get("descricao", ""),
            "valor": float(t.get("valor", 0)),
            "categoria": categoria
        })

    return resultados


def classificar_perfil(renda_mensal, nivel_endividamento, frequencia_poupanca,
                       transacoes_classificadas):
    from math import exp

    total_gastos = sum(t.get("valor", 0) for t in transacoes_classificadas)

    proporcao_essenciais = 0
    proporcao_nao_essenciais = 0
    if renda_mensal > 0:
        gastos_essenciais = sum(
            t.get("valor", 0) for t in transacoes_classificadas
            if t.get("categoria") in ("Alimentacao", "Moradia", "Saude",
                                       "Transporte", "Educacao")
        )
        gastos_nao_essenciais = sum(
            t.get("valor", 0) for t in transacoes_classificadas
            if t.get("categoria") in ("Lazer", "Servicos")
        )
        proporcao_essenciais = gastos_essenciais / renda_mensal
        proporcao_nao_essenciais = gastos_nao_essenciais / renda_mensal

    poupanca_score = {"Nenhuma": 0, "Baixa": 0.25, "Media": 0.5, "Alta": 1.0}
    freq_score = poupanca_score.get(frequencia_poupanca, 0)

    endividamento_norm = nivel_endividamento / 100.0

    risco = (
        endividamento_norm * 0.35
        + (1 - freq_score) * 0.25
        + proporcao_nao_essenciais * 0.20
        + proporcao_essenciais * 0.10
        + (total_gastos / renda_mensal if renda_mensal > 0 else 0) * 0.10
    )

    if risco < 0.30:
        perfil = "Saudavel"
        probabilidade = 0.70 + (0.30 - risco) * 1.5
    elif risco < 0.55:
        perfil = "Em observacao"
        probabilidade = 0.60 + (0.55 - risco) * 2.0
    else:
        perfil = "Em risco"
        probabilidade = 0.70 + (risco - 0.55) * 1.5

    probabilidade = max(0.0, min(1.0, probabilidade))
    probabilidade = round(probabilidade, 2)

    return perfil, probabilidade
