# 🧱 Etapa 1 – Pré-processamento dos Dados

## 1️⃣ Organização dos Datasets

Nesta primeira etapa da Sprint 2, consolidamos os dados coletados na Sprint 1 em um único dataset unificado. As fontes utilizadas foram todas públicas e oficiais, conforme solicitado no desafio:

| Fonte | Tipo de Dado | Utilização no Projeto |
|:------|:-------------|:----------------------|
| **SATVeg – Embrapa** | NDVI mensal (por região) | Avaliação do vigor vegetativo da lavoura |
| **INMET – Estação Uberaba** | Clima (chuva, temperatura máxima e mínima) | Análise de influência climática sobre a produtividade |
| **IBGE – Produção Agrícola Municipal** | Produtividade agrícola (ton/ha) anual | Variável-alvo para o modelo preditivo |

### 📁 Estrutura do Dataset Final

Todos os dados foram organizados em um único arquivo `.csv` localizado no diretório `data/`, com as seguintes colunas:

- `Ano-Mes`: Período de referência (formato YYYY-MM)
- `NDVI`: Índice de vegetação por diferença normalizada
- `Chuva (mm)`: Total mensal de precipitação
- `Temp. Máx. (C)`: Temperatura máxima mensal
- `Temp. Mín. (C)`: Temperatura mínima mensal
- `Produtividade (ton/ha)`: Produtividade agrícola interpolada mensalmente

### 🗃️ Tratamento Inicial

- Conversão de datas para o formato datetime
- Interpolação dos valores anuais de produtividade para escala mensal
- Conferência de valores nulos, tipos e coerência dos dados

Essa estrutura padronizada permitiu que o modelo de IA fosse alimentado com dados temporais sincronizados e comparáveis ao longo dos meses e anos.

## 2️⃣ Tratamento e Limpeza dos Dados

Após consolidar os dados das fontes SATVeg, INMET e IBGE, realizamos um processo completo de limpeza e padronização para garantir a integridade e compatibilidade entre os datasets.

---

### 🔄 Conversão de Datas

Todos os registros foram organizados na escala **mensal**, com a coluna `Ano-Mes` convertida para o formato `datetime`. A partir dela, extraímos as colunas auxiliares `Ano` e `Mes`, fundamentais para análises sazonais e agrupamentos.

```python
df['Ano-Mes'] = pd.to_datetime(df['Ano-Mes'])
df['Ano'] = df['Ano-Mes'].dt.year
df['Mes'] = df['Ano-Mes'].dt.month

### 📉 Interpolação da Produtividade
A produtividade da cana-de-açúcar, obtida pelo IBGE, foi fornecida em escala anual. Para integrá-la aos dados mensais de NDVI e clima, aplicamos uma interpolação simples:
Cada valor anual foi uniformemente distribuído entre os 12 meses do respectivo ano.
Essa técnica garantiu a presença da variável de produtividade em todos os meses, mesmo com origem anual.

df['Produtividade (ton/ha)'] = df.groupby('Ano')['Produtividade (ton/ha)'].transform('mean')

ℹ️ Em uma versão futura, essa interpolação poderá ser aprimorada com técnicas mais robustas, como médias móveis, splines ou regressões temporais.

### 🧼 Tratamento de Valores Ausentes e Tipos

Realizamos a checagem de dados ausentes e a padronização dos tipos de dados:
 - Todas as colunas foram convertidas para tipos adequados (float64 para variáveis numéricas e datetime64 para datas).
 - Não foram encontrados valores nulos nas colunas principais após a junção e tratamento.

df.info()
df.isnull().sum()

### ✅ Resultado Final
Após o pré-processamento, o dataset final ficou estruturado da seguinte forma:
 - Um registro por mês (de 2019 a 2023), totalizando 60 linhas no conjunto principal;
 - Todas as variáveis numéricas consistentes e alinhadas no tempo;
 - Estrutura pronta para uso nas etapas de análise exploratória e construção do modelo de IA.