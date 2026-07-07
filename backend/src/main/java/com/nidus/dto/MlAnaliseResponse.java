package com.nidus.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.math.BigDecimal;
import java.util.List;

public class MlAnaliseResponse {

    @JsonProperty("perfil_financeiro")
    private String perfilFinanceiro;
    private BigDecimal probabilidade;
    @JsonProperty("transacoes_classificadas")
    private List<MlTransacaoClassificada> transacoesClassificadas;

    public MlAnaliseResponse() {}

    public String getPerfilFinanceiro() { return perfilFinanceiro; }
    public void setPerfilFinanceiro(String perfilFinanceiro) { this.perfilFinanceiro = perfilFinanceiro; }
    public BigDecimal getProbabilidade() { return probabilidade; }
    public void setProbabilidade(BigDecimal probabilidade) { this.probabilidade = probabilidade; }
    public List<MlTransacaoClassificada> getTransacoesClassificadas() { return transacoesClassificadas; }
    public void setTransacoesClassificadas(List<MlTransacaoClassificada> transacoesClassificadas) {
        this.transacoesClassificadas = transacoesClassificadas;
    }

    public static class MlTransacaoClassificada {
        private String descricao;
        private BigDecimal valor;
        private String categoria;

        public MlTransacaoClassificada() {}

        public String getDescricao() { return descricao; }
        public void setDescricao(String descricao) { this.descricao = descricao; }
        public BigDecimal getValor() { return valor; }
        public void setValor(BigDecimal valor) { this.valor = valor; }
        public String getCategoria() { return categoria; }
        public void setCategoria(String categoria) { this.categoria = categoria; }
    }
}
