# 🎯 Etapa 2 – Extração de Informações Relevantes

## 1️⃣ Definição das Variáveis-Chave

Com base na análise exploratória realizada na Sprint 2, definimos as seguintes variáveis-chave para a construção do modelo de previsão de produtividade agrícola:

| Variável | Descrição | Justificativa |
|:---------|:----------|:--------------|
| **NDVI** | Índice de Vegetação por Diferença Normalizada | Representa o vigor vegetativo da lavoura, com forte relação com o crescimento e produtividade. |
| **Chuva (mm)** | Volume de precipitação mensal | A água é um fator fundamental para o desenvolvimento da cana-de-açúcar. |
| **Temperatura Máxima (°C)** | Temperatura máxima mensal | Altas temperaturas podem causar estresse térmico e reduzir o NDVI e a produtividade. |
| **Temperatura Mínima (°C)** | Temperatura mínima mensal | Impacta o metabolismo das plantas, embora com influência mais sutil na região analisada. |
| **Mês do ano** | Mês de referência | Captura a sazonalidade agrícola, permitindo que o modelo aprenda padrões anuais de crescimento e entressafra. |

### 📚 Resumo da Escolha

Essas variáveis foram selecionadas pois:

- Têm **impacto agronômico direto** no crescimento da cana-de-açúcar.
- Estão **disponíveis em bases públicas confiáveis** (INMET, Embrapa SATVeg, IBGE).
- **Mostraram correlação moderada ou consistente** com a produtividade agrícola nos dados explorados.
- Permitem que o modelo capte tanto **tendências sazonais** quanto **eventos climáticos anormais**.

---

## 2️⃣ Análise da Relação entre NDVI e Produtividade Agrícola

A partir da análise exploratória realizada, foi possível identificar padrões importantes na série temporal do NDVI e sua relação com a produtividade da cultura da cana-de-açúcar em Uberaba/MG:

### 📈 Padrões Observados:

- **Picos de NDVI:** 
  - Ocorreram, em geral, entre os meses de **dezembro e abril**.
  - Estes períodos indicam **maior vigor vegetativo**, associado à fase de crescimento ativo da cana-de-açúcar.

- **Quedas no NDVI:**
  - Foram mais frequentes entre **junho e agosto**.
  - Essa queda coincide com **épocas de seca** na região e **fase de maturação ou colheita** da cultura.

- **NDVI Médio Anual:**
  - Anos com **NDVI médio mais elevado** apresentaram **maiores produtividades agrícolas**.
  - Mesmo pequenas variações no NDVI anual mostraram influência nas oscilações de produtividade.

---

### 🧠 Interpretação Agronômica:

- O **NDVI** é um excelente **indicador precoce de produtividade**: quanto maior o vigor vegetativo ao longo do ciclo, maior tende a ser a produção ao final da safra.
- A **sazonalidade agrícola** da cana-de-açúcar foi refletida nos ciclos do NDVI, validando sua escolha como principal variável preditiva.
- As **oscilações climáticas** (chuvas e temperaturas extremas) afetaram o padrão do NDVI e, consequentemente, impactaram a produtividade.

---

### 🔎 Períodos Críticos Identificados:

| Fase | Período | Impacto |
|:-----|:--------|:--------|
| Crescimento ativo | Dezembro a Abril | NDVI elevado → maior acúmulo de biomassa |
| Maturação/Colheita | Junho a Agosto | NDVI reduzido → início da colheita ou estresse hídrico |
| Recuperação/Rebrota | Setembro a Novembro | Retomada gradual do NDVI |

---

## 📚 Conclusão

A análise reforça que o acompanhamento do NDVI ao longo do tempo permite prever tendências de produtividade agrícola, justificando seu uso como variável-chave no modelo de IA proposto.

---

## 3️⃣ Segmentação de Áreas Específicas de Cultivo

Embora a plataforma SATVeg não forneça segmentações por talhões agrícolas automaticamente, é possível **simular uma segmentação funcional** com base nos próprios valores de NDVI obtidos por pixel ou média de área.

### 🗺️ Abordagem Utilizada:

Para esta análise, aplicamos uma **técnica de segmentação simples por limiar (threshold)**:

- Consideramos que **áreas com NDVI > 0.60** representam regiões de **alto vigor vegetativo**, indicando condições favoráveis de crescimento.
- Por outro lado, **áreas com NDVI < 0.45** foram interpretadas como regiões de **baixa vegetação ou possível estresse agrícola**.

---

### 🔍 Justificativa:

- A segmentação por limiar é uma técnica eficiente e acessível para destacar **zonas críticas ou produtivas** em uma região agrícola.
- Em aplicações mais avançadas, seria possível utilizar imagens georreferenciadas do SATVeg com ferramentas de visão computacional (ex: OpenCV, rasterio, shapely) para realizar:
  - Segmentações por contorno
  - Comparação entre ciclos de crescimento
  - Detecção automática de áreas improdutivas

---

### 🧪 Exemplo de Código (simulação simplificada):

# 🔄 Cópia do DataFrame original para não alterar os dados originais
df_segmentado = df.copy()

# 🧱 Segmentação do NDVI em três faixas com base em limiares:
# - NDVI de 0.00 a 0.45  → Baixo vigor (estresse, corte ou vegetação degradada)
# - NDVI de 0.45 a 0.60  → Vigor moderado (fase de recuperação, rebrota ou seca parcial)
# - NDVI de 0.60 a 1.00  → Alto vigor (fase de crescimento ativo e saudável)
df_segmentado['Classe NDVI'] = pd.cut(
    df_segmentado['NDVI'],                     # coluna a ser segmentada
    bins=[0, 0.45, 0.6, 1.0],                   # limites dos intervalos
    labels=['Baixo vigor', 'Vigor moderado', 'Alto vigor']  # rótulos atribuídos
)

# 📊 Visualização da quantidade de registros por faixa de vigor
# Isso nos ajuda a entender como o NDVI está distribuído entre as classes simuladas
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 4))
sns.countplot(data=df_segmentado, x='Classe NDVI', palette='Set2')

# 🖼️ Título e rótulos do gráfico
plt.title('Distribuição de Áreas por Faixa de NDVI')
plt.ylabel('Número de Ocorrências')
plt.xlabel('Classe de Vigor Vegetativo')

# 🔽 Ajuste para melhor visualização e salvamento do gráfico
plt.tight_layout()
plt.savefig('../tests/images/segmentacao_ndvi_classes.png')
plt.show()

