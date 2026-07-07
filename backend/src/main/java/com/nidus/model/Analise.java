package com.nidus.model;

import jakarta.persistence.*;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import java.math.BigDecimal;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "analise")
public class Analise {

    @Id
    private UUID id;

    @Column(name = "criado_em", nullable = false)
    private Instant criadoEm;

    @Column(name = "requisicao", columnDefinition = "JSONB", nullable = false)
    @JdbcTypeCode(SqlTypes.JSON)
    private String requisicao;

    @Column(name = "resposta", columnDefinition = "JSONB", nullable = false)
    @JdbcTypeCode(SqlTypes.JSON)
    private String resposta;

    @Column(name = "perfil_financeiro", length = 20, nullable = false)
    private String perfilFinanceiro;

    @Column(name = "probabilidade", precision = 4, scale = 2, nullable = false)
    private BigDecimal probabilidade;

    public Analise() {}

    @PrePersist
    public void prePersist() {
        if (id == null) id = UUID.randomUUID();
        if (criadoEm == null) criadoEm = Instant.now();
    }

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    public Instant getCriadoEm() { return criadoEm; }
    public void setCriadoEm(Instant criadoEm) { this.criadoEm = criadoEm; }
    public String getRequisicao() { return requisicao; }
    public void setRequisicao(String requisicao) { this.requisicao = requisicao; }
    public String getResposta() { return resposta; }
    public void setResposta(String resposta) { this.resposta = resposta; }
    public String getPerfilFinanceiro() { return perfilFinanceiro; }
    public void setPerfilFinanceiro(String perfilFinanceiro) { this.perfilFinanceiro = perfilFinanceiro; }
    public BigDecimal getProbabilidade() { return probabilidade; }
    public void setProbabilidade(BigDecimal probabilidade) { this.probabilidade = probabilidade; }

    @Transient
    public java.util.Map<String, BigDecimal> getResumoGastos() {
        return new java.util.HashMap<>();
    }
}
