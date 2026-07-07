export interface Transacao {
  descricao: string;
  valor: number;
}

export interface AnaliseFinanceiraRequest {
  rendaMensal: number;
  nivelEndividamento: number;
  frequenciaPoupanca: "Nenhuma" | "Baixa" | "Media" | "Alta";
  transacoes: Transacao[];
}

export interface AnaliseFinanceiraResponse {
  perfilFinanceiro: "Saudavel" | "Em observacao" | "Em risco";
  probabilidade: number;
  resumoGastos: Record<string, number>;
  padroesIdentificados: string[];
  recomendacoes: string[];
}

export interface ClassificacaoTransacoesRequest {
  transacoes: Transacao[];
}

export interface ClassificacaoTransacoesResponse {
  transacoesClassificadas: (Transacao & { categoria: string })[];
}

export interface ErroResponse {
  erro: {
    codigo: string;
    mensagem: string;
    campo: string | null;
    timestamp: string;
  };
}

export interface HistoricoItem {
  id: string;
  criadoEm: string;
  perfilFinanceiro: string;
  resumoGastos: Record<string, number>;
}

export interface HistoricoResponse {
  analises: HistoricoItem[];
}
