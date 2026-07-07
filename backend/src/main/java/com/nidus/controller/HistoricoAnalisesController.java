package com.nidus.controller;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.nidus.repository.AnaliseRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

@RestController
public class HistoricoAnalisesController {

    private final AnaliseRepository repository;
    private final ObjectMapper objectMapper;

    public HistoricoAnalisesController(AnaliseRepository repository, ObjectMapper objectMapper) {
        this.repository = repository;
        this.objectMapper = objectMapper;
    }

    @GetMapping("/historico-analises")
    public ResponseEntity<HistoricoResponse> listar() {
        var analises = repository.findAllByOrderByCriadoEmDesc();
        var historico = analises.stream()
            .map(a -> {
                Map<String, BigDecimal> resumoGastos = Map.of();
                try {
                    var respostaJson = objectMapper.readTree(a.getResposta());
                    var resumoNode = respostaJson.get("resumoGastos");
                    if (resumoNode != null) {
                        resumoGastos = objectMapper.convertValue(
                            resumoNode, new TypeReference<Map<String, BigDecimal>>() {});
                    }
                } catch (Exception ignored) {}
                return new HistoricoItem(
                    a.getId().toString(),
                    a.getCriadoEm().toString(),
                    a.getPerfilFinanceiro(),
                    resumoGastos
                );
            })
            .toList();
        return ResponseEntity.ok(new HistoricoResponse(historico));
    }

    public record HistoricoResponse(List<HistoricoItem> analises) {}
    public record HistoricoItem(String id, String criadoEm, String perfilFinanceiro,
                                Map<String, BigDecimal> resumoGastos) {}
}
