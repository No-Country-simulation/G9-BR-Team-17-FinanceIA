package com.nidus.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import com.nidus.dto.AnaliseFinanceiraRequest;
import com.nidus.dto.MlAnaliseResponse;
import com.nidus.dto.MlAnaliseResponse.MlTransacaoClassificada;
import com.nidus.dto.TransacaoRequest;
import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.assertj.core.api.Assertions.assertThat;

@ExtendWith(MockitoExtension.class)
class AnaliseFinanceiraServiceTest {

    @Mock
    private MlServiceClient mlServiceClient;

    @Mock
    private IdentificadorPadroesConsumo identificadorPadroes;

    @Mock
    private GeradorRecomendacoes geradorRecomendacoes;

    @Mock
    private com.nidus.repository.AnaliseRepository repository;

    @Mock
    private com.fasterxml.jackson.databind.ObjectMapper objectMapper;

    @InjectMocks
    private AnaliseFinanceiraService service;

    @Test
    void deveRetornarAnaliseCompleta() {
        var request = new AnaliseFinanceiraRequest();
        request.setRendaMensal(new BigDecimal("4500"));
        request.setNivelEndividamento(new BigDecimal("25"));
        request.setFrequenciaPoupanca("Media");
        request.setTransacoes(List.of(
            new TransacaoRequest("Supermercado", new BigDecimal("420"))
        ));

        var mlResponse = new MlAnaliseResponse();
        mlResponse.setPerfilFinanceiro("Em observacao");
        mlResponse.setProbabilidade(new BigDecimal("0.82"));
        mlResponse.setTransacoesClassificadas(List.of(
            criarTransacao("Supermercado", 420, "Alimentacao")
        ));

        when(mlServiceClient.analisar(any())).thenReturn(mlResponse);
        when(identificadorPadroes.identificar(any(), any()))
            .thenReturn(List.of("Categoria de maior gasto: Alimentacao"));
        when(geradorRecomendacoes.gerar(any(), any(), any(), any(), any(), any()))
            .thenReturn(List.of("Monitorar gastos em Alimentacao"));

        var response = service.analisar(request);

        assertThat(response.getPerfilFinanceiro()).isEqualTo("Em observacao");
        assertThat(response.getProbabilidade()).isEqualByComparingTo(new BigDecimal("0.82"));
        assertThat(response.getResumoGastos()).containsKey("Alimentacao");
        assertThat(response.getPadroesIdentificados()).isNotEmpty();
        assertThat(response.getRecomendacoes()).isNotEmpty();
    }

    private MlTransacaoClassificada criarTransacao(String desc, double valor, String cat) {
        var t = new MlTransacaoClassificada();
        t.setDescricao(desc);
        t.setValor(BigDecimal.valueOf(valor));
        t.setCategoria(cat);
        return t;
    }
}
