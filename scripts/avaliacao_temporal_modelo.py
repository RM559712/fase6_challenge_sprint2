# avaliacao_temporal_modelo.py
# Diretório recomendado: scripts/

"""
Etapa 4 – Avaliação e Ajustes
Este script testa a performance do modelo SVR em diferentes anos de teste,
com treino baseado em dados anteriores. Ele gera métricas por ano e gráficos de comparação.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# ===============================
# 1. Carregamento e Preparo dos Dados
# ===============================
data_path = '../data/dataset_unificado.csv'
if not os.path.exists(data_path):
    raise FileNotFoundError("Arquivo de dados não encontrado: ../data/dataset_unificado.csv")

df = pd.read_csv(data_path)
if 'Ano-Mes' in df.columns:
    df['Ano-Mes'] = pd.to_datetime(df['Ano-Mes'])
    df['Ano'] = df['Ano-Mes'].dt.year
    df['Mes'] = df['Ano-Mes'].dt.month
else:
    raise KeyError("Coluna 'Ano-Mes' necessária para extração do ano e mês.")

# ===============================
# 2. Avaliação Ano a Ano
# ===============================
resultados = []
anos_disponiveis = sorted(df['Ano'].unique())

for ano_teste in anos_disponiveis[1:]:
    df_treino = df[df['Ano'] < ano_teste]
    df_teste = df[df['Ano'] == ano_teste]

    if df_treino.empty or df_teste.empty:
        continue

    X_train = df_treino[['NDVI', 'Chuva (mm)', 'Temp. Máx. (C)', 'Temp. Mín. (C)', 'Mes']]
    y_train = df_treino['Produtividade (ton/ha)']
    X_test = df_teste[['NDVI', 'Chuva (mm)', 'Temp. Máx. (C)', 'Temp. Mín. (C)', 'Mes']]
    y_test = df_teste['Produtividade (ton/ha)']

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    modelo = SVR(kernel='rbf', C=100, epsilon=0.5)
    modelo.fit(X_train_scaled, y_train)

    y_pred = modelo.predict(X_test_scaled)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    resultados.append({'Ano': ano_teste, 'MAE': mae, 'MSE': mse, 'R2': r2})

# ===============================
# 3. Geração de Métricas e Gráficos
# ===============================
result_df = pd.DataFrame(resultados)
result_df.to_csv('../tests/avaliacao_temporal_metricas.csv', index=False)

# Gráfico MAE por ano
plt.figure(figsize=(8,5))
plt.bar(result_df['Ano'].astype(str), result_df['MAE'], color='skyblue')
plt.title('MAE por Ano de Teste (SVR)')
plt.xlabel('Ano de Teste')
plt.ylabel('Erro Absoluto Médio (ton/ha)')
plt.tight_layout()
plt.savefig('../tests/images/avaliacao_mae_por_ano.png')
plt.show()

# Gráfico R² por ano
plt.figure(figsize=(8,5))
plt.bar(result_df['Ano'].astype(str), result_df['R2'], color='lightgreen')
plt.title('R² por Ano de Teste (SVR)')
plt.xlabel('Ano de Teste')
plt.ylabel('R² (Coeficiente de Determinação)')
plt.tight_layout()
plt.savefig('../tests/images/avaliacao_r2_por_ano.png')
plt.show()

# Gráfico de dispersão Produtividade Real vs Prevista (último ano testado)
ultimo_ano = result_df['Ano'].max()
df_ultimo = df[df['Ano'] == ultimo_ano]
X_ultimo = df_ultimo[['NDVI', 'Chuva (mm)', 'Temp. Máx. (C)', 'Temp. Mín. (C)', 'Mes']]
y_ultimo = df_ultimo['Produtividade (ton/ha)']
X_ultimo_scaled = scaler.transform(X_ultimo)
y_pred_ultimo = modelo.predict(X_ultimo_scaled)

plt.figure(figsize=(10,6))
plt.scatter(y_ultimo, y_pred_ultimo, alpha=0.7, color='orange')
plt.plot([y_ultimo.min(), y_ultimo.max()], [y_ultimo.min(), y_ultimo.max()], 'k--', lw=2)
plt.title(f'Produtividade Real vs Prevista - Ano {ultimo_ano}')
plt.xlabel('Produtividade Real (ton/ha)')
plt.ylabel('Produtividade Prevista (ton/ha)')
plt.tight_layout()
plt.savefig(f'../tests/images/disp_real_vs_prevista_{ultimo_ano}.png')
plt.show()
# Gráfico de Resíduos
residuos = y_ultimo - y_pred_ultimo
plt.figure(figsize=(10,4))
plt.scatter(y_ultimo, residuos, alpha=0.7, color='purple')
plt.axhline(0, linestyle='--', color='gray')
plt.title(f'Resíduos do Modelo SVR - Ano {ultimo_ano}')
plt.xlabel('Produtividade Real (ton/ha)')
plt.ylabel('Erro (Resíduo)')
plt.tight_layout()
plt.savefig(f'../tests/images/residuos_{ultimo_ano}.png')
plt.show()
# ===============================
# 4. Conclusão
# ===============================
print("Avaliação temporal do modelo SVR concluída. Resultados salvos em '../tests/avaliacao_temporal_metricas.csv'.")
