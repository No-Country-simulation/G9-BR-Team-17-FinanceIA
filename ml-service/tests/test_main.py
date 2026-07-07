from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/ml/health")
    assert response.status_code in (200, 503)


def test_analise_completa():
    response = client.post("/ml/analise", json={
        "renda_mensal": 8000,
        "nivel_endividamento": 5,
        "frequencia_poupanca": "Alta",
        "transacoes": [
            {"descricao": "Aluguel", "valor": 1500},
            {"descricao": "Farmacia", "valor": 120},
        ],
    })
    assert response.status_code == 200
    data = response.json()
    assert "perfil_financeiro" in data
    assert "probabilidade" in data
    assert "transacoes_classificadas" in data


def test_analise_sem_transacoes():
    response = client.post("/ml/analise", json={
        "renda_mensal": 8000,
        "nivel_endividamento": 5,
        "frequencia_poupanca": "Alta",
        "transacoes": [],
    })
    assert response.status_code == 422


def test_analise_valor_negativo():
    response = client.post("/ml/analise", json={
        "renda_mensal": 8000,
        "nivel_endividamento": 5,
        "frequencia_poupanca": "Alta",
        "transacoes": [{"descricao": "Teste", "valor": -100}],
    })
    assert response.status_code == 422
