import type {
  AnaliseFinanceiraRequest,
  AnaliseFinanceiraResponse,
  ClassificacaoTransacoesRequest,
  ClassificacaoTransacoesResponse,
  ErroResponse,
  HistoricoResponse,
} from "../types";

const API_BASE = "/api";

async function request<T>(url: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_BASE}${url}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const erro: ErroResponse = await response.json();
    throw erro;
  }

  return response.json();
}

export async function analisarFinanceiro(
  dados: AnaliseFinanceiraRequest
): Promise<AnaliseFinanceiraResponse> {
  return request<AnaliseFinanceiraResponse>("/analise-financeira", dados);
}

export async function classificarTransacoes(
  dados: ClassificacaoTransacoesRequest
): Promise<ClassificacaoTransacoesResponse> {
  return request<ClassificacaoTransacoesResponse>("/classificacao-transacoes", dados);
}

export async function getHistorico(): Promise<HistoricoResponse> {
  const response = await fetch(`${API_BASE}/historico-analises`);

  if (!response.ok) {
    const erro: ErroResponse = await response.json();
    throw erro;
  }

  return response.json();
}
