import { Link } from "react-router-dom";
import type { ReactNode } from "react";

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div style={{ minHeight: "100vh", fontFamily: "sans-serif" }}>
      <nav style={{ padding: "1rem 2rem", borderBottom: "1px solid #ddd", marginBottom: "1rem" }}>
        <Link to="/" style={{ fontWeight: "bold", fontSize: "1.2rem", textDecoration: "none", color: "#333" }}>
          Nidus
        </Link>
        <span style={{ margin: "0 1rem" }}>|</span>
        <Link to="/analise-financeira" style={{ textDecoration: "none", color: "#555" }}>
          Análise Financeira
        </Link>
        <span style={{ margin: "0 0.5rem" }}>|</span>
        <Link to="/classificacao-transacoes" style={{ textDecoration: "none", color: "#555" }}>
          Classificação de Transações
        </Link>
        <span style={{ margin: "0 0.5rem" }}>|</span>
        <Link to="/historico-analises" style={{ textDecoration: "none", color: "#555" }}>
          Histórico
        </Link>
      </nav>
      <main style={{ maxWidth: "800px", margin: "0 auto", padding: "0 1rem" }}>
        {children}
      </main>
    </div>
  );
}
