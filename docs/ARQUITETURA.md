# Documentação de Arquitetura

## Sistema de Análise de Comportamento Financeiro e Recomendação Personalizada

---

## 1. Visão Geral da Arquitetura

O sistema é composto por três serviços independentes que rodam em containers Docker, orquestrados pelo docker compose:

```
┌─────────────────────────────────────────────────────────────────┐
│                        docker compose                            │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │   Frontend   │    │     API      │    │   ML Service     │   │
│  │   (React)    │───▶│ Spring Boot  │───▶│   (FastAPI)      │   │
│  │   :3000      │    │   :8080      │    │   :8000          │   │
│  └──────────────┘    └──────┬───────┘    └──────────────────┘   │
│                             │                                    │
│                             ▼                                    │
│                      ┌──────────────┐                           │
│                      │  Armazenamento                           │
│                      │  Local ou AJD │                           │
│                      └──────────────┘                           │
└─────────────────────────────────────────────────────────────────┘
```

### 1.1 Fluxo de uma Requisição (Análise Financeira)

```mermaid
sequenceDiagram
    participant U as Usuario
    participant F as Frontend (React)
    participant B as API (Spring Boot)
    participant M as ML Service (FastAPI)
    participant S as Storage

    U->>F: Preenche formulario
    F->>F: Valida campos no cliente
    F->>B: POST /api/analise-financeira
    B->>B: Valida entrada (Bean Validation)
    B->>M: POST /ml/analise
    M->>M: Carrega modelos .pkl
    M->>M: Classifica transacoes + perfil
    M-->>B: JSON com classificacao + probabilidade
    B->>B: Identifica padroes de consumo
    B->>B: Gera recomendacoes
    B->>S: Salva resultado da analise
    B-->>F: JSON com perfil + gastos + padroes + recomendacoes
    F->>F: Renderiza resultado
    F-->>U: Exibe tela com dados financeiros
```

---

## 2. Decisões Técnicas

### 2.1 Por que FastAPI e não Flask para o ML Service?

| Critério | FastAPI | Flask |
|---|---|---|
| Performance | Assíncrono nativo (uvloop) | Síncrono |
| Validação | Pydantic integrado | Manual (marshmallow) |
| Documentação | OpenAPI automática | Necessário flasgger |
| Curva de aprendizado | Baixa (similar a Flask) | Baixa |
| Suporte a tipos | Type hints nativos | Sem type hints |

### 2.2 Por que React + Vite e não Next.js ou CRA?

- **Vite**: mais rápido que CRA, mais simples que Next.js (sem SSR)
- **React puro**: time de frontend já conhece
- **Nginx**: servindo build estático, deploy universal
- Não há necessidade de SSR ou rotas no servidor para o MVP

### 2.3 Por que docker compose?

- Ambiente idêntico em todas as máquinas
- Zero instalação de dependências (Java, Python, Node) nos notebooks da equipe
- Facilita CI/CD futuro
- Cada serviço pode ser desenvolvido e testado isoladamente

### 2.4 Por que WireMock e não o ml-service real nos testes?

- Testes mais rápidos (milissegundos vs. segundos)
- Cenários de erro controlados (timeout, 500, resposta malformada)
- Sem dependência do container Python nos testes do backend
- O contrato real é verificado separadamente (teste de contrato opcional)

### 2.5 Por que armazenamento em interface?

```java
public interface Armazenamento {
    void salvar(String id, String conteudoJson);
    Optional<String> carregar(String id);
    List<String> listarHistorico(int limite);
}
```

- `ArmazenamentoLocal` → usa H2 em arquivo, roda no container `api` sem dependência externa
- `ArmazenamentoAJD` → usa SODA para Java, conecta na Oracle Autonomous JSON Database via wallet
- Trocado via variável de ambiente `ARMAZENAMENTO_TIPO`
- Zero alteração no código de negócio ao migrar

### 2.6 Por que Autonomous JSON Database e não Object Storage?

O edital do hackathon sugere Object Storage como serviço OCI para "armazenamento de modelos ou dados". O projeto optou pelo Autonomous JSON Database (AJD) pelas seguintes razões:

| Critério | AJD (escolhido) | Object Storage |
|---|---|---|
| Estrutura | Documentos JSON nativos (SODA) | Blobs (arquivos) |
| Consulta | Consultas por campo do JSON sem baixar o documento inteiro | Download completo do blob para ler qualquer campo |
| Modelo de dados | Um documento por análise, estrutura definida (seção 4.3) | Um arquivo `.json` por análise |
| Complexidade de implementação | Driver SODA para Java, integração direta com Spring Boot | SDK do OCI, upload/download manual |
| Armazenamento de modelos `.pkl` | (não atende) | (não atende igualmente) |

**Os modelos treinados (.pkl) não são armazenados em serviço OCI nesta versão do MVP.** Eles ficam em volume Docker local (`ml-service/models/`) e são carregados na inicialização do ml-service, conforme RA004. O Object Storage não foi escolhido porque o AJD oferece maior alinhamento com a natureza JSON dos dados do projeto (cada análise é um documento JSON) e porque o armazenamento de `.pkl` em Object Storage exigiria um fluxo de download na inicialização que adicionaria complexidade sem benefício para o prazo do hackathon. Essa decisão está registrada no board de riscos para reavaliação em versões futuras.

---

## 3. Estrutura do Projeto

```
nidus/
├── backend/                          # Spring Boot (API REST)
│   ├── Dockerfile
│   ├── pom.xml
│   └── src/
│       ├── main/java/com/nidus/
│       │   ├── controller/           # Endpoints REST
│       │   ├── dto/                  # Request/Response DTOs
│       │   ├── service/              # Regras de negócio
│       │   ├── validation/           # Validadores
│       │   └── infrastructure/       # Armazenamento, config
│       └── test/
├── ml-service/                       # FastAPI (ML)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── predictor.py                  # Serviço de predição
│   ├── models/                       # Modelos .pkl
│   └── tests/
├── frontend/                         # React + Vite
│   ├── Dockerfile
│   ├── package.json
│   ├── nginx.conf                    # Proxy reverso (produção)
│   ├── src/
│   │   ├── pages/                    # Páginas
│   │   ├── components/               # Componentes reutilizáveis
│   │   └── services/                 # Chamadas à API
│   └── tests/
├── notebooks/                        # Notebooks de treinamento
│   ├── eda.ipynb
│   └── treinamento.ipynb
├── docker-compose.yml
└── README.md
```

---

## 4. Armazenamento

### 4.1 Local (modo dev, `ARMAZENAMENTO_TIPO=local`)

- Banco H2 em arquivo (`./data/nidus.db`), montado como volume Docker no serviço `api`
- Cada análise salva como documento JSON em uma tabela simulada pelo H2
- Nenhuma credencial externa necessária

### 4.2 Oracle Autonomous JSON Database (modo produção, `ARMAZENAMENTO_TIPO=autonomous_json`)

- Serviço OCI utilizado: Autonomous JSON Database (AJD)
- API de acesso: SODA para Java (driver `com.oracle.database.soda`)
- Estrutura de dados: coleção SODA `analises`, um documento JSON por análise
- Autenticação: wallet (arquivo de configuração de conexão), nunca versionado no repositório
- Ativado por: `ARMAZENAMENTO_TIPO=autonomous_json`
- Deve ser implementado e compilado no código desde o MVP, mesmo que usado apenas na apresentação

### 4.3 Estrutura do Documento na Coleção SODA

Cada análise salva como um documento JSON na coleção `analises`:

| Campo do documento | Descrição |
|---|---|---|
| id | Identificador único da análise (UUID v4) |
| criado_em | Timestamp ISO 8601 da análise |
| requisição | Corpo original enviado pelo cliente |
| resposta | Corpo completo retornado ao cliente |

---

### 4.4 Regra de derivação das chaves do resumo_gastos

As chaves do objeto `resumo_gastos` são derivadas do nome oficial da categoria (conforme seção 3 do DICIONARIO.md) aplicando:

1. Conversão para minúsculas
2. Remoção de acentos
3. Substituição de espaços por underline (caso existam)

Exemplo: `"Alimentacao"` → `"alimentacao"`, `"Em observacao"` → `"em_observacao"`.

---

## 5. Estratégia de Migração para OCI

| Componente | Local (MVP) | OCI (Produção) | Mudança |
|---|---|---|---|
| API | Container Docker | OCI Compute (mesma imagem) | Apenas deploy |
| ML Service | Container Docker | OCI Compute (mesma imagem) | Apenas deploy |
| Frontend | Container Docker | OCI Compute + Nginx | Apenas deploy |
| Armazenamento | H2 em arquivo (`./data/nidus.db`) | Oracle Autonomous JSON Database (AJD) via SODA | Trocar implementação via interface |

Nenhuma linha de código de negócio precisa ser alterada. A migração é puramente operacional.

### 5.1 Tratamento de timeout do ml-service

A API (Spring Boot) deve configurar timeout de conexão e leitura ao chamar o ml-service. Caso o ml-service não responda dentro do limite (ex: 5s), a API deve retornar HTTP 504 com o código de erro `SERVICO_ML_INDISPONIVEL`, conforme catálogo do CONTRATOS.md.

---

## 6. Segurança

### 6.1 MVP (sem autenticação)

- A API não exige autenticação
- Recomendado rodar apenas em rede local
- Documentado como pendente para produção

### 6.2 Produção (OCI)

- RNF-SEG-003: controle de acesso via API Key ou JWT
- RNF-SEG-001: HTTPS via load balancer da OCI
- RNF-SEG-002: criptografia em repouso nativa do Oracle Autonomous JSON Database
- A ser definido em versão futura

---

## 7. Variáveis de Ambiente

| Variável | Serviço | Descrição | Default (MVP) |
|---|---|---|---|
| `ML_SERVICE_URL` | api | URL do ml-service | `http://ml-service:8000` |
| `ARMAZENAMENTO_TIPO` | api | local ou autonomous_json | `local` |
| `VITE_API_URL` | frontend | URL da API | `http://localhost:8080` |

---

## 8. Diagrama de Containers (docker compose)

```yaml
services:
  ml-service:
    build: ./ml-service
    ports:
      - "8000:8000"
    volumes:
      - ./ml-service/models:/app/models
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/ml/health"]
      interval: 5s
      retries: 10
      start_period: 15s

  api:
    build: ./backend
    ports:
      - "8080:8080"
    volumes:
      - ./data/nidus.db:/app/data/nidus.db
    environment:
      - ML_SERVICE_URL=http://ml-service:8000
      - ARMAZENAMENTO_TIPO=local
    depends_on:
      ml-service:
        condition: service_healthy

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - api
    environment:
      - VITE_API_URL=http://localhost:8080
```
