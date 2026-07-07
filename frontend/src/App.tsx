import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import AnaliseFinanceira from "./pages/AnaliseFinanceira";
import ClassificacaoTransacoes from "./pages/ClassificacaoTransacoes";
import HistoricoAnalises from "./pages/HistoricoAnalises";

function Home() {
  return (
    <div style={{ padding: "2rem", textAlign: "center" }}>
      <h1>Nidus</h1>
      <p>Sistema de Análise de Comportamento Financeiro</p>
      <div style={{ display: "flex", gap: "1rem", justifyContent: "center", marginTop: "2rem" }}>
        <a href="/analise-financeira" style={cardStyle}>
          <h3>Análise Financeira</h3>
          <p>Classifique seu perfil financeiro e receba recomendações</p>
        </a>
        <a href="/classificacao-transacoes" style={cardStyle}>
          <h3>Classificação de Transações</h3>
          <p>Classifique transações por categoria</p>
        </a>
        <a href="/historico-analises" style={cardStyle}>
          <h3>Histórico</h3>
          <p>Consulte análises financeiras anteriores</p>
        </a>
      </div>
    </div>
  );
}

const cardStyle: React.CSSProperties = {
  display: "block",
  padding: "2rem",
  border: "1px solid #ccc",
  borderRadius: "8px",
  textDecoration: "none",
  color: "inherit",
  maxWidth: "300px",
};

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/analise-financeira" element={<AnaliseFinanceira />} />
        <Route path="/classificacao-transacoes" element={<ClassificacaoTransacoes />} />
        <Route path="/historico-analises" element={<HistoricoAnalises />} />
      </Routes>
    </Layout>
  );
}
