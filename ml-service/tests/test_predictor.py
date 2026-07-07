from predictor import classificar_transacoes, classificar_perfil


def test_classificar_alimentacao():
    transacoes = [{"descricao": "Supermercado", "valor": 420}]
    resultado = classificar_transacoes(transacoes)
    assert resultado[0]["categoria"] == "Alimentacao"


def test_classificar_transporte():
    transacoes = [{"descricao": "Combustivel", "valor": 200}]
    resultado = classificar_transacoes(transacoes)
    assert resultado[0]["categoria"] == "Transporte"


def test_classificar_outras():
    transacoes = [{"descricao": "Descricao completamente desconhecida", "valor": 100}]
    resultado = classificar_transacoes(transacoes)
    assert resultado[0]["categoria"] == "Outras"


def test_classificar_perfil_saudavel():
    perfil, prob = classificar_perfil(
        renda_mensal=8000,
        nivel_endividamento=5,
        frequencia_poupanca="Alta",
        transacoes_classificadas=[
            {"descricao": "Aluguel", "valor": 1500, "categoria": "Moradia"}
        ],
    )
    assert perfil == "Saudavel"
    assert 0 <= prob <= 1


def test_classificar_perfil_risco():
    perfil, prob = classificar_perfil(
        renda_mensal=3000,
        nivel_endividamento=80,
        frequencia_poupanca="Nenhuma",
        transacoes_classificadas=[
            {"descricao": "Cartao de credito", "valor": 900, "categoria": "Servicos"},
            {"descricao": "Uber", "valor": 500, "categoria": "Transporte"},
            {"descricao": "Ifood", "valor": 600, "categoria": "Alimentacao"},
        ],
    )
    assert perfil == "Em risco"
    assert 0 <= prob <= 1


def test_probabilidade_no_range():
    perfil, prob = classificar_perfil(
        renda_mensal=4500,
        nivel_endividamento=25,
        frequencia_poupanca="Media",
        transacoes_classificadas=[
            {"descricao": "Supermercado", "valor": 420, "categoria": "Alimentacao"},
            {"descricao": "Streaming", "valor": 40, "categoria": "Lazer"},
        ],
    )
    assert 0 <= prob <= 1
    assert perfil in ("Saudavel", "Em observacao", "Em risco")
