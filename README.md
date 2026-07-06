# Nidus

![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-6DB33F?style=for-the-badge&logo=spring-boot&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Oracle Cloud](https://img.shields.io/badge/Oracle_Cloud-F80000?style=for-the-badge&logo=oracle&logoColor=white)

## Sobre

Sistema de análise de comportamento financeiro com classificação de transações, perfil financeiro e recomendações personalizadas.

```
docker compose up
├── Frontend (React)   :3000  ← Interface do usuário
├── API (Spring Boot)  :8080  ← Regras de negócio + validação
└── ML Service (FastAPI):8000 ← Classificação com modelo treinado
```

---

## Descrição do projeto 

Criar uma solução inteligente capaz de analisar o comportamento financeiro de um usuário a partir de suas transações e informações financeiras, gerando uma visão mais completa da sua saúde financeira. 
A solução deverá receber informações relacionadas a gastos e hábitos financeiros, como descrição de transações, valores, categorias de despesas, renda mensal, frequência de economia, nível de endividamento e outros indicadores relevantes. 
Com base nesses dados, o sistema deverá ser capaz de: 
* Classificar automaticamente despesas em categorias financeiras; 
* Identificar padrões de consumo; 
* Classificar o perfil financeiro do usuário; 
* Gerar indicadores que auxiliem na compreensão dos hábitos financeiros; 
* Apresentar recomendações simples para melhoria da saúde financeira. 
 
Esse tipo de solução pode ser utilizado por aplicativos financeiros, carteiras digitais, plataformas de educação financeira ou por usuários que desejam organizar melhor suas finanças pessoais. 
A solução deverá retornar os resultados em formato JSON e utilizar serviços OCI para armazenamento, processamento ou implantação da aplicação. 

---

## Necessidade do cliente 

Muitas pessoas possuem acesso aos dados das suas transações, mas têm dificuldade em transformar essas informações em conhecimento útil para tomada de decisão. 

A solução deve permitir: 
* Organizar automaticamente despesas e receitas; 
* Entender para onde o dinheiro está sendo direcionado; 
* Identificar hábitos financeiros positivos ou de risco; 
* Receber recomendações simples de melhoria; 
* Acompanhar a evolução do comportamento financeiro ao longo do tempo. 

Essa abordagem transforma dados financeiros brutos em informações claras e acionáveis. 

---

## Validação de mercado 

O mercado de fintechs, bancos digitais e plataformas de educação financeira continua em expansão. 

Os usuários buscam ferramentas que permitam: 
* Automatizar o controle financeiro; 
* Entender padrões de consumo; 
* Melhorar a capacidade de planejamento; 
* Reduzir riscos financeiros; 
* Receber recomendações personalizadas. 

Soluções que unem análise de gastos e avaliação de perfil financeiro geram mais valor do que classificadores isolados, pois oferecem uma visão mais ampla do comportamento do usuário. 

---

## Objetivo do Hackathon 

Desenvolver um MVP funcional capaz de: 
* Classificar despesas financeiras automaticamente; 
* Analisar o comportamento financeiro do usuário; 
* Gerar uma classificação de perfil financeiro; 
* Apresentar recomendações personalizadas; 
* Disponibilizar os resultados por meio de uma API REST; 
* Utilizar pelo menos um serviço OCI como parte da arquitetura da solução. 
 
---

## Resultados esperados 

### Ciência de Dados 
Notebook contendo: 
* Exploração e limpeza dos dados (EDA); 
* Tratamento de variáveis financeiras e textuais; 
* Engenharia de atributos; 
* Classificação de despesas; 
* Análise de perfil financeiro; 
* Treinamento e avaliação de modelos; 
* Métricas de desempenho adequadas; 
* Serialização dos modelos. 

### Back-End 
API REST contendo: 
* Endpoint para análise financeira; 
* Endpoint para classificação de transações; 
* Validação de entrada; 
* Tratamento de erros; 
* Documentação dos endpoints. 

### OCI 
Utilização de pelo menos um dos seguintes serviços: 
* Object Storage para armazenamento de modelos ou dados; 
* OCI Compute para hospedagem da aplicação; 
* OCI Functions para processamento específico; 
* Banco de dados opcional para persistência de informações. 
 
---

## Funcionalidades obrigatórias (MVP) 

### Classificação de transações 
O sistema deverá ser capaz de classificar automaticamente despesas em categorias como: 
* Alimentação; 
* Transporte; 
* Saúde; 
* Moradia; 
* Educação; 
* Lazer; 
* Serviços; 
* Outras categorias definidas pela equipe. 

### Análise de perfil financeiro 
O sistema deverá gerar uma avaliação do perfil financeiro do usuário com base nos dados analisados. 
Exemplos de categorias: 
* Saudável; 
* Em observação; 
* Em risco. 

As categorias podem ser adaptadas pela equipe conforme a estratégia adotada. 

### Recomendações financeiras 
A solução deverá gerar recomendações simples e objetivas com base nos resultados obtidos. 
Exemplos: 
* Reduzir gastos em determinada categoria; 
* Aumentar frequência de poupança; 
* Melhorar controle de despesas recorrentes. 
 
---

## Exemplo de uso 

### Endpoint 
`POST /analise-financeira` 

### Entrada 
```json
{ 
  "renda_mensal": 4500, 
  "nivel_endividamento": 25, 
  "frequencia_poupanca": "Media", 
  "transacoes": [ 
    { 
      "descricao": "Supermercado", 
      "valor": 420 
    }, 
    { 
      "descricao": "Combustivel", 
      "valor": 300 
    }, 
    { 
      "descricao": "Streaming", 
      "valor": 40 
    } 
  ] 
}
```
### Saída
```json
{ 
  "perfil_financeiro": "Em observacao", 
  "probabilidade": 0.82, 
  "resumo_gastos": { 
    "alimentacao": 420, 
    "transporte": 300, 
    "lazer": 40 
  }, 
  "recomendacoes": [ 
    "Monitorar gastos recorrentes de lazer", 
    "Aumentar reserva financeira mensal" 
  ] 
} 
```

---

## Requisitos mínimos

* Modelo treinado e carregado corretamente;
* Validação de entrada;
* Classificação funcional das transações;
* Análise de perfil financeiro;
* Geração de recomendações;
* API documentada;
* Integration com OCI;
* Mínimo de três exemplos reais de utilização.

---

## Recursos opcionais

* Dashboard financeiro;
* Visualização da evolução financeira;
* Processamento em lote via CSV;
* Histórico de análises;
* Alertas de gastos elevados;
* Containerização com Docker;
* Testes automatizados;
* Exportação de relatórios;
* Explicabilidade dos modelos.

---

## Diretrizes para Ciência de Dados

Cada equipe deverá construir seu próprio conjunto de dados financeiros. Os dados poderão ser:

* Obtidos em bases públicas;
* Gerados por simulações;
* Construídos manualmente pela equipe.

Recomenda-se utilizar:

* Python;
* Pandas;
* Scikit-Learn;
* Técnicas de classificação supervisionada;
* Engenharia de atributos;
* Modelos de classificação adequados ao problema.

A utilização de outras abordagens é permitida.

---

## Diretrizes para Back-End

A equipe deverá desenvolver uma API REST, preferencialmente utilizando Java com Spring Boot. A solução deverá:

* Receber informações financeiras;
* Processar classificações e análises;
* Retornar respostas estruturadas em JSON;
* Integrar o modelo de Ciência de Dados ao backend.

A arquitetura adotada deverá ser documentada pela equipe.

---

## OCI

A solucao deve utilizar pelo menos um servico OCI como parte obrigatoria do projeto. A implementacao segue o padrao de interface descrito na ARQUITETURA.md:

- **Dev** (`ARMAZENAMENTO_TIPO=local`): armazenamento em arquivos locais, sem dependencia de nuvem
- **Producao** (`ARMAZENAMENTO_TIPO=oci`): armazenamento no OCI Object Storage, ativado apenas quando necessario

---

## Estrutura do Projeto

```
nidus/
├── backend/                          # Spring Boot (API REST)
│   ├── Dockerfile
│   ├── pom.xml
│   └── src/
├── ml-service/                       # FastAPI (ML)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── predictor.py
│   └── models/                       # Modelos .pkl
├── frontend/                         # React + Vite
│   ├── Dockerfile
│   ├── package.json
│   ├── nginx.conf
│   └── src/
├── notebooks/                        # Notebooks de treinamento
│   ├── eda.ipynb
│   └── treinamento.ipynb
├── docker-compose.yml
├── docker-compose.test.yml
└── README.md
```

---

## Como Executar

### Pré-requisitos

- Docker e Docker Compose instalados
- Nenhuma outra dependência necessária (Java, Python, Node vêm nas imagens)

### Desenvolvimento

```bash
# Sobe todos os serviços
docker compose up

# Acessar:
# Frontend: http://localhost:3000
# API:      http://localhost:8080
# Swagger:  http://localhost:8080/swagger-ui.html
```

### Testes

```bash
# Executa todos os testes (backend + ml-service + frontend)
docker compose -f docker-compose.test.yml up --abort-on-container-exit

# Apenas backend
docker compose -f docker-compose.test.yml run api

# Apenas ml-service
docker compose -f docker-compose.test.yml run ml-service

# Apenas frontend
docker compose -f docker-compose.test.yml run frontend
```

---

## Modos de Execução

O sistema suporta dois modos de armazenamento controlados pela variável de ambiente `ARMAZENAMENTO_TIPO`:

| Modo | ARMAZENAMENTO_TIPO | Onde os dados são salvos | Requer OCI? |
|---|---|---|---|
| **Dev** | `local` (default) | Diretório `./data/analises/` montado como volume Docker | Nao |
| **Producao** | `oci` | OCI Object Storage (bucket) | Sim |

Durante o desenvolvimento, todos os membros da equipe rodam em modo `local`. Nenhuma credencial OCI é necessaria. Na apresentacao, ativa-se o modo `oci` para demonstrar a integracao com o bucket real.

---

## Stack Tecnologica

| Camada | Tecnologia | Finalidade |
|---|---|---|
| Frontend | React + Vite + TypeScript | Interface do usuário |
| API | Java 17 + Spring Boot 3 | Regras de negócio, validação, recomendações |
| ML Service | Python + FastAPI + Scikit-Learn | Classificação e perfil financeiro |
| Banco de dados | Nenhum (armazenamento em arquivos JSON) | MVP simula OCI Object Storage |
| Container | Docker + docker compose | Ambiente padronizado para toda a equipe |
| Testes (Java) | JUnit 5 + Mockito + WireMock | Testes unitários e de integração |
| Testes (Python) | pytest + TestClient | Testes do ml-service |
| Testes (React) | Vitest + React Testing Library + MSW | Testes do frontend |
| Cloud | OCI (Object Storage + Compute) | Produção / deploy |

---

## Documentação Complementar

- [Arquitetura](docs/ARQUITETURA.md) - Decisões técnicas, diagramas, estratégia OCI
- [Contratos de API](docs/CONTRATOS.md) - Endpoints, JSON, códigos de erro
- [Dicionário de Dados](docs/DICIONARIO.md) - Domínios, regras de normalização, glossário
- [Frontend](docs/FRONTEND.md) - Componentes, páginas, tipos, fluxo de dados
- [Requisitos (SRS)](docs/REQUISITOS.md) - Requisitos funcionais e não funcionais
- [Testes](docs/TESTES.md) - Estratégia, cenários, responsabilidades