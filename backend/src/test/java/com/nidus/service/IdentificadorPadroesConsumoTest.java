package com.nidus.service;

import static org.assertj.core.api.Assertions.assertThat;
import com.nidus.dto.MlAnaliseResponse;
import com.nidus.dto.MlAnaliseResponse.MlTransacaoClassificada;
import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.Test;

class IdentificadorPadroesConsumoTest {

    private final IdentificadorPadroesConsumo identificador = new IdentificadorPadroesConsumo();

    private MlAnaliseResponse criarResposta(List<MlTransacaoClassificada> transacoes) {
        var resp = new MlAnaliseResponse();
        resp.setTransacoesClassificadas(transacoes);
        return resp;
    }

    private MlTransacaoClassificada t(String desc, double valor, String cat) {
        var t = new MlTransacaoClassificada();
        t.setDescricao(desc);
        t.setValor(BigDecimal.valueOf(valor));
        t.setCategoria(cat);
        return t;
    }

    @Test
    void dadoConcentracaoEmLazer_deveIdentificarPC001() {
        var transacoes = List.of(
            t("Cinema", 400, "Lazer"),
            t("Supermercado", 100, "Alimentacao"),
            t("Onibus", 50, "Transporte")
        );
        var padroes = identificador.identificar(criarResposta(transacoes), new BigDecimal("5000"));
        assertThat(padroes).anyMatch(p -> p.contains("Concentracao em Lazer"));
    }

    @Test
    void dadoGastosDistribuidos_semConcentracao() {
        var transacoes = List.of(
            t("Supermercado", 100, "Alimentacao"),
            t("Onibus", 100, "Transporte"),
            t("Farmacia", 100, "Saude"),
            t("Aluguel", 100, "Moradia")
        );
        var padroes = identificador.identificar(criarResposta(transacoes), new BigDecimal("5000"));
        assertThat(padroes).noneMatch(p -> p.contains("Concentracao em"));
    }

    @Test
    void dadoDescricaoRepetida_deveIdentificarPC004() {
        var transacoes = List.of(
            t("Streaming", 40, "Lazer"),
            t("streaming", 45, "Lazer")
        );
        var padroes = identificador.identificar(criarResposta(transacoes), new BigDecimal("5000"));
        assertThat(padroes).anyMatch(p -> p.contains("Padrao recorrente"));
    }

    @Test
    void dadoValorAtipico_deveIdentificarPC005() {
        var transacoes = List.of(
            t("Supermercado", 100, "Alimentacao"),
            t("Onibus", 10, "Transporte"),
            t("Viagem", 3000, "Lazer")
        );
        var padroes = identificador.identificar(criarResposta(transacoes), new BigDecimal("5000"));
        assertThat(padroes).anyMatch(p -> p.contains("Transacao atipica"));
    }

    @Test
    void deveIdentificarCategoriaDominante() {
        var transacoes = List.of(
            t("Supermercado", 500, "Alimentacao"),
            t("Onibus", 100, "Transporte")
        );
        var padroes = identificador.identificar(criarResposta(transacoes), new BigDecimal("5000"));
        assertThat(padroes).anyMatch(p -> p.contains("Categoria de maior gasto: Alimentacao"));
    }
}
