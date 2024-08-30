# SpotSat - Desafio de Classificação de Imagens de Satélite

## Descrição do Projeto

Este projeto faz parte do desafio da **SpotSat** e tem como objetivo desenvolver uma solução para a classificação de imagens de satélite, identificando áreas de floresta e não-floresta. A solução inclui uma API RESTful construída com Django, permitindo o upload de arquivos TIFF, a classificação das imagens, e a consulta dos resultados armazenados em um banco de dados **PostGIS**.

## Estrutura do Projeto

A estrutura do projeto está organizada da seguinte forma:

SpotSat/
│
├── data/
│   ├── processed/
│   │   ├── training/
│   │   │   ├── X_train_processed.npy
│   │   │   └── train_gdf_processed.shp
│   │   ├── validation/
│   │       ├── validX_train_processed.npy
│   │       └── validation_gdf_processed.shp
│   ├── raw/
│       ├── shapetraining.shp
│       ├── shapevalidation.shp
│       └── tifffiles/
│           ├── red.tif
│           ├── green.tif
│           └── blue.tif
│
├── model/
│   ├── agent/
│       └── random_forest_model.joblib
│
├── notebooks/
│   ├── exploration/
│   │   ├── data_exploration_shape_training_files.ipynb
│   │   └── data_exploration_shape_validation_files.ipynb
│   ├── training/
│       └── training_models_random_forest.ipynb
│
├── results/
│   ├── classification/
│   ├── geopackage/
│   ├── metrics/
│   └── raster/
│
├── spotsat/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── src/
│   ├── api/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── serializers/
│   │   └── views/
│   └── tests/
│
├── .env
├── .gitignore
├── data.zip
├── docker-compose.yml
├── Dockerfile
├── init_db.py
├── manage.py
├── nginx.conf
├── README.md
├── requirements.txt
└── wait-for-it.sh (se necessário)


### Descrição das Pastas

- **data/processed/**: Contém os arquivos processados, incluindo dados de treinamento e validação em formato NPY e Shapefile.
- **data/raw/**: Contém os arquivos brutos, como shapefiles de treinamento/validação e arquivos TIFF.
- **model/**: Armazena o modelo treinado (random_forest_model.joblib) na subpasta agent.
- **notebooks/**: Contém notebooks Jupyter para exploração de dados e treinamento do modelo.
  - **exploration/**: Explorando e analisando os dados inicialmente.
  - **training/**: Treinamento e validação do modelo Random Forest.
- **results/**: Armazena os resultados da classificação, incluindo shapefiles, geopackages, métricas e rasters gerados.
- **spotsat/**: Contém as configurações do projeto Django.
- **src/**: Diretório com a API Django, organizado com Controllers, Models, Serializers, Views, e testes.
- **.env**: Configurações de ambiente.
- **docker-compose.yml** e **Dockerfile**: Arquivos para configurar e rodar o ambiente Docker.
- **init_db.py**: Script para inicializar o banco de dados.
- **manage.py**: Arquivo principal do Django para executar comandos do projeto.
- **nginx.conf**: Configuração do Nginx para balanceamento de carga.

## Como Executar o Projeto

### Pré-requisitos

- Docker e Docker Compose instalados.
- Python 3.11 ou 3.10.

### Executando com Docker

1. Clone o repositório:
   
bash
   git clone https://github.com/seu_usuario/seu_repositorio.git
   cd seu_repositorio


2. Construa e inicie os containers:
   
bash
   sudo docker-compose up --build


3. Acesse a API Django na porta 8000.

### Executando os Notebooks

Os notebooks podem ser abertos e executados no Visual Studio Code, Jupyter Notebook, Google Colab, ou qualquer outro editor que suporte Jupyter.

## Endpoints da API

### POST /api/classification/

Recebe um arquivo TIFF e retorna a classificação (floresta ou não-floresta) junto com os metadados da imagem.

**Exemplo de Uso com CURL:**
bash
curl -X POST http://localhost:8000/api/classification/ \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/caminho/para/seu/arquivo.tif"

**Exemplo de Resposta (200):**
json
{
  "id": 1,
  "file_path": "FAA_UTM18N_NAD83.tif",
  "cloud_coverage": null,
  "processing_date": "2024-08-30",
  "geom": null,
  "classification_result": {
    "idRaster": "957066bc-bb9e-4c34-8690-e2290c787dce",
    "classification": "floresta",
    "file_name": "FAA_UTM18N_NAD83.tif",
    "width": 1491,
    "height": 1387,
    "crs": "EPSG:26918",
    "transform": [223586.23651964564,23.927070933333344,0.0,4217906.977453323,0.0,-23.927070933333344],
    "count": 3,
    "driver": "GTiff",
    "cloud_coverage": "N/A"
  }
}

--------------------------------
### GET /api/consultation/

Permite consultar as classificações anteriores, com opções de filtro por idRaster, range de datas ou cloud_coverage.

**Exemplo de Uso com CURL:**
bash
curl -X GET "http://localhost:8000/api/consultation/?idRaster=<UUID>"

**Exemplo de Resposta (200):**
json
{
  "id": 1,
  "file_path": "FAA_UTM18N_NAD83.tif",
  "cloud_coverage": null,
  "processing_date": "2024-08-30",
  "geom": null,
  "classification_result": {
    "idRaster": "957066bc-bb9e-4c34-8690-e2290c787dce",
    "classification": "floresta",
    "file_name": "FAA_UTM18N_NAD83.tif",
    "width": 1491,
    "height": 1387,
    "crs": "EPSG:26918",
    "transform": [223586.23651964564,23.927070933333344,0.0,4217906.977453323,0.0,-23.927070933333344],
    "count": 3,
    "driver": "GTiff",
    "cloud_coverage": "N/A"
  }
}

-------------------------------
### GET /api/metrics/

Retorna as métricas de avaliação do modelo em formato JSON.

**Exemplo de Uso com CURL:**
bash
curl -X GET http://localhost:8000/api/metrics/

**Exemplo de Resposta (200):**
json
{
  "precision": [0.98, 0.78],
  "recall": [0.73, 0.98],
  "accuracy": 0.86,
  "confusion_matrix": [
    [48, 18],
    [1, 65]
  ]
}
-------------------------------
Claro! Aqui está a seção dos testes reformulada para adicionar ao seu README:

---

## Testes Automatizados

Este projeto inclui uma série de testes automatizados para garantir a funcionalidade correta da API. Os testes foram criados para validar cada uma das rotas principais e assegurar que os endpoints estão funcionando conforme esperado.

### Estrutura dos Testes

Os testes estão organizados da seguinte maneira:

- **`test_classification.py`**: Valida a rota `/api/classification/`, garantindo que a classificação de imagens TIFF seja realizada corretamente e que a resposta contenha os metadados esperados, incluindo a classificação ("floresta" ou "não-floresta").

- **`test_consultation.py`**: Testa a rota `/api/consultation/`, verificando se as consultas de classificações anteriores podem ser feitas com sucesso, seja por `idRaster`, `intervalo de datas`, ou `cloud_coverage`.

- **`test_metrics.py`**: Verifica a rota `/api/metrics/`, assegurando que as métricas do modelo de classificação sejam retornadas corretamente em formato JSON.

### Executando os Testes

Para executar todos os testes, siga os passos abaixo:

1. Certifique-se de que você está no diretório raiz do projeto.

2. Utilize o seguinte comando para rodar todos os testes:

   ```bash
   pytest src/api/tests/
   ```

Este comando irá executar todos os testes definidos na pasta `tests` dentro de `src/api/`, permitindo que você valide rapidamente se o sistema está funcionando conforme esperado.

--------------------------------
## Métricas do Modelo

Após o treinamento do modelo **Random Forest**, os seguintes resultados foram obtidos:

- **Matriz de Confusão**:
  
plaintext
  [[48, 18],
   [1,  65]]


- **Relatório de Classificação**:
  - **Precisão**: 98% (Floresta), 78% (Não-Floresta)
  - **Recall**: 73% (Floresta), 98% (Não-Floresta)
  - **Acurácia**: 86%

Essas métricas são salvas em um arquivo JSON (metrics_training_model.json) e em um PDF (metrics_and_validation.pdf), na pasta **results**.

## Conclusão
Este projeto foi desenvolvido como parte de um desafio proposto pela SpotSat, com o objetivo de criar uma solução eficaz para a classificação de imagens de satélite. Ele utiliza ferramentas modernas como Docker, Django, e Random Forest, e segue boas práticas de desenvolvimento de software e machine learning.