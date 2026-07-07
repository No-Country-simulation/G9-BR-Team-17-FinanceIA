package com.nidus.controller;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.nidus.dto.AnaliseFinanceiraRequest;
import com.nidus.dto.TransacaoRequest;
import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureMockMvc
@ActiveProfiles("test")
class AnaliseFinanceiraControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void deveRetornar200ComDadosValidos() throws Exception {
        var request = new AnaliseFinanceiraRequest();
        request.setRendaMensal(new BigDecimal("4500"));
        request.setNivelEndividamento(new BigDecimal("25"));
        request.setFrequenciaPoupanca("Media");
        request.setTransacoes(List.of(
            new TransacaoRequest("Supermercado", new BigDecimal("420"))
        ));

        mockMvc.perform(post("/analise-financeira")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.perfilFinanceiro").isString())
            .andExpect(jsonPath("$.probabilidade").isNumber())
            .andExpect(jsonPath("$.resumoGastos").isMap())
            .andExpect(jsonPath("$.recomendacoes").isArray());
    }

    @Test
    void deveRetornar422QuandoRendaInvalida() throws Exception {
        var request = new AnaliseFinanceiraRequest();
        request.setRendaMensal(new BigDecimal("-100"));
        request.setNivelEndividamento(new BigDecimal("25"));
        request.setFrequenciaPoupanca("Media");
        request.setTransacoes(List.of(
            new TransacaoRequest("Teste", new BigDecimal("10"))
        ));

        mockMvc.perform(post("/analise-financeira")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isUnprocessableEntity());
    }

    @Test
    void deveRetornar422QuandoTransacaoVazia() throws Exception {
        var request = new AnaliseFinanceiraRequest();
        request.setRendaMensal(new BigDecimal("4500"));
        request.setNivelEndividamento(new BigDecimal("25"));
        request.setFrequenciaPoupanca("Media");
        request.setTransacoes(List.of());

        mockMvc.perform(post("/analise-financeira")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isUnprocessableEntity())
            .andExpect(jsonPath("$.erro.codigo").value("LISTA_TRANSACOES_VAZIA"));
    }

    @Test
    void deveRetornar400QuandoJsonInvalido() throws Exception {
        mockMvc.perform(post("/analise-financeira")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{{ json invalido"))
            .andExpect(status().isBadRequest());
    }

    @Test
    void deveRetornar422QuandoFrequenciaPoupancaInvalida() throws Exception {
        var request = new AnaliseFinanceiraRequest();
        request.setRendaMensal(new BigDecimal("4500"));
        request.setNivelEndividamento(new BigDecimal("25"));
        request.setFrequenciaPoupanca("Invalida");
        request.setTransacoes(List.of(
            new TransacaoRequest("Teste", new BigDecimal("10"))
        ));

        mockMvc.perform(post("/analise-financeira")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isUnprocessableEntity());
    }
}
