## 📊 Etapa 4 – Avaliação e Ajustes

### 🎯 Objetivo
Avaliar a consistência e confiabilidade do modelo SVR ao longo dos anos de produção, testando sua capacidade de generalização temporal.

---

### ✅ O que foi feito:

1. **Divisão por ano**
   - O dataset foi separado por ano com base na coluna `Ano-Mes`.
   - Para cada ano de teste (ex: 2023), o modelo foi treinado com os dados dos anos anteriores (ex: 2021 e 2022).

2. **Métricas calculadas**
   - Para cada ano testado, foram avaliados:
     - MAE (Erro Absoluto Médio)
     - MSE (Erro Quadrático Médio)
     - R² (Coeficiente de Determinação)

3. **Resultados e visualização**
   - Os resultados foram exportados para `avaliacao_temporal_metricas.csv`.
   - O gráfico `avaliacao_mae_por_ano.png` mostra o desempenho do modelo ao longo do tempo.

---

### 📁 Arquivos gerados:
- `scripts/avaliacao_temporal_modelo.py`
- `tests/avaliacao_temporal_metricas.csv`
- `tests/images/avaliacao_mae_por_ano.png`

---

### 🧠 Conclusão parcial:
> A análise por ano permite entender se o modelo está se adaptando bem a novas safras e mudanças climáticas. Essa abordagem também ajuda a validar se a estratégia de modelagem é confiável em diferentes contextos temporais.
