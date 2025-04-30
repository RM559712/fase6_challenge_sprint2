# svr_treinamento_gpu.py
# Diretório recomendado: scripts/

"""
Script alternativo de treinamento utilizando o modelo SVR (Support Vector Regression)
para previsão da produtividade da cana-de-açúcar. Utiliza os dados unificados do diretório ../data/
e salva os gráficos de resultado no diretório ../tests/images/

Este modelo foi escolhido após testes comparativos com o XGBoost, pois apresentou desempenho
melhor nos dados disponíveis. O SVR é indicado para bases pequenas e com pouca variabilidade,
o que se alinha ao cenário do projeto.
"""

# ============================================================
# 1. Importação das Bibliotecas
# ============================================================
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

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

# Criação de novas features derivadas simples
# Diferença térmica e índice climático (chuva sobre soma de temperaturas)
df['Temp_Diff'] = df['Temp. Máx. (C)'] - df['Temp. Mín. (C)']
df['Indice_Climatico'] = df['Chuva (mm)'] / (df['Temp. Máx. (C)'] + 1)

X = df[['NDVI', 'Chuva (mm)', 'Temp. Máx. (C)', 'Temp. Mín. (C)', 'Mes', 'Temp_Diff', 'Indice_Climatico']]
y = df['Produtividade (ton/ha)']

# Normalização das features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# ============================================================
# 4. Treinamento com SVR
# ============================================================
modelo = SVR(kernel='rbf', C=100, epsilon=0.5)
modelo.fit(X_train, y_train)

# ============================================================
# 5. Avaliação do Modelo
# ============================================================
y_pred = modelo.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n✅ Avaliação do Modelo SVR:")
print(f"MAE (Erro Absoluto Médio): {mae:.2f} ton/ha")
print(f"MSE (Erro Quadrático Médio): {mse:.2f}")
print(f"R² (Coeficiente de Determinação): {r2:.2f}")

# Validação cruzada para robustez das métricas
cv_r2 = cross_val_score(modelo, X_scaled, y, cv=5, scoring='r2')
print(f"R² médio com validação cruzada (5-fold): {cv_r2.mean():.2f}")

# ============================================================
# 6. Gráfico: Produtividade Real vs Prevista
# ============================================================
plt.figure(figsize=(10,6))
plt.scatter(y_test, y_pred, alpha=0.7, color='green')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
plt.xlabel('Produtividade Real (ton/ha)')
plt.ylabel('Produtividade Prevista (ton/ha)')
plt.title('Produtividade Real vs Prevista - SVR')
plt.grid(True)
plt.tight_layout()
plt.savefig('../tests/images/svr_real_vs_prevista.png')
plt.show()

# ============================================================
# 7. Gráfico de Resíduos
# ============================================================
residuos = y_test - y_pred
plt.figure(figsize=(10,4))
plt.scatter(y_test, residuos, alpha=0.7, color='orange')
plt.axhline(0, linestyle='--', color='gray')
plt.title('Resíduos do Modelo SVR')
plt.xlabel('Produtividade Real (ton/ha)')
plt.ylabel('Erro (Resíduo)')
plt.grid(True)
plt.tight_layout()
plt.savefig('../tests/images/svr_residuos.png')
plt.show()

print(f"\n📊 Desvio padrão dos resíduos: {np.std(residuos):.2f} ton/ha")

# ============================================================
# 8. Maiores Erros Absolutos
# ============================================================
df_resultado = pd.DataFrame({
    'Produtividade Real': y_test.values,
    'Produtividade Prevista': y_pred
})
df_resultado['Erro Absoluto'] = abs(df_resultado['Produtividade Real'] - df_resultado['Produtividade Prevista'])
print("\n🔎 Top 3 maiores erros absolutos:")
print(df_resultado.sort_values(by='Erro Absoluto', ascending=False).head(3))

# ============================================================
# 9. Exportação das Métricas
# ============================================================
df_metricas = pd.DataFrame([{
    'Modelo': 'SVR RBF',
    'MAE': mae,
    'MSE': mse,
    'R2': r2,
    'R2_CrossVal': cv_r2.mean()
}])
df_metricas.to_csv('../tests/svr_metricas.csv', index=False)
print("\n✅ Métricas exportadas para ../tests/svr_metricas.csv")