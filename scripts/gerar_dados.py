"""
Script de geracao de dados sinteticos para treinamento dos modelos.
Gera datasets de transacoes e perfil financeiro.
"""
import csv
import random
import os

random.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CATEGORIAS = {
    "Alimentacao": [
        "Supermercado", "Restaurante", "Padaria", "Ifood", "Feira",
        "Acougue", "Hortifruti", "Pizzaria", "Lanche", "Sushi",
    ],
    "Transporte": [
        "Combustivel", "Uber", "Gasolina", "Estacionamento", "Onibus",
        "Oficina Mecanica", "Pedagio", "Metro", "99", "Manutencao",
    ],
    "Saude": [
        "Farmacia", "Consulta Medica", "Plano de Saude", "Academia",
        "Hospital", "Exame", "Dentista", "Psicologo", "Medicamento",
    ],
    "Moradia": [
        "Aluguel", "Condominio", "Energia Eletrica", "Agua",
        "Gas", "Reforma", "IPTU",
    ],
    "Educacao": [
        "Mensalidade Escolar", "Curso Online", "Livros", "Faculdade",
        "Material Didatico", "Aula Particular", "Idiomas",
    ],
    "Lazer": [
        "Streaming", "Cinema", "Show", "Viagem", "Hotel",
        "Netflix", "Spotify", "Parque", "Teatro",
    ],
    "Servicos": [
        "Cartao de Credito", "Tarifa Bancaria", "Assinatura Software",
        "Seguro", "Convenio", "Fatura Cartao",
    ],
    "Outras": [
        "Pagamento Diverso", "Transferencia", "PIX", "Boleto Avulso",
    ],
}

def gerar_transacoes(qtd=2000):
    rows = []
    for _ in range(qtd):
        cat = random.choice(list(CATEGORIAS.keys()))
        desc = random.choice(CATEGORIAS[cat])
        if random.random() < 0.2:
            desc = desc.upper() if random.random() < 0.5 else desc.lower()
        if random.random() < 0.1:
            desc += "!!!" if random.random() < 0.5 else "  "
        valor = round(random.uniform(10, 2000), 2)
        rows.append({"descricao": desc.strip(), "valor": valor, "categoria": cat})
    return rows

def gerar_perfil(qtd=500):
    rows = []
    for _ in range(qtd):
        renda = round(random.uniform(1200, 15000), 2)
        endividamento = round(random.uniform(0, 100), 1)
        poupanca = random.choice(["Nenhuma", "Baixa", "Media", "Alta"])

        n_transacoes = random.randint(2, 8)
        transacoes = gerar_transacoes(n_transacoes)
        total_gastos = sum(t["valor"] for t in transacoes)
        gastos_essenciais = sum(
            t["valor"] for t in transacoes
            if t["categoria"] in ("Alimentacao", "Moradia", "Saude", "Transporte", "Educacao")
        )
        gastos_nao_essenciais = sum(
            t["valor"] for t in transacoes
            if t["categoria"] in ("Lazer", "Servicos")
        )

        proporcao_comprometimento = total_gastos / renda if renda > 0 else 0
        proporcao_nao_essenciais = gastos_nao_essenciais / renda if renda > 0 else 0

        freq_score = {"Nenhuma": 0, "Baixa": 0.25, "Media": 0.5, "Alta": 1.0}[poupanca]
        risco = (
            (endividamento / 100.0) * 0.35
            + (1 - freq_score) * 0.25
            + proporcao_nao_essenciais * 0.20
            + (proporcao_comprometimento * 0.10)
            + min(gastos_essenciais / renda, 1) * 0.10
        )

        if risco < 0.30:
            perfil = "Saudavel"
        elif risco < 0.55:
            perfil = "Em observacao"
        else:
            perfil = "Em risco"

        rows.append({
            "renda_mensal": renda,
            "nivel_endividamento": endividamento,
            "frequencia_poupanca": poupanca,
            "proporcao_comprometimento_renda": round(proporcao_comprometimento, 4),
            "proporcao_gastos_nao_essenciais": round(proporcao_nao_essenciais, 4),
            "perfil_financeiro": perfil,
        })
    return rows

def salvar_csv(nome, dados, fieldnames):
    path = os.path.join(OUTPUT_DIR, nome)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dados)
    print(f"Gerado: {path} ({len(dados)} linhas)")

if __name__ == "__main__":
    transacoes = gerar_transacoes(2000)
    salvar_csv("transacoes.csv", transacoes,
               ["descricao", "valor", "categoria"])

    perfis = gerar_perfil(500)
    salvar_csv("perfil.csv", perfis,
               ["renda_mensal", "nivel_endividamento", "frequencia_poupanca",
                "proporcao_comprometimento_renda", "proporcao_gastos_nao_essenciais",
                "perfil_financeiro"])

    print("Dataset gerado com sucesso!")
