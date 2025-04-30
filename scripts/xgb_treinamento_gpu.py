# xgb_treinamento_gpu.py
# Diretório recomendado: scripts/

"""
Script de treinamento do modelo XGBoost com CUDA para previsão de produtividade da cana-de-açúcar.
Utiliza os dados unificados do diretório ../data/ e salva os gráficos de resultado no diretório ../tests/images/
"""

# ============================================================
# 1. Importação das Bibliotecas
# ============================================================
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import XGBRegressor, DMatrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ============================================================
# 2. Carregamento e Validação do Dataset
# ============================================================
# Caminho para o dataset unificado com NDVI, clima e produtividade
data_path = '../data/dataset_unificado.csv'

# Verifica se o arquivo existe antes de carregar
if not os.path.exists(data_path):
    raise FileNotFoundError("❌ Arquivo de dados não encontrado em ../data/")

# Carrega os dados em um DataFrame pandas
df = pd.read_csv(data_path)

# ============================================================
# 3. Preparação das Variáveis (Features e Target)
# ============================================================
# Verifica se a coluna 'Mes' existe; caso contrário, extrai do campo 'Ano-Mes'
if 'Mes' not in df.columns:
    if 'Ano-Mes' in df.columns:
        df['Ano-Mes'] = pd.to_datetime(df['Ano-Mes'])
        df['Mes'] = df['Ano-Mes'].dt.month
    else:
        raise KeyError("Coluna 'Mes' não encontrada e 'Ano-Mes' também não disponível para extração.")

# Define as colunas de entrada (variáveis independentes)
X = df[['NDVI', 'Chuva (mm)', 'Temp. Máx. (C)', 'Temp. Mín. (C)', 'Mes']]

# Define a variável alvo (produtividade da cana)
y = df['Produtividade (ton/ha)']

# Divide os dados em treino (80%) e teste (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ============================================================
# 4. Treinamento com XGBoost usando GPU
# ============================================================
# Cria o modelo XGBoost com execução acelerada via CUDA
modelo = XGBRegressor(
    tree_method='hist',        # Usa histograma (necessário para usar device)
    device='cuda',             # Executa na GPU com CUDA
    n_estimators=200,          # Número de árvores na floresta
    max_depth=6,               # Profundidade máxima das árvores
    learning_rate=0.1,         # Taxa de aprendizado (shrinkage)
    random_state=42            # Reprodutibilidade
)

# Treina o modelo com os dados de treino
modelo.fit(X_train, y_train)

# ============================================================
# 5. Avaliação do Modelo
# ============================================================
# Realiza predições com o conjunto de teste, convertendo para o mesmo dispositivo do modelo
X_test_dmatrix = DMatrix(X_test, nthread=-1)
y_pred = modelo.predict(X_test)

# Calcula as métricas de avaliação
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Exibe os resultados
print("\n✅ Avaliação do Modelo:")
print(f"MAE (Erro Absoluto Médio): {mae:.2f} ton/ha")
print(f"MSE (Erro Quadrático Médio): {mse:.2f}")
print(f"R² (Coeficiente de Determinação): {r2:.2f}")

# ============================================================
# 6. Gráfico: Produtividade Real vs Prevista
# ============================================================
plt.figure(figsize=(10,6))
plt.scatter(y_test, y_pred, alpha=0.7, color='blue')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
plt.xlabel('Produtividade Real (ton/ha)')
plt.ylabel('Produtividade Prevista (ton/ha)')
plt.title('Produtividade Real vs Prevista - XGBoost GPU')
plt.grid(True)
plt.tight_layout()

# Salva a imagem no diretório de testes
plt.savefig('../tests/images/xgb_real_vs_prevista.png')
plt.show()

# ============================================================
# 7. Gráfico: Importância das Variáveis
# ============================================================
# Captura a importância relativa de cada variável usada no modelo
importancias = modelo.feature_importances_
variaveis = X.columns

plt.figure(figsize=(8,5))
sns.barplot(x=importancias, y=variaveis, palette='viridis')
plt.title('Importância das Variáveis - XGBoost com GPU')
plt.xlabel('Importância Relativa')
plt.tight_layout()

# Salva o gráfico
plt.savefig('../tests/images/xgb_importancia_variaveis.png')
plt.show()
