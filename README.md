# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/images/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Enterprise Challenge - Sprint 2 - Ingredion

## 👨‍👩 Grupo

Grupo de número <b>4</b> formado pelos integrantes mencionados abaixo.

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/cirohenrique/">Ciro Henrique</a> ( <i>RM559040</i> )
- <a href="javascript:void(0)">Enyd Bentivoglio</a> ( <i>RM560234</i> )
- <a href="https://www.linkedin.com/in/marcofranzoi/">Marco Franzoi</a> ( <i>RM559468</i> )
- <a href="https://www.linkedin.com/in/rodrigo-mazuco-16749b37/">Rodrigo Mazuco</a> ( <i>RM559712</i> )

## 👩‍🏫 Professores:

### Tutor(a) 
- <a href="https://www.linkedin.com/in/leonardoorabona/">Leonardo Ruiz Orabona</a>

### Coordenador(a)
- <a href="https://www.linkedin.com/in/profandregodoi/">André Godoi</a>

## 📜 Descrição

<b>Referência</b>: https://on.fiap.com.br/mod/assign/view.php?id=475221&c=12936

### 🧩 Etapa 1 – Pré-processamento dos Dados

Reunimos três conjuntos de dados:
- NDVI mensal da região de Uberaba/MG (2019–2023)
- Dados climáticos: temperatura máxima, mínima e chuvas (INMET)
- Produtividade da cana-de-açúcar (IBGE), interpolada por mês

> 🔗 Dados salvos em: [`data/dataset_unificado.csv`](data/dataset_unificado.csv)

Foram realizados:
- Conversão de datas para o padrão `Ano-Mês`
- Remoção de valores inconsistentes
- Agrupamento mensal e padronização

Mais informações, clique [aqui](https://github.com/RM559712/fase6_challenge_sprint2/blob/main/document/ACTIVITIES.md) e [aqui](https://github.com/RM559712/fase6_challenge_sprint2/blob/main/document/ETAPA1_SPRINT2.md).

---

### 🔍 Etapa 2 – Análise Exploratória & Seleção de Variáveis

Selecionamos as seguintes variáveis para previsão da produtividade:

| Variável              | Justificativa                                   |
|----------------------|--------------------------------------------------|
| NDVI                 | Indica o vigor vegetativo da cana                |
| Temperatura Máxima   | Altas temperaturas afetam o crescimento da planta|
| Temperatura Mínima   | Pode influenciar o metabolismo da cultura        |
| Chuvas               | Essenciais para o desenvolvimento da lavoura     |
| Mês                  | Consideramos a sazonalidade                      |

> 📊 Ver análises em [`scripts/analise_exploratoria.ipynb`](scripts/analise_exploratoria.ipynb)

Mais informações, clique [aqui](https://github.com/RM559712/fase6_challenge_sprint2/blob/main/document/ETAPA2_SPRINT2.md)

---

### 🧠 Etapa 3 – Modelo de Inteligência Artificial

Optamos por usar o modelo `RandomForestRegressor` pela sua capacidade de:
- Lidar bem com dados tabulares e não lineares
- Interpretabilidade e análise da importância das variáveis

#### 🔧 Etapas:
- Treinamento com dados de 2019 a 2022
- Validação com dados de 2023
- Ajuste de hiperparâmetros com GridSearch

Mais informações, clique [aqui](https://github.com/RM559712/fase6_challenge_sprint2/blob/main/document/ETAPA3_SPRINT2.md)

---

### 📈 Etapa 4 – Avaliação do Modelo

#### ✅ Métricas Obtidas:
- **R²:** 0.87
- **RMSE:** 1.12 toneladas/ha
- **MAE:** 0.91 toneladas/ha

Mais informações, clique [aqui](https://github.com/RM559712/fase6_challenge_sprint2/blob/main/document/ETAPA4_SPRINT2.md)

---

### 🎥 Demonstração em Vídeo

📺 A execução de todo o processo também pode ser visualizada através de um vídeo clicando [aqui](https://www.youtube.com/watch?v=[PENDENTE]).

---

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

1. <b>assets</b>: Diretório para armazenamento de arquivos complementares da estrutura do sistema.
    - Diretório "images": Diretório para armazenamento de imagens.

2. <b>config</b>: Diretório para armazenamento de arquivos em formato <i>json</i> contendo configurações.

3. <b>document</b>: Diretório para armazenamento de documentos relacionados ao sistema.

4. <b>scripts</b>: Diretório para armazenamento de scripts.

5. <b>src</b>: Diretório para armazenamento de código fonte do sistema.

6. <b>data</b>: Diretório para armazenamento dos dados do projeto

7. <b>tests</b>: Diretório para armazenamento de resultados de testes.
	- Diretório "images": Diretório para armazenamento de imagens relacionadas aos testes efetuados.

8. <b>README.md</b>: Documentação do projeto em formato markdown.

<i><strong>Importante</strong>: A estrutura de pastas foi mantida neste formato para atender ao padrão de entrega dos projetos.</i>

## 🔧 Como executar o código

Esse projeto não possui parte técnica para execução.

## 📋 Licença

Desenvolvido pelo Grupo 4 para o projeto da fase 6 (<i>Enterprise Challenge - Sprint 2 - Ingredion</i>) da <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a>. Está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>