package com.nidus.service;

import com.nidus.dto.*;
import com.nidus.model.Analise;
import com.nidus.repository.AnaliseRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;
import java.math.BigDecimal;
import java.util.HashMap;

@Service
public class AnaliseFinanceiraService {

    private final MlServiceClient mlServiceClient;
    private final IdentificadorPadroesConsumo identificadorPadroes;
    private final GeradorRecomendacoes geradorRecomendacoes;
    private final AnaliseRepository repository;
    private final ObjectMapper objectMapper;

    public AnaliseFinanceiraService(MlServiceClient mlServiceClient,
                                    IdentificadorPadroesConsumo identificadorPadroes,
                                    GeradorRecomendacoes geradorRecomendacoes,
                                    AnaliseRepository repository,
                                    ObjectMapper objectMapper) {
        this.mlServiceClient = mlServiceClient;
        this.identificadorPadroes = identificadorPadroes;
        this.geradorRecomendacoes = geradorRecomendacoes;
        this.repository = repository;
        this.objectMapper = objectMapper;
    }

    public AnaliseFinanceiraResponse analisar(AnaliseFinanceiraRequest request) {
        var mlRequest = new MlAnaliseRequest(
            request.getRendaMensal(),
            request.getNivelEndividamento(),
            request.getFrequenciaPoupanca(),
            request.getTransacoes()
        );

        var mlResponse = mlServiceClient.analisar(mlRequest);

        var resumoGastos = new HashMap<String, BigDecimal>();
        if (mlResponse.getTransacoesClassificadas() != null) {
            for (var t : mlResponse.getTransacoesClassificadas()) {
                var cat = t.getCategoria();
                resumoGastos.merge(cat, t.getValor(), BigDecimal::add);
            }
        }

        var padroes = identificadorPadroes.identificar(mlResponse, request.getRendaMensal());

        var recomendacoes = geradorRecomendacoes.gerar(
            mlResponse.getPerfilFinanceiro(),
            mlResponse.getProbabilidade(),
            request.getNivelEndividamento(),
            request.getFrequenciaPoupanca(),
            request.getRendaMensal(),
            resumoGastos
        );

        var response = new AnaliseFinanceiraResponse(
            mlResponse.getPerfilFinanceiro(),
            mlResponse.getProbabilidade(),
            resumoGastos,
            padroes,
            recomendacoes
        );

        try {
            var analise = new Analise();
            analise.setRequisicao(objectMapper.writeValueAsString(request));
            analise.setResposta(objectMapper.writeValueAsString(response));
            analise.setPerfilFinanceiro(response.getPerfilFinanceiro());
            analise.setProbabilidade(response.getProbabilidade());
            repository.save(analise);
        } catch (Exception e) {
            throw new RuntimeException("Erro ao persistir analise", e);
        }

        return response;
    }
}
