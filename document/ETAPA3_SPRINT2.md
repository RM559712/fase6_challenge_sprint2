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


