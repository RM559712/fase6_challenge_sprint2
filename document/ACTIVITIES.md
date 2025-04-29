# 📚 Etapa 1 – Pré-processamento dos Dados

## 1.1 Organização dos Datasets Coletados na Sprint 1

| Item              | Status | Observação                                          |
|-------------------|:------:|-----------------------------------------------------|
| NDVI              | ✅      | Coletado via SATVeg, estruturado por mês/ano         |
| Dados Climáticos  | ✅      | Coletados via INMET: chuva, temperatura máxima/mínima |
| Produtividade     | ✅      | Coletado via IBGE, interpolado mensalmente           |

> 📂 Resultado: Dados organizados em `data/dataset_unificado.csv`.

---

## 1.2 Tratamento dos Dados

| Item                                 | Status | Observação                                |
|--------------------------------------|:------:|-------------------------------------------|
| Conversão de datas para `Ano-Mês`    | ✅      | Realizado                                 |
| Normalização de formatos numéricos   | ✅      | Ajustado (ponto decimal, etc.)             |
| Verificação de valores nulos         | ✅      | Tratado                                   |
| Padronização de nomes de colunas     | ✅      | Feito                                     |

> 📂 Resultado: Dados prontos para alimentar o modelo de IA, sem inconsistências.

---

## 1.3 Identificação de Padrões e Sazonalidades no NDVI

| Item                                             | Status | Observação                                         |
|--------------------------------------------------|:------:|----------------------------------------------------|
| Análise de tendências no NDVI                   | ✅      | Gráfico NDVI ao longo do tempo plotado              |
| Correlação entre NDVI e Produtividade Agrícola   | ✅      | Análise exploratória confirmando relação positiva  |
| Observação de sazonalidade                       | ✅      | Redução do NDVI nos períodos secos (junho-agosto)   |

> 📊 Resultado: Confirmada a presença de padrões sazonais na cultura da cana-de-açúcar.

---

# 📋 Resumo da Etapa 1
| Sub-etapa                               | Status       |
|-----------------------------------------|--------------|
| Organização dos dados                   | ✅ Completo   |
| Tratamento e estruturação               | ✅ Completo   |
| Identificação de padrões e sazonalidades| ✅ Completo   |


# 🧠 Etapa 2 – Extração de Informações Relevantes

## 2.1 Definição das Variáveis-Chave para o Modelo

A partir da análise exploratória dos dados, as seguintes variáveis foram selecionadas para compor o modelo de previsão de produtividade agrícola:

| Variável              | Tipo       | Justificativa                                                                 |
|----------------------|------------|-------------------------------------------------------------------------------|
| NDVI                 | Numérica   | Indica o vigor da vegetação e o estado fisiológico da cana-de-açúcar         |
| Chuva (mm)           | Numérica   | A disponibilidade de água influencia diretamente no crescimento da cultura   |
| Temperatura Máxima (°C) | Numérica   | Altas temperaturas podem gerar estresse térmico e reduzir a produtividade    |
| Temperatura Mínima (°C) | Numérica   | Temperaturas muito baixas também afetam o desenvolvimento vegetativo         |
| Mês                  | Categórica | Captura padrões sazonais críticos (ex: seca em junho-agosto)                 |

> 🔎 As variáveis foram validadas por meio de **correlação estatística** e **observação visual de sazonalidades** no notebook de análise exploratória.

---

## 2.2 Análise da Relação NDVI x Produtividade Agrícola

Com base nos dados entre **2019 e 2023**, foi possível observar:

- **Correlação positiva entre NDVI e produtividade**  
  Quanto maior o NDVI em determinado período, maior tende a ser a produtividade da cultura.

- **Ciclos de crescimento bem definidos**  
  Os picos de NDVI ocorrem geralmente entre **dezembro e abril**, refletindo as fases de maior vigor da cultura.

- **Períodos críticos de baixa no NDVI**  
  Identificados nos meses **junho a agosto**, indicando sazonalidade seca que reduz a atividade fotossintética.

---

## 2.3 Segmentação de Áreas nas Imagens de Satélite

Embora o projeto não exija interface visual, foi feita a sugestão técnica para:

- **Aplicar segmentação por talhão** nas imagens extraídas do SATVeg, identificando áreas com NDVI abaixo de determinado limiar.
- Essa técnica pode ser usada para **realce de áreas críticas**, onde o modelo pode indicar alerta de baixa produtividade.
- A segmentação pode ser aplicada com auxílio de mascaramento por polígonos (ex: shapefiles) ou análise por NDVI médio por pixel.

> 🛰️ A técnica pode ser estendida em projetos futuros com apoio de bibliotecas como **Rasterio**, **OpenCV** ou **Google Earth Engine** para manipulação geoespacial.

---

# 📋 Resumo da Etapa 2

| Sub-etapa                                       | Status       |
|-------------------------------------------------|--------------|
| Seleção e validação das variáveis do modelo     | ✅ Completo   |
| Análise NDVI x Produtividade e sazonalidades    | ✅ Completo   |
| Segmentação sugerida para áreas críticas        | ✅ Documentada|


# 🤖 Etapa 3 – Construção do Modelo de Inteligência Artificial

## 3.1 Escolha do Modelo

Foi selecionado o algoritmo **Random Forest Regressor**, por apresentar as seguintes vantagens:

| Critério                        | Justificativa                                                                 |
|---------------------------------|-------------------------------------------------------------------------------|
| Robustez a dados com ruído      | Random Forest é menos sensível a flutuações isoladas nos dados               |
| Capacidade de interpretar variáveis | Permite observar a importância de cada variável na predição                 |
| Flexibilidade                   | Lida bem com dados não lineares e combina múltiplas árvores de decisão       |
| Baixo overfitting (quando bem configurado) | Ideal para evitar previsões irreais em dados complexos               |

> 💡 O modelo também pode ser substituído futuramente por XGBoost ou redes neurais (LSTM), caso a base seja expandida.

---

## 3.2 Preparação para o Treinamento

- Dados de entrada: `NDVI`, `Chuva`, `Temperatura Máx`, `Temperatura Mín`
- Variável de saída: `Produtividade (ton/ha)`
- Divisão dos dados:
  - **Treino:** 2019 a 2022 (48 meses)
  - **Teste:** 2023 (12 meses)

> 📁 Arquivo de dados: `data/dataset_unificado.csv`  
> 📄 Implementado no notebook: `src/modelo_ia.ipynb`

---

## 3.3 Treinamento e Validação do Modelo

- O modelo foi treinado com `RandomForestRegressor(n_estimators=100, random_state=42)`
- Após o treinamento, os valores de produtividade foram previstos para os 12 meses de 2023
- As previsões foram comparadas com os valores reais interpolados

---

## 3.4 Avaliação de Desempenho

| Métrica             | Resultado aproximado |
|---------------------|----------------------|
| R² (Coef. de determinação) | 0.87                 |
| RMSE (Raiz do erro quadrático médio) | 1.12 ton/ha        |
| MAE (Erro absoluto médio) | 0.91 ton/ha         |

> 🧪 Resultados indicam boa capacidade do modelo em capturar a variação produtiva da cultura ao longo do ano.

---

## 3.5 Visualizações Geradas

- 📈 Gráfico comparando **Produtividade Real x Prevista**  
  ![Gráfico Real vs Previsto](../tests/images/produtividade_real_vs_prevista.png)

- 📊 Gráfico de **Importância das Variáveis no Modelo**  
  ![Importância das Variáveis](../tests/images/importancia_variaveis.png)

---

# 📋 Resumo da Etapa 3

| Sub-etapa                              | Status       |
|----------------------------------------|--------------|
| Definição e justificativa do modelo    | ✅ Completo   |
| Divisão e preparação dos dados         | ✅ Completo   |
| Treinamento e validação do modelo      | ✅ Completo   |
| Avaliação com métricas e gráficos      | ✅ Completo   |

# 🔍 Etapa 4 – Avaliação e Ajustes do Modelo

## 4.1 Testes com Diferentes Períodos de Dados

O modelo foi treinado com dados de **2019 a 2022** e testado com o ano de **2023**, simulando um cenário real de previsão futura. Foram considerados os seguintes aspectos:

- **Variações sazonais mantidas** no período de teste
- **Manutenção da estrutura do solo e cultura** (sem mudanças drásticas)
- Teste com **dados interpolados de produtividade**, já que não há dados mensais reais

> 📊 A base mostrou-se coerente para uso preditivo de curto prazo (até 12 meses).

---

## 4.2 Análise dos Resultados

O modelo apresentou um desempenho satisfatório com as seguintes métricas:

| Métrica        | Resultado (2023) |
|----------------|------------------|
| R²             | 0.87             |
| RMSE           | 1.12 ton/ha      |
| MAE            | 0.91 ton/ha      |

📌 Esses valores demonstram:
- Boa capacidade de generalização
- Baixo erro médio em relação ao valor absoluto da produtividade (~86–89 ton/ha)
- Indicação de que as variáveis climáticas e NDVI possuem impacto relevante e previsível

---

## 4.3 Ajustes Técnicos Considerados

| Ajuste                          | Ação |
|----------------------------------|------|
| Número de árvores (estimators)  | Mantido em 100 para reduzir overfitting |
| Aleatoriedade (random_state)    | Fixada em 42 para reprodutibilidade     |
| Feature importance              | Avaliada com gráfico para interpretar modelo |
| Próximos passos                 | Testar modelos como **XGBoost** ou **LSTM** em versões futuras do projeto |

---

## 4.4 Visualizações Geradas para Avaliação

- 📈 **Gráfico 1 – Produtividade Real vs Prevista (2023)**  
  ![Gráfico Real vs Previsto](../tests/images/produtividade_real_vs_prevista.png)

- 📊 **Gráfico 2 – Importância das Variáveis**  
  ![Importância das Variáveis](../tests/images/importancia_variaveis.png)

---

## 📋 Resumo da Etapa 4

| Sub-etapa                                 | Status       |
|--------------------------------------------|--------------|
| Validação com dados de teste (2023)        | ✅ Completo   |
| Cálculo de métricas                        | ✅ Completo   |
| Análise de desempenho                      | ✅ Completo   |
| Ajustes e recomendações futuras            | ✅ Completo   |
| Visualizações para relatório e README      | ✅ Geradas    |





