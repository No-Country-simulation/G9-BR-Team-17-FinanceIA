import joblib
import logging
from pathlib import Path
from sklearn.linear_model import LogisticRegression

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
            if isinstance(data, dict) and "modelo" in data:
                modelo_transacoes = data["modelo"]
                vectorizer = data["vectorizer"]
                logger.info("Modelo de transacoes carregado (TfidfVectorizer + %s)",
                            type(modelo_transacoes).__name__)
            else:
                modelo_transacoes = data
                logger.info("Modelo de transacoes carregado (formato legado)")
        else:
            logger.warning("Modelo de transacoes nao encontrado: %s", MODELO_TRANSACOES_PATH)

        if MODELO_PERFIL_PATH.exists():
            modelo_perfil = joblib.load(MODELO_PERFIL_PATH)
            logger.info("Modelo de perfil carregado (%s)", type(modelo_perfil).__name__)
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
        desc_clean = "".join(c for c in desc if c.isalnum() or c.isspace()).strip()

        if modelo_transacoes is not None and vectorizer is not None:
            desc_vec = vectorizer.transform([desc_clean])
            cat_idx = modelo_transacoes.predict(desc_vec)[0]
            if isinstance(modelo_transacoes, LogisticRegression):
                probs = modelo_transacoes.predict_proba(desc_vec)[0]
                max_prob = max(probs)
                categorias = modelo_transacoes.classes_
                idx = list(categorias).index(cat_idx)
                if max_prob >= 0.5:
                    categoria = str(cat_idx)
                else:
                    categoria = CATEGORIA_PADRAO
            else:
                categoria = str(cat_idx)
        else:
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
    poupanca_order = {"Nenhuma": 0, "Baixa": 1, "Media": 2, "Alta": 3}
    freq_num = poupanca_order.get(frequencia_poupanca, 0)

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

    endividamento_norm = nivel_endividamento / 100.0

    if modelo_perfil is not None:
        import pandas as pd
        import numpy as np
        input_df = pd.DataFrame([{
            "renda_mensal": renda_mensal,
            "nivel_endividamento": endividamento_norm * 100,
            "proporcao_comprometimento_renda": proporcao_essenciais + proporcao_nao_essenciais,
            "proporcao_gastos_nao_essenciais": proporcao_nao_essenciais,
            "frequencia_poupanca_Nenhuma": 1 if freq_num == 0 else 0,
            "frequencia_poupanca_Baixa": 1 if freq_num == 1 else 0,
            "frequencia_poupanca_Media": 1 if freq_num == 2 else 0,
            "frequencia_poupanca_Alta": 1 if freq_num == 3 else 0,
        }])

        if hasattr(modelo_perfil, "predict_proba"):
            probas = modelo_perfil.predict_proba(input_df)[0]
            idx = int(np.argmax(probas))
            perfil = str(modelo_perfil.classes_[idx])
            probabilidade = round(float(probas[idx]), 2)
        else:
            perfil = str(modelo_perfil.predict(input_df)[0])
            probabilidade = 0.85
        return perfil, probabilidade

    risco = (
        endividamento_norm * 0.35
        + (1 - freq_num / 3.0) * 0.25
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
