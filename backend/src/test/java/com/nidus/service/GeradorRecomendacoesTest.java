package com.nidus.service;

import static org.assertj.core.api.Assertions.assertThat;
import java.math.BigDecimal;
import java.util.Map;
import org.junit.jupiter.api.Test;

class GeradorRecomendacoesTest {

    private final GeradorRecomendacoes gerador = new GeradorRecomendacoes();

    @Test
    void dadoPerfilSaudavelEPoupancaAlta_deveRecomendarManterPadrao() {
        var recomendacoes = gerador.gerar("Saudavel", new BigDecimal("0.91"),
            new BigDecimal("5"), "Alta", Map.of("moradia", new BigDecimal("1500")));
        assertThat(recomendacoes).anyMatch(r -> r.contains("Manter o padrao atual de poupanca"));
    }

    @Test
    void dadoPerfilRisco_deveRecomendarQuitacaoDividas() {
        var recomendacoes = gerador.gerar("Em risco", new BigDecimal("0.88"),
            new BigDecimal("68"), "Nenhuma", Map.of("servicos", new BigDecimal("900")));
        assertThat(recomendacoes).anyMatch(r -> r.contains("Priorizar quitacao de dividas"));
    }

    @Test
    void dadoEndividamentoAlto_deveRecomendarReduzirEndividamento() {
        var recomendacoes = gerador.gerar("Em observacao", new BigDecimal("0.70"),
            new BigDecimal("50"), "Media", Map.of("alimentacao", new BigDecimal("500")));
        assertThat(recomendacoes).anyMatch(r -> r.contains("Reduzir o nivel de endividamento"));
    }

    @Test
    void dadoPerfilRiscoSemPoupanca_deveRecomendarMetaPoupanca() {
        var recomendacoes = gerador.gerar("Em risco", new BigDecimal("0.85"),
            new BigDecimal("60"), "Nenhuma", Map.of());
        assertThat(recomendacoes).anyMatch(r -> r.contains("Estabelecer meta minima de poupanca"));
    }

    @Test
    void dadoGastoEmLazerElevado_deveRecomendarReduzirLazer() {
        var recomendacoes = gerador.gerar("Em observacao", new BigDecimal("0.75"),
            new BigDecimal("20"), "Media", Map.of("Lazer", new BigDecimal("1500")));
        assertThat(recomendacoes).anyMatch(r -> r.contains("Reduzir gastos com lazer"));
    }

    @Test
    void quandoNenhumGatilhoAtivado_deveRetornarRecomendacaoGenerica() {
        var recomendacoes = gerador.gerar("Saudavel", new BigDecimal("0.95"),
            new BigDecimal("5"), "Alta", Map.of());
        assertThat(recomendacoes).anyMatch(r -> r.contains("Manter o padrao atual de poupanca"));
    }
}
