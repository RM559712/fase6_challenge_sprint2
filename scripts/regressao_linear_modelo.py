# regressao_linear_treinamento.py
# Diretório recomendado: scripts/

"""
Script de benchmark utilizando regressão linear para previsão da produtividade da cana-de-açúcar.
Usa as mesmas variáveis do modelo SVR para comparar desempenho de forma simples e interpretável.
"""

# ============================================================
# 1. Importação das Bibliotecas
# ============================================================
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ============================================================
# 2. Carregamento e Validação do Dataset
# ============================================================
data_path = '../data/dataset_unificado.csv'
if not os.path.exists(data_path):
    raise FileNotFoundError("❌ Arquivo de dados não encontrado em ../data/")

df = pd.read_csv(data_path)

# ============================================================
# 3. Preparação das Variáveis (Features e Target)
# ============================================================
if 'Mes' not in df.columns:
    if 'Ano-Mes' in df.columns:
        df['Ano-Mes'] = pd.to_datetime(df['Ano-Mes'])
        df['Mes'] = df['Ano-Mes'].dt.month
    else:
        raise KeyError("Coluna 'Mes' não encontrada e 'Ano-Mes' também não disponível para extração.")

X = df[['NDVI', 'Chuva (mm)', 'Temp. Máx. (C)', 'Temp. Mín. (C)', 'Mes']]
y = df['Produtividade (ton/ha)']

# Normalização das features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# ============================================================
# 4. Treinamento com Regressão Linear
# ============================================================
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# ============================================================
# 5. Avaliação do Modelo
# ============================================================
y_pred = modelo.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n✅ Avaliação do Modelo Regressão Linear:")
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
plt.title('Produtividade Real vs Prevista - Regressão Linear')
plt.grid(True)
plt.tight_layout()
plt.savefig('../tests/images/regressao_linear_real_vs_prevista.png')
plt.show()
