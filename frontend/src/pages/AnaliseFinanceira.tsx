import { useState } from "react";
import type { AnaliseFinanceiraResponse, Transacao } from "../types";
import { analisarFinanceiro } from "../services/api";
import FormTransacoes from "../components/FormTransacoes";
import ResultadoPerfil from "../components/ResultadoPerfil";
import ResumoGastos from "../components/ResumoGastos";
import ListaPadroesConsumo from "../components/ListaPadroesConsumo";
import ListaRecomendacoes from "../components/ListaRecomendacoes";
import ErrorAlert from "../components/ErrorAlert";

export default function AnaliseFinanceira() {
  const [rendaMensal, setRendaMensal] = useState("");
  const [nivelEndividamento, setNivelEndividamento] = useState("0");
  const [frequenciaPoupanca, setFrequenciaPoupanca] = useState("Media");
  const [transacoes, setTransacoes] = useState<Transacao[]>([]);
  const [resultado, setResultado] = useState<AnaliseFinanceiraResponse | null>(null);
  const [erro, setErro] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErro("");
    setResultado(null);
    setLoading(true);

    try {
      const data = await analisarFinanceiro({
        rendaMensal: parseFloat(rendaMensal),
        nivelEndividamento: parseFloat(nivelEndividamento),
        frequenciaPoupanca: frequenciaPoupanca as "Nenhuma" | "Baixa" | "Media" | "Alta",
        transacoes,
      });
      setResultado(data);
    } catch (err: unknown) {
      const e = err as { erro?: { mensagem?: string; codigo?: string } };
      setErro(e?.erro?.mensagem || e?.erro?.codigo || "Erro ao processar análise");
    } finally {
      setLoading(false);
    }
  }

  function novaAnalise() {
    setResultado(null);
    setErro("");
    setTransacoes([]);
    setRendaMensal("");
    setNivelEndividamento("0");
    setFrequenciaPoupanca("Media");
  }

  if (resultado) {
    return (
      <div>
        <h2>Resultado da Análise</h2>
        <ResultadoPerfil perfil={resultado.perfilFinanceiro} probabilidade={resultado.probabilidade} />
        <ResumoGastos gastos={resultado.resumoGastos} />
        <ListaPadroesConsumo padroes={resultado.padroesIdentificados} />
        <ListaRecomendacoes recomendacoes={resultado.recomendacoes} />
        <button onClick={novaAnalise} style={{ padding: "0.5rem 1rem" }}>
          Nova Análise
        </button>
      </div>
    );
  }

  return (
    <div>
      <h2>Análise Financeira</h2>
      {erro && <ErrorAlert mensagem={erro} />}
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "1rem" }}>
          <label>Renda Mensal</label>
          <input
            type="number"
            min="0.01"
            step="0.01"
            value={rendaMensal}
            onChange={(e) => setRendaMensal(e.target.value)}
            required
            style={{ display: "block", width: "100%", padding: "0.5rem", marginTop: "0.25rem" }}
          />
        </div>
        <div style={{ marginBottom: "1rem" }}>
          <label>Nível de Endividamento (%)</label>
          <input
            type="range"
            min="0"
            max="100"
            value={nivelEndividamento}
            onChange={(e) => setNivelEndividamento(e.target.value)}
            style={{ display: "block", width: "100%", marginTop: "0.25rem" }}
          />
          <span>{nivelEndividamento}%</span>
        </div>
        <div style={{ marginBottom: "1rem" }}>
          <label>Frequência de Poupança</label>
          <select
            value={frequenciaPoupanca}
            onChange={(e) => setFrequenciaPoupanca(e.target.value)}
            style={{ display: "block", width: "100%", padding: "0.5rem", marginTop: "0.25rem" }}
          >
            <option value="Nenhuma">Nenhuma</option>
            <option value="Baixa">Baixa</option>
            <option value="Media">Media</option>
            <option value="Alta">Alta</option>
          </select>
        </div>
        <div style={{ marginBottom: "1rem" }}>
          <label>Transações</label>
          <FormTransacoes transacoes={transacoes} onChange={setTransacoes} />
        </div>
        <button type="submit" disabled={loading} style={{ padding: "0.5rem 2rem" }}>
          {loading ? "Analisando..." : "Analisar"}
        </button>
      </form>
    </div>
  );
}
