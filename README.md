
# New York Times - Top Stories

<details open>
<summary>Documentação (PT-BR)</summary>

\
*Além das manchetes: Quais insights podemos desvendar das notícias exibidas na página inicial do maior jornal do planeta?*

----

\
O The New York Times fornece uma API que permite extrair algumas informações do site, incluindo as notícias de um determinado período, opiniões e as principais manchetes - que é a fonte de dados deste projeto

Esse project tem como objetivo construir um pipeline de ingestão de dados utilizando Python, Databricks e SQL que nos permita extrair as principais manchetes de cada dia, armazena-las em suas respectivas camadas da Arquitetura Medalhão - Bronze, Silver e Gold - e analisar os dados através de um dashboard.

\
**Créditos**

Todos o dados deste projeto são fornecidos pelo The New York Times em https://developer.nytimes.com/.

Este projeto é baseado no projeto "Lago do Mago" construído pelo Teo Me Why. O Téo fornece cursos gratuitos sobre análise, engenharia e ciência de dados. Eu recomendo o canal dele para qualquer um que queira saber mais sobre dados. Canal do youtube:  https://www.youtube.com/@teomewhy.


## **Detalhes do Projeto**


### 1. Pipeline de Dados

\
O pipeline foi construído usando a Arquitetura Medalhão. O processo é dividido nas camadas Raw, Bronze, Silver e Gold, cada uma com um determinado nível de limpeza e tratamento dos dados. A imagem abaixo ilustra como o pipeline foi desenhado.

\
<img width="1252" height="695" alt="image" src="Pipeline Screenshot.png" />


#### 1.1 Camadas de Dados
\
**1.1.1 Camada Raw**

Os dados brutos (raw) são extraídos no formato JSON da API do NY Times utilizando uma Lambda Function agendada diariamente às 16h (UTC - 3:00). Os dados são armazenado em um bucket S3 na AWS sem nenhum tratamento, exceto pela inclusão da data de referência em que os dados foram extraídos.

\
**1.1.2 Camada Bronze**

Com os dados salvos no S3, fazemos a leitura utilizando Jobs agendados no Databricks. Através do python, usamos o  Databricks Autoloader para identificar os novos arquivos adicionados no Bucket e realizar a ingestão incremental numa tabela Delta. Nenhum tratamento adicional é feito nessa etapa.

\
**1.1.3 Camada Silver**

É aqui que começamos a realizar alguns tratamentos nos dados. As colunas são renomeadas para melhorar a legibilidade, e a coluna de "autores" é transformada num array, para manter o padrão com os demais dados. Algumas colunas são removidas nessa camada, pois não seriam úteis para as análises.

A tabela da camada Silver é atualizada utilizando o recurso de Delta Change Data Feed, que permite identificar as alterações feita na camada bronze, e realizar as atualizações em Silver de forma incremental, reduzindo o tempo de execução e os custos de processamento.

\
**Lista de transforamções:**


| Bronze || Silver ||
|--|--|--|--|
|Nome da coluna (Bronze) | Tipo de dado (Bronze) | Nome da coluna (Silver) | Tipo de dado (Silver)|
| title | string | ds_headline | string |
| abstract | string | ds_lead | string |
| byline | string | ds_authors | array |
| section | string | ds_section | string |
| subsection | string | ds_subsection | string |
| url | string | ds_url | string |
| geo_facet | array | ds_locations | array
| des_facet | array | ds_topics | array
| org_facet | array | ds_organizations | array
| perc_facet | array | ds_persons | array
| published_date | string | - | -
| ref_date | string | ref_date | date
| short_url | string | removido | -
| multimedia | array | removido | - 
| item_type | string | removido |-
| kicker | string | removido | -
| material_type_facet | string | removido | -
| created_date | string | removido | - 
| uri | string | removido | - 

\
**1.1.4 Camada Gold**

A camada Gold serve os processos de Analytics, então ela contem tabelas otimizadas com dados sumarizados:

- Daily Trending Topics: uma contagem da quantidade de notícias para cada assunto

- Weekly Trending Persons: uma contagem de quantas vezes cada pessoa/figura pública é mencionada na semana (considerando a semana do ano)

- Last Month Trendings Organizations: contagem de quantas vezes cada organização (empresas, partidos políticos, etc) foi mencionada nos últimos 30 dias

- Last Month Top Authors: contagem de quantas notícias cada jornalista teve exibida na página principal nos últimos 30 dias.

\
Cada notícia pode ter vários topicos, autores e pessoas mencionadas, salvas em um array. Por isso, o array é "aberto" para listar individualmente cada item e identificar, por exemplo, casos em que uma notícia foi feita por 2 ou mais autores, de forma que ela seja contabilizada para cada um deles.


#### 1.2 Databricks Workflows

O pipleine de ingestão roda automaticamente utilizando o recurso do Databricks de Jobs & Pipelines.

<img width="1252" height="695" alt="image" src="Databricks Workflow Screenshot.png" />

\
Cada camada possui um código de ingestão genérico que usa os parâmetros do workflows do Databricks para se adaptar à cada tabela. Isso permite que novas tabelas sejam adicionadas sem precisar alterar o código de ingestão, apenas adicionando a query para a nova tabela e uma nova etapa no Workflow.

### 2. Análise dos dados

Dados só têm valor quanto são transformados em métricas e insights que possam ser usado por pessoas e organizations para obter conhecimento e construir soluções.

Para este projeto, decidi construir um dashboard simples no próprio Databricks para exibir as informações da camada Gold. O dashboard atualiza os gráficos baseado na data selecionado, exibindo:

- Assuntos mais mencionados no dia
- Pessoas mais mencionadas na semana
- Organizações mais mencionadas nos últimos 30 dias
- Autores mais mencionados nos últimos 30 dias

<img width="1252" height="695" alt="image" src="Dashboard Screenshot.png" />

</details>

---

'
<details>

<summary> Documentation (EN-US)</summary>

\
*Beyond the headlines: What insights can we uncover from the news displayed in the front page of the world's biggest newspaper?*

----

\
The New York Times provides API endpoints that allow users to get data from their website, including news from a specific period, reviews and the top stories - which is the data source of this project.

This project aims build a pipeline that allow us to get the Top Stories of each day, save then to corresponding data lakers - Bronze, Silver and Gold - and analyze the data in a dashboard

\
**Credits**

All the data used in this project is provided by the New York Times at https://developer.nytimes.com/.

This project is based in the "Lago do Mago" project built by Teo Me Why. Téo provides free courses about data analytics, engineering and machine learning. I highly recommend his channel for anyone who wants to learn about data, look at https://www.youtube.com/@teomewhy.


## **Project Details**


### 1. Data Pipeline

\
The pipeline has been built using the Medallion Architecture. It divides the process in Raw, Bronze, Silver and Gold Data Layers, each one with specific level of cleaning and treatments. The picture bellow illustrates how the workflow has been designed.

\
<img width="1252" height="695" alt="image" src="Pipeline Screenshot.png" />


#### 1.1 Data Layers

\
**1.1.1 Raw Data Layer**

The raw data is extracted ins JSON format from the NY Times API through a Lambda Function scheduled to run daily at 7 p.m (UTC). The data is saved in a S3 Bucket in AWS without additional treatment but the inclusion of the reference date of when the news were extracted.

\
**1.1.2 Bronze Data Layer**

With the raw data saved to S3, we read this data using a Scheduled Job in Databricks. The python code uses Databricks Autoloader to identify new files that have been added to the S3 Bucket, proccess the new data and add then into a Delta Table, adding the ingestion date to it's contents. No further treatments are made

\
**1.1.3 Silver Data Layer**

This is where we start to do some treatments in our data. The columns are renamed for better readbility, the "author" collumn is treated to keep a pattern with the other list columns, and we also remove the columns that won't be useful in our future analysis. The Silver table is updated using the Delta Change Data Feed feature, allowing us to identify changes made to the Bronze table, and processing only this new data into the Silver table, improving running time and costs.

\
**List of Transformations:**


| Bronze || Silver ||
|--|--|--|--|
|Bronze Column Name | Bronze Column Type | Silver Column Name | Silver Column Type |
| title | string | ds_headline | string |
| abstract | string | ds_lead | string |
| byline | string | ds_authors | array |
| section | string | ds_section | string |
| subsection | string | ds_subsection | string |
| url | string | ds_url | string |
| geo_facet | array | ds_locations | array
| des_facet | array | ds_topics | array
| org_facet | array | ds_organizations | array
| perc_facet | array | ds_persons | array
| published_date | string | - | -
| ref_date | string | ref_date | date
| short_url | string | removed | -
| multimedia | array | removed | - 
| item_type | string | removed |-
| kicker | string | removed | -
| material_type_facet | string | removed | -
| created_date | string | removed | - 
| uri | string | removed | - 

\
**1.1.4 Gold Data Layer**

The gold layer aims to serve the analytics proccess, so it contains tables optimized with summarized data. It contains:

- Daily Trending Topics: a simple count of the stories for each topic and day

- Weekly Trending Persons: a count of how many times each public figure is mentioned in the stories each week
- Last Month Trendings Organizations: a count of how many stories each organizations (enterprises, political parties etc) had in the main page in the last 30 day
- Last Month Top Authors: a count of how many stories each author had in the main page in the last 30 days.

Since the Stories's topics,authors and persons are a array-like information, I had to explode it to identify cases where, for an example, an author has worked alonged with others, and so I've counted it as a story for each one of them.


#### 1.2 Databricks Workflows

The ingestion pipeline is runs automatically using the Databricks Jobs & Pipelines resources.

<img width="1252" height="695" alt="image" src="Databricks Workflow Screenshot.png" />

\
Each layers has a generic ingestion code that uses the workflow parameters to adapt to each table. This allows us to add new tables without having to update the ingestion code itself, but only building its query and adding a new step to the workflow

### 2. Data Analysis

Data is only valuable when it turns into metrics and insights that can be used by people and organizations to build knowledge and solutions.

For this project, I decided to build a simple dashboard inside databricks to display the Gold Layers informations.

The dashboard updates the visualizations based on the select date, and shows up:

- Trending topics of the selected day
- Trending persons of the week of year of the selected day
- Trending organizations in the last 30 days from the selected day
- Top authors in the last 30 days from the selected day

<img width="1252" height="695" alt="image" src="Dashboard Screenshot.png" />
</details>