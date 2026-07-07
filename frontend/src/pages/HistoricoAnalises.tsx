import { useState, useEffect, useCallback } from "react";
import type { HistoricoItem } from "../types";
import { getHistorico } from "../services/api";
import ErrorAlert from "../components/ErrorAlert";

export default function HistoricoAnalises() {
  const [analises, setAnalises] = useState<HistoricoItem[]>([]);
  const [erro, setErro] = useState("");
  const [loading, setLoading] = useState(true);
  const [expandido, setExpandido] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    setLoading(true);
    setErro("");
    try {
      const data = await getHistorico();
      setAnalises(data.analises);
    } catch (err: unknown) {
      const e = err as { erro?: { mensagem?: string } };
      setErro(e?.erro?.mensagem || "Erro ao carregar histórico");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { carregar(); }, [carregar]);

  return (
    <div>
      <h2>Histórico de Análises</h2>
      {erro && <ErrorAlert mensagem={erro} />}

      {loading && <p>Carregando...</p>}

      {!loading && analises.length === 0 && !erro && (
        <p>Nenhuma análise encontrada. Faça sua primeira análise financeira!</p>
      )}

      {analises.map((a) => (
        <div
          key={a.id}
          style={{
            border: "1px solid #ddd",
            borderRadius: "8px",
            padding: "1rem",
            marginBottom: "1rem",
            cursor: "pointer",
          }}
          onClick={() => setExpandido(expandido === a.id ? null : a.id)}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <strong>{a.perfilFinanceiro}</strong>
            <span style={{ color: "#666", fontSize: "0.9rem" }}>
              {new Date(a.criadoEm).toLocaleString("pt-BR")}
            </span>
          </div>

          {expandido === a.id && (
            <div style={{ marginTop: "1rem", paddingTop: "1rem", borderTop: "1px solid #eee" }}>
              <h4 style={{ margin: "0 0 0.5rem 0" }}>Resumo de Gastos</h4>
              {Object.keys(a.resumoGastos).length === 0 ? (
                <p style={{ color: "#666" }}>Nenhum gasto registrado</p>
              ) : (
                <table style={{ width: "100%", borderCollapse: "collapse" }}>
                  <thead>
                    <tr>
                      <th style={thStyle}>Categoria</th>
                      <th style={{ ...thStyle, textAlign: "right" }}>Valor</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(a.resumoGastos).map(([cat, valor]) => (
                      <tr key={cat}>
                        <td style={tdStyle}>{cat}</td>
                        <td style={{ ...tdStyle, textAlign: "right" }}>{valor.toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}
        </div>
      ))}

      {analises.length > 0 && (
        <button onClick={carregar} disabled={loading} style={{ padding: "0.5rem 1rem" }}>
          {loading ? "Recarregando..." : "Recarregar"}
        </button>
      )}
    </div>
  );
}

const thStyle: React.CSSProperties = {
  borderBottom: "2px solid #ddd",
  padding: "0.5rem",
  textAlign: "left",
};

const tdStyle: React.CSSProperties = {
  borderBottom: "1px solid #eee",
  padding: "0.5rem",
};
