# 🤖 Etapa 3 – Construção do Modelo de IA

## 1️⃣ Seleção do Modelo

Para o desenvolvimento do modelo de previsão da produtividade agrícola da cana-de-açúcar, avaliamos algoritmos de aprendizado de máquina adequados para dados tabulares multivariados e que pudessem se beneficiar do uso de **GPU com CUDA**.

### 🎯 Requisitos técnicos considerados:

- Dados de entrada com múltiplas variáveis numéricas mensais (NDVI, chuva, temperatura, mês).
- Quantidade moderada de dados (não massivos, mas com sazonalidade importante).
- Modelo com **baixo tempo de treinamento** e **capacidade de capturar relações não-lineares** entre clima, vegetação e produtividade.
- Possibilidade de execução acelerada por **GPU NVIDIA com CUDA**, disponível em nossa infraestrutura com WSL2.

---

## 🔍 Modelo escolhido: **XGBoost com aceleração por GPU**

Selecionamos o algoritmo **XGBoost Regressor** com o parâmetro `tree_method='gpu_hist'`, que permite:

- Treinamento extremamente rápido utilizando núcleos CUDA;
- Performance comparável ou superior ao Random Forest em muitos cenários com poucos dados;
- Capacidade de realizar **interpretação dos resultados** por meio da importância das variáveis.

### ⚙️ Configuração inicial do modelo:

```python
from xgboost import XGBRegressor

modelo = XGBRegressor(
    tree_method='gpu_hist',    # Ativa o uso da GPU (via CUDA)
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    random_state=42
)


## 2️⃣ Treinamento e Avaliação do Modelo

Com o modelo XGBoost configurado para utilizar **aceleração via GPU (CUDA)**, realizamos o treinamento utilizando os dados históricos de NDVI, clima e produtividade.

---

### 🔀 Divisão dos dados

A base consolidada foi dividida em dois subconjuntos:

- **80% dos dados** para treinamento (`X_train`, `y_train`)
- **20% dos dados** para teste e validação do modelo (`X_test`, `y_test`)

```python
from sklearn.model_selection import train_test_split

X = df[['NDVI', 'Chuva (mm)', 'Temp. Máx. (C)', 'Temp. Mín. (C)', 'Mes']]
y = df['Produtividade (ton/ha)']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


## 📊 Comparativo entre Modelos: XGBoost vs SVR

Testamos dois algoritmos para prever a produtividade da cana-de-açúcar:

| Modelo     | MAE (ton/ha) | MSE | R² (Coef. Determinação) |
|------------|--------------|-----|--------------------------|
| XGBoost GPU| 1.22         | 2.08| **-0.53**                |
| SVR (RBF)  | **1.08**     | **1.37** | **-0.01**           |

✅ **O modelo SVR apresentou melhor desempenho** geral, com menor erro absoluto e quadrático.  
📉 O R² ainda está abaixo de zero, indicando que o modelo não generaliza bem, mas é **muito superior ao XGBoost neste cenário de poucos dados com baixa variação**.

---

### 🎯 Justificativa da Escolha do SVR

O **SVR com kernel RBF** foi escolhido por sua capacidade de lidar com:

- Pequenas bases de dados;
- Relações não lineares entre as variáveis climáticas e a produtividade;
- Robustez contra overfitting em datasets com pouca variabilidade.

Além disso, o uso de `StandardScaler` para normalização das variáveis foi essencial para que o SVR tivesse bom desempenho.

---

### 📈 Visualizações

- **Gráfico Real vs Previsto (SVR)**: mostra boa tendência de ajuste mesmo com dados limitados.
- Arquivo salvo: `../tests/images/svr_real_vs_prevista.png`


## 🧠 Etapa 3 – Construção e Avaliação dos Modelos

Durante a Sprint 2, testamos diferentes algoritmos de regressão para prever a produtividade agrícola da cana-de-açúcar, utilizando dados climáticos e NDVI mensal da região de Uberaba/MG.

### ⚙️ Modelos Avaliados

| Modelo                         | MAE (ton/ha) | MSE  | R²    | Observações |
|-------------------------------|--------------|------|--------|-------------|
| **SVR (RBF)**                 | **1.08**     | **1.37** | **-0.01** | Melhor desempenho geral |
| SVR + validação cruzada + features derivadas | 1.07 | 1.39 | -0.02 | Piorou; validação cruzada instável |
| SVR otimizado (GridSearch)    | 1.39         | 2.49 | -0.83 | Desempenho inferior |
| **Regressão Linear**          | 1.17         | 1.65 | -0.21 | Usado como baseline |

---

### ✅ Justificativa da Escolha Final

Após testar várias estratégias — incluindo tuning de hiperparâmetros, validação cruzada, criação de variáveis derivadas e análise de resíduos — o **modelo SVR com kernel RBF e configuração padrão** apresentou o melhor equilíbrio entre simplicidade e desempenho.

- O SVR capturou **relações não-lineares** entre as variáveis.
- Tentativas de otimização automática (com GridSearchCV) e adição de novas features **não trouxeram ganho real** e inclusive pioraram a performance.
- A regressão linear foi útil como benchmark, mas teve menor capacidade de generalização.

---

### 📁 Gráficos Gerados

- `svr_real_vs_prevista.png` – Desempenho do SVR
- `regressao_linear_real_vs_prevista.png` – Desempenho do baseline
- `svr_residuos.png` (versão intermediária) – Análise de resíduos
- `svr_metricas.csv` – Registro das métricas principais

---

### 📝 Conclusão

> O modelo **SVR com RBF** será mantido como modelo oficial do projeto, com base em evidências estatísticas, robustez e capacidade de aprendizado sobre os dados disponíveis.



## 🧠 Etapa 3 – Construção do Modelo de IA

### 🎯 Objetivo
Desenvolver um modelo preditivo capaz de estimar a produtividade agrícola com base nos dados climáticos e no índice NDVI.

---

### ✅ O que foi feito:

1. **Seleção do Modelo**
   - Foram testados diversos algoritmos:
     - SVR (RBF) ✅ (modelo escolhido)
     - XGBoost com GPU
     - Regressão Linear (baseline)
   - O SVR se mostrou mais robusto e adaptado ao tamanho e comportamento do dataset.

2. **Treinamento e Validação**
   - Utilizamos `train_test_split` para treinar e testar os modelos.
   - Métricas de avaliação: `MAE`, `MSE`, `R²`.
   - Visualizações com gráficos de previsões e resíduos.

3. **Ajuste de Hiperparâmetros**
   - Foram testadas abordagens com `GridSearchCV`, validação cruzada (5-fold) e adição de novas variáveis.
   - Essas abordagens não trouxeram ganhos reais e foram descartadas após análise.
   - O modelo SVR com configuração padrão foi mantido como o melhor candidato.

---

### 🧪 Conclusão da Etapa 3

O modelo **SVR com kernel RBF** foi mantido como oficial por apresentar o melhor desempenho, simplicidade e estabilidade frente aos demais avaliados. As tentativas de ajuste mais agressivas (como GridSearch) mostraram-se ineficazes para o volume de dados disponível.
