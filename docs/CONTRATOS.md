# Documentação de Contratos de API
## Análise de Comportamento Financeiro e Recomendação Personalizada

---

## 1. Propósito deste Documento

Este documento detalha os contratos de entrada e saída de cada endpoint da API REST, definindo estrutura de dados, tipos, obrigatoriedade, restrições de valor e comportamento esperado em cenários de sucesso e de erro. O objetivo é eliminar ambiguidades antes do início da implementação, servindo como referência única entre as equipes de Ciência de Dados e Back-End.

Este documento não define tecnologia de implementação. Os formatos aqui descritos (JSON, códigos HTTP) são requisitos funcionais do projeto, não escolhas de infraestrutura.

---

## 2. Convenções Gerais

### 2.1 Formato de Dados

Todas as requisições e respostas utilizam o formato JSON, com codificação UTF-8.

### 2.2 Convenção de Nomenclatura de Campos

Os campos seguem `snake_case`, em português, conforme já estabelecido no exemplo de referência do projeto.

### 2.3 Códigos de Status HTTP Utilizados

| Código | Significado | Quando ocorre |
|---|---|---|
| 200 | OK | Requisição processada com sucesso |
| 400 | Bad Request | Estrutura da requisição malformada (ex: JSON inválido, campo com tipo incorreto) |
| 422 | Unprocessable Entity | Estrutura válida, porém com dados semanticamente inválidos (ex: valor negativo, campo obrigatório ausente) |
| 500 | Internal Server Error | Falha inesperada no processamento interno (ex: falha ao carregar o modelo) |
| 504 | Gateway Timeout | O ml-service nao respondeu dentro do limite de tempo configurado |

### 2.4 Estrutura Padrão de Erro

Toda resposta de erro (400, 422 ou 500) segue a mesma estrutura, independente do endpoint:

```json
{
  "erro": {
    "codigo": "CAMPO_INVALIDO",
    "mensagem": "O campo 'renda_mensal' deve ser um numero positivo.",
    "campo": "renda_mensal",
    "timestamp": "2026-07-06T14:32:10Z"
  }
}
```

| Campo | Tipo | Descrição |
|---|---|---|
| codigo | string | Identificador padronizado do tipo de erro (ver catálogo na seção 5) |
| mensagem | string | Descrição legível do problema, sem exposição de dados sensíveis |
| campo | string ou null | Nome do campo que originou o erro, quando aplicável |
| timestamp | string (ISO 8601) | Momento em que o erro foi gerado |

### 2.5 Fluxo Geral de Requisição (visão conceitual)

```mermaid
sequenceDiagram
    participant Cliente
    participant API
    participant Validador
    participant MotorAnalise as Motor de Analise

    Cliente->>API: POST requisicao (JSON)
    API->>Validador: Validar estrutura e dados
    alt Dados invalidos
        Validador-->>API: Erro estruturado
        API-->>Cliente: 400 ou 422 + corpo de erro
    else Dados validos
        Validador-->>API: OK
        API->>MotorAnalise: Processar analise
        MotorAnalise-->>API: Resultado
        API-->>Cliente: 200 + corpo de resposta
    end
```

---

## 3. Endpoint 1: Análise Financeira Completa

### 3.1 Identificação

| Item | Detalhe |
|---|---|
| Método | POST |
| Caminho | /analise-financeira |
| Descrição | Recebe os dados financeiros do usuário e retorna a classificação de perfil financeiro, o resumo de gastos por categoria e as recomendações associadas. |

### 3.2 Contrato de Entrada

```json
{
  "renda_mensal": 4500,
  "nivel_endividamento": 25,
  "frequencia_poupanca": "Media",
  "transacoes": [
    {
      "descricao": "Supermercado",
      "valor": 420
    }
  ]
}
```

| Campo | Tipo | Obrigatório | Restrições |
|---|---|---|---|
| renda_mensal | número decimal | Sim | Deve ser maior que 0 |
| nivel_endividamento | número decimal | Sim | Deve estar entre 0 e 100 (representa percentual da renda comprometida) |
| frequencia_poupanca | string (enum) | Sim | Valores aceitos: "Nenhuma", "Baixa", "Media", "Alta" |
| transacoes | lista de objetos | Sim | Deve conter no mínimo 1 transação |
| transacoes[].descricao | string | Sim | Não pode ser vazia; máximo de 120 caracteres |
| transacoes[].valor | número decimal | Sim | Deve ser maior que 0 |

### 3.3 Contrato de Saída (sucesso, 200)

```json
{
  "perfil_financeiro": "Em observacao",
  "probabilidade": 0.82,
  "resumo_gastos": {
    "alimentacao": 420,
    "transporte": 300,
    "lazer": 40
  },
  "padroes_identificados": [
    "Categoria de maior gasto: Alimentacao",
    "Comprometimento de renda com gastos essenciais: 16%"
  ],
  "recomendacoes": [
    "Monitorar gastos recorrentes de lazer",
    "Aumentar reserva financeira mensal"
  ]
}
```

| Campo | Tipo | Descrição |
|---|---|---|
| perfil_financeiro | string (enum) | Um dos valores: "Saudavel", "Em observacao", "Em risco" |
| probabilidade | número decimal (0 a 1) | Nível de confiança da classificação do perfil |
| resumo_gastos | objeto (chave dinâmica) | Mapa de categoria de despesa para valor total agregado. Somente categorias com transações presentes são exibidas (conforme RN de omissão de categorias vazias) |
| padroes_identificados | lista de string | Lista de padrões de consumo identificados na análise (ver domínio no DICIONARIO.md). Cada string segue formato descritivo definido na seção 10. Pode ser vazia se nenhum padrão for detectado. |
| recomendacoes | lista de string | Uma ou mais recomendações objetivas, vinculadas aos indicadores identificados |

### 3.4 Fluxo de Decisão Interna (visão conceitual)

```mermaid
flowchart TD
    A[Receber dados de entrada] --> B{Validacao estrutural e semantica}
    B -- Invalido --> C[Retornar 400/422 com erro estruturado]
    B -- Valido --> D[Classificar cada transacao por categoria]
    D --> E[Agregar resumo de gastos por categoria]
    E --> F[Identificar padroes de consumo]
    F --> G[Calcular indicadores: comprometimento de renda, padrao de poupanca]
    G --> H[Classificar perfil financeiro + probabilidade]
    H --> I[Gerar recomendacoes vinculadas aos indicadores e padroes]
    I --> J[Retornar 200 com corpo de resposta]
```

### 3.4.1 Fluxo de Identificacao de Padroes de Consumo

```mermaid
flowchart TD
    A[Transacoes classificadas por categoria] --> B[Calcular percentual por categoria]
    B --> C{Categoria > 30% do total?}
    C -- Sim --> D[Registrar padrao PC001: concentracao]
    C -- Nao --> E[Sem concentracao]
    B --> F[Calcular essenciais vs nao essenciais]
    F --> G[Registrar padrao PC002/PC003: comprometimento]
    A --> H{Descricao normalizada repetida?}
    H -- Sim --> I[Registrar padrao PC004: recorrencia]
    A --> J{Valor > 2x a media?}
    J -- Sim --> K[Registrar padrao PC005: atipica]
    A --> L[Categoria com maior soma]
    L --> M[Registrar padrao PC006: categoria dominante]
    D --> N[Lista consolidada de padroes identificados]
    G --> N
    I --> N
    K --> N
    M --> N
    N --> O[Utilizada por: classificacao de perfil e geracao de recomendacoes]
```

### 3.5 Exemplos Reais de Utilização

**Exemplo 1: Perfil "Em observação"**

Entrada:
```json
{
  "renda_mensal": 4500,
  "nivel_endividamento": 25,
  "frequencia_poupanca": "Media",
  "transacoes": [
    { "descricao": "Supermercado", "valor": 420 },
    { "descricao": "Combustivel", "valor": 300 },
    { "descricao": "Streaming", "valor": 40 }
  ]
}
```

Saída:
```json
{
  "perfil_financeiro": "Em observacao",
  "probabilidade": 0.82,
  "resumo_gastos": {
    "alimentacao": 420,
    "transporte": 300,
    "lazer": 40
  },
  "padroes_identificados": [
    "Categoria de maior gasto: Alimentacao",
    "Comprometimento de renda com gastos essenciais: 16%"
  ],
  "recomendacoes": [
    "Monitorar gastos recorrentes de lazer",
    "Aumentar reserva financeira mensal"
  ]
}
```

**Exemplo 2: Perfil "Saudavel"**

Entrada:
```json
{
  "renda_mensal": 8000,
  "nivel_endividamento": 5,
  "frequencia_poupanca": "Alta",
  "transacoes": [
    { "descricao": "Aluguel", "valor": 1500 },
    { "descricao": "Farmacia", "valor": 120 },
    { "descricao": "Curso online", "valor": 200 }
  ]
}
```

Saida:
```json
{
  "perfil_financeiro": "Saudavel",
  "probabilidade": 0.91,
  "resumo_gastos": {
    "moradia": 1500,
    "saude": 120,
    "educacao": 200
  },
  "padroes_identificados": [
    "Categoria de maior gasto: Moradia",
    "Comprometimento de renda com gastos essenciais: 22%",
    "Gastos nao essenciais comprometem 0% da renda"
  ],
  "recomendacoes": [
    "Manter o padrao atual de poupanca",
    "Considerar reserva de emergencia adicional"
  ]
}
```

**Exemplo 3: Perfil "Em risco"**

Entrada:
```json
{
  "renda_mensal": 3000,
  "nivel_endividamento": 68,
  "frequencia_poupanca": "Nenhuma",
  "transacoes": [
    { "descricao": "Cartao de credito", "valor": 900 },
    { "descricao": "Uber", "valor": 250 },
    { "descricao": "Delivery", "valor": 300 }
  ]
}
```

Saída:
```json
{
  "perfil_financeiro": "Em risco",
  "probabilidade": 0.88,
  "resumo_gastos": {
    "servicos": 900,
    "transporte": 250,
    "alimentacao": 300
  },
  "padroes_identificados": [
    "Concentracao em Servicos (62% do total gasto)",
    "Comprometimento de renda com gastos essenciais: 0%",
    "Categoria de maior gasto: Servicos"
  ],
  "recomendacoes": [
    "Reduzir gastos com aplicativos de transporte",
    "Priorizar quitacao de dividas com cartao de credito",
    "Estabelecer meta minima de poupanca mensal"
  ]
}
```

**Exemplo 4 (erro): Transação com valor inválido**

Entrada:
```json
{
  "renda_mensal": 4500,
  "nivel_endividamento": 25,
  "frequencia_poupanca": "Media",
  "transacoes": [
    { "descricao": "Supermercado", "valor": -420 }
  ]
}
```

Saída (422):
```json
{
  "erro": {
    "codigo": "VALOR_TRANSACAO_INVALIDO",
    "mensagem": "O campo 'valor' da transacao deve ser maior que zero.",
    "campo": "transacoes[0].valor",
    "timestamp": "2026-07-06T14:32:10Z"
  }
}
```

---

## 4. Endpoint 2: Classificação de Transações

### 4.1 Identificação

| Item | Detalhe |
|---|---|
| Método | POST |
| Caminho | /classificacao-transacoes |
| Descrição | Recebe uma lista de transações e retorna a categoria financeira de cada uma, sem realizar análise de perfil. |

### 4.2 Contrato de Entrada

```json
{
  "transacoes": [
    { "descricao": "Supermercado", "valor": 420 },
    { "descricao": "Combustivel", "valor": 300 }
  ]
}
```

| Campo | Tipo | Obrigatório | Restrições |
|---|---|---|---|
| transacoes | lista de objetos | Sim | Deve conter no mínimo 1 transação |
| transacoes[].descricao | string | Sim | Não pode ser vazia; máximo de 120 caracteres |
| transacoes[].valor | número decimal | Sim | Deve ser maior que 0 |

### 4.3 Contrato de Saída (sucesso, 200)

```json
{
  "transacoes_classificadas": [
    {
      "descricao": "Supermercado",
      "valor": 420,
      "categoria": "Alimentacao"
    },
    {
      "descricao": "Combustivel",
      "valor": 300,
      "categoria": "Transporte"
    }
  ]
}
```

| Campo | Tipo | Descrição |
|---|---|---|
| transacoes_classificadas | lista de objetos | Uma entrada por transação recebida, na mesma ordem de envio |
| transacoes_classificadas[].descricao | string | Repete a descrição original recebida |
| transacoes_classificadas[].valor | número decimal | Repete o valor original recebido |
| transacoes_classificadas[].categoria | string (enum) | Categoria atribuída: "Alimentacao", "Transporte", "Saude", "Moradia", "Educacao", "Lazer", "Servicos", "Outras" |

### 4.4 Exemplos Reais de Utilização

**Exemplo 1: Múltiplas categorias**

Entrada:
```json
{
  "transacoes": [
    { "descricao": "Farmacia Popular", "valor": 85 },
    { "descricao": "Cinema", "valor": 60 }
  ]
}
```

Saída:
```json
{
  "transacoes_classificadas": [
    { "descricao": "Farmacia Popular", "valor": 85, "categoria": "Saude" },
    { "descricao": "Cinema", "valor": 60, "categoria": "Lazer" }
  ]
}
```

**Exemplo 2: Transação não reconhecida (categoria "Outras")**

Entrada:
```json
{
  "transacoes": [
    { "descricao": "Pagamento diverso XY123", "valor": 50 }
  ]
}
```

Saída:
```json
{
  "transacoes_classificadas": [
    { "descricao": "Pagamento diverso XY123", "valor": 50, "categoria": "Outras" }
  ]
}
```

**Exemplo 3 (erro): Lista vazia**

Entrada:
```json
{
  "transacoes": []
}
```

Saída (422):
```json
{
  "erro": {
    "codigo": "LISTA_TRANSACOES_VAZIA",
    "mensagem": "E necessario informar ao menos uma transacao para classificacao.",
    "campo": "transacoes",
    "timestamp": "2026-07-06T14:32:10Z"
  }
}
```

---

## 5. Catálogo de Códigos de Erro

| Código | Status HTTP | Descrição |
|---|---|---|
| JSON_MALFORMADO | 400 | O corpo da requisição não é um JSON válido |
| CAMPO_OBRIGATORIO_AUSENTE | 422 | Um campo obrigatório não foi informado |
| CAMPO_INVALIDO | 422 | Um campo foi informado com tipo ou formato incorreto |
| VALOR_TRANSACAO_INVALIDO | 422 | O valor de uma transação é menor ou igual a zero |
| LISTA_TRANSACOES_VAZIA | 422 | A lista de transações foi enviada sem nenhum item |
| ENUM_INVALIDO | 422 | Valor informado para um campo do tipo enumerado não pertence ao domínio aceito |
| FALHA_INTERNA_PROCESSAMENTO | 500 | Erro inesperado durante a execução da análise ou classificação |
| SERVICO_ML_INDISPONIVEL | 504 | O ml-service nao respondeu ou retornou erro antes de completar a classificacao |

---

# Contrato Interno: ML Service

Este contrato define a comunicação entre a API (Spring Boot) e o ML Service (FastAPI). A API chama o ML Service internamente para obter a classificação das transações e do perfil financeiro. O resultado é então enriquecido pela API com recomendações e armazenamento.

---

## 7. Endpoint Interno: Classificação ML

### 7.1 Identificação

| Item | Detalhe |
|---|---|
| Método | POST |
| Caminho | /ml/analise |
| Consumidor | API (Spring Boot) |
| Descrição | Recebe os dados financeiros completos e retorna a classificação das transações, o perfil financeiro e a probabilidade associada. |

### 7.2 Contrato de Entrada

```json
{
  "renda_mensal": 4500,
  "nivel_endividamento": 25,
  "frequencia_poupanca": "Media",
  "transacoes": [
    { "descricao": "Supermercado", "valor": 420 },
    { "descricao": "Combustivel", "valor": 300 }
  ]
}
```

| Campo | Tipo | Obrigatório | Restrições |
|---|---|---|---|
| renda_mensal | número decimal | Sim | Deve ser maior que 0 |
| nivel_endividamento | número decimal | Sim | Deve estar entre 0 e 100 |
| frequencia_poupanca | string (enum) | Sim | "Nenhuma", "Baixa", "Media", "Alta" |
| transacoes | lista de objetos | Sim | Mínimo 1 |
| transacoes[].descricao | string | Sim | 1 a 120 caracteres |
| transacoes[].valor | número decimal | Sim | Maior que 0 |

### 7.3 Contrato de Saída (sucesso, 200)

```json
{
  "perfil_financeiro": "Em observacao",
  "probabilidade": 0.82,
  "transacoes_classificadas": [
    { "descricao": "Supermercado", "valor": 420, "categoria": "Alimentacao" },
    { "descricao": "Combustivel", "valor": 300, "categoria": "Transporte" }
  ]
}
```

| Campo | Tipo | Descrição |
|---|---|---|
| perfil_financeiro | string (enum) | "Saudavel", "Em observacao", "Em risco" |
| probabilidade | número decimal (0 a 1) | Confiança da classificação |
| transacoes_classificadas | lista de objetos | Transações com categoria atribuída |
| transacoes_classificadas[].descricao | string | Descrição original |
| transacoes_classificadas[].valor | número decimal | Valor original |
| transacoes_classificadas[].categoria | string | Categoria atribuída (ver domínio no Dicionário) |

### 7.4 Contrato de Erro (422)

```json
{
  "erro": {
    "codigo": "VALOR_TRANSACAO_INVALIDO",
    "mensagem": "O campo 'valor' da transacao deve ser maior que zero.",
    "campo": "transacoes[0].valor",
    "timestamp": "2026-07-06T14:32:10Z"
  }
}
```

### 7.5 Endpoint de Health Check

| Item | Detalhe |
|---|---|
| Método | GET |
| Caminho | /ml/health |
| Consumidor | API (Spring Boot), docker healthcheck |
| Resposta (200) | `{ "status": "ok" }` |
| Resposta (503) | `{ "status": "loading" }` (modelos ainda carregando) |

### 7.6 Observações

- O ML Service é stateless: cada requisição carrega os modelos do disco
- Os modelos (.pkl) são carregados na inicialização do serviço
- O endpoint é chamado exclusivamente pela API (Spring Boot), nunca diretamente pelo frontend
- A URL do ML Service é configurada via variável de ambiente `ML_SERVICE_URL`
- A API deve tratar timeout de conexão com o ml-service e retornar 504 com `SERVICO_ML_INDISPONIVEL`

---

## 8. Endpoint: Histórico de Análises

### 8.1 Identificação

| Item | Detalhe |
|---|---|
| Método | GET |
| Caminho | /historico-analises |
| Descrição | Retorna a lista das análises financeiras realizadas anteriormente, ordenadas da mais recente para a mais antiga. |

### 8.2 Contrato de Saída (sucesso, 200)

```json
{
  "analises": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "criado_em": "2026-07-06T14:32:10Z",
      "perfil_financeiro": "Em observacao",
      "resumo_gastos": {
        "alimentacao": 420,
        "transporte": 300,
        "lazer": 40
      }
    }
  ]
}
```

| Campo | Tipo | Descrição |
|---|---|---|
| analises | lista de objetos | Lista de análises anteriores, ordenadas da mais recente para a mais antiga |
| analises[].id | string (UUID v4) | Identificador único da análise |
| analises[].criado_em | string (ISO 8601) | Momento em que a análise foi realizada |
| analises[].perfil_financeiro | string (enum) | Perfil classificado na análise: "Saudavel", "Em observacao", "Em risco" |
| analises[].resumo_gastos | objeto (chave dinâmica) | Mapa de categoria de despesa para valor total agregado |

### 8.3 Exemplos Reais de Utilização

**Exemplo 1: Com análises anteriores**

Requisição:
```
GET /historico-analises
```

Resposta (200):
```json
{
  "analises": [
    {
      "id": "c7d8e9f0-a1b2-3456-cdef-0987654321ab",
      "criado_em": "2026-07-06T14:30:00Z",
      "perfil_financeiro": "Em observacao",
      "resumo_gastos": {
        "alimentacao": 420,
        "transporte": 300,
        "lazer": 40
      }
    },
    {
      "id": "b2c3d4e5-f6a7-8901-bcde-1234567890ab",
      "criado_em": "2026-07-05T10:15:00Z",
      "perfil_financeiro": "Em risco",
      "resumo_gastos": {
        "servicos": 900,
        "transporte": 250,
        "alimentacao": 300
      }
    }
  ]
}
```

**Exemplo 2: Sem análises anteriores**

Requisição:
```
GET /historico-analises
```

Resposta (200):
```json
{
  "analises": []
}
```

### 8.4 Observações

- O limite máximo de análises retornadas é definido por configuração padrão (ex: 20)
- A listagem considera apenas as análises armazenadas localmente (H2 em dev, AJD em prod)
- Este endpoint depende da implementação de RF014 (registro automático de análises no armazenamento)

---

## 9. Observações de Rastreabilidade

Cada requisição processada deve gerar um identificador único de execução, conforme estabelecido em RN009 do documento de SRS. Esse identificador não faz parte obrigatória do contrato de resposta ao cliente, mas deve estar disponível internamente para fins de auditoria e depuração.

**Definição de geração:** um UUID v4 é gerado no controller da API (Spring Boot) no momento em que a requisição é recebida, antes de qualquer validação ou processamento. Esse UUID é armazenado juntamente com a análise no campo `id` do documento da coleção SODA (ARQUITETURA.md seção 4.3) e pode ser exposto futuramente como cabeçalho de resposta `X-Request-Id`, caso definido em versão futura do sistema.

---

