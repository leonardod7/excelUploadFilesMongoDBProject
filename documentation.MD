<div>
    <img src="assets/img/img.png" width="140" height="100">
</div>

---
Autor: Leonardo dos Santos Costa
<br>
<font color=#ffcc00>MongoDB Atlas - Projeto PUC </font>

Scope: Data Preparation

# <font color=#ffcc00>MongoDB Atlas - Projeto PUC </font>

## <font color=#ffcc00> Considerações do Projeto:</font>

#### <font color=gray>1) Objetivo:</font>

O objetivo do projeto é criar uma aplicação web que receba arquivos em formato Excel do usuário referente aos demonstrativos financeiros: Demonstração de Resultado, Balanço Patrimonial e Fluxo de Caixa.
Os arquivos deverão seguir um padrão de formatação e a aplicação deverá realizar a leitura dos arquivos, armazenar os dados no banco de dados e exibir os dados na tela quando solicitado.

#### <font color=gray>2) Tecnologias Utilizadas:</font>

- Python 3.12
- Flask
- MongoDB Atlas
- HTML
- CSS
- Dash Plotly

#### <font color=gray>3) Requisitos Funcionais:</font>

- O usuário poderá enviar arquivos em formato Excel, através da funcionalidade **Drag and Drop**.
- A aplicação deverá realizar a leitura dos arquivos e armazenar os dados no banco de dados.
- A aplicação deverá exibir os dados na tela quando solicitado.
- A aplicação deverá exibir a quantidade de documentos armazenados.
- A aplicação deverá apresentar opções de consulta e cadastro de arquivos para 3 modalidades de usinas: Eólicas, Solar e Hidrelétricas.
- A aplicação deverá permitir a exclusão de arquivos.
- A aplicação não deverá permitir a exclusão de arquivo quando restar apenas 1 único arquivo. Ela deverá exibir uma mensagem de erro.

#### <font color=gray>4) Requisitos Não Funcionais:</font>

- A aplicação deverá ser responsiva.
- A aplicação deverá utilizar o banco de dados MongoDB Atlas.
- A aplicação deverá ser hospedada no Heroku.
- O back-end da aplicação deverá ser desenvolvida em Python.
- O front-end da aplicação deverá ser desenvolvida em Dash Plotly.
- A aplicação deverá ser desenvolvida utilizando o framework Flask.
- A aplicação deverá ser desenvolvida utilizando o padrão de arquitetura MVC (Model-View-Controller).

Estamos utilizando esse conceito no projeto, onde o DAO lida com o acesso ao banco de dados, as classes como SPE representam o modelo de negócio e o Dash atua como uma camada de visualização (View)





## <font color=#ffcc00> 1) Conhecendo o Projeto:</font>

### <font color=#ffcc00>1.1) Arquitetura de Pastas do Projeto</font>

O projeto possui a seguinte divisão de pastas:

- > **.venv** - Ambiente virtual do Python.
- > **assets** - Contém os arquivos de imagem e formatação css.
- > **components** - Contém os componentes da aplicação.
- > **dao** - Contém as classes de CRUD da aplicação com o banco de dados.
- > **functions** - Contém as funções auxiliares da aplicação.
- > **model** - Contém as classes de modelo da aplicação.
- > **pages** - Cada arquivo representa uma página da aplicação.
- > **.env** - Contém as variáveis de ambiente para conexão com cada banco de dados.
- > **app** - Arquivo com as configurações do app.
- > **index** - Arquivo principal responsável por iniciar a aplicação.
- > **requirements** - Arquivo com as dependências do projeto.

### <font color=#ffcc00>1.2) Configuração Mongo DB </font>
  


## <font color=#ffcc00> 2) Arquivos.py:</font>

### <font color=#ffcc00>2.1) app.py </font>


```python
# Importando as bibliotecas 
import dash
import dash_bootstrap_components as dbc
from flask_caching import Cache  # pip install Flask-Caching

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server
app.config.suppress_callback_exceptions = True


# Configuração do cache
cache = Cache(app.server, config={
    'CACHE_TYPE': 'simple',  # Pode mudar para 'redis', 'filesystem', etc. conforme necessidade
    'CACHE_DEFAULT_TIMEOUT': 300  # Cache expira em 5 minutos (300 segundos)
})
```


Este arquivo configura o aplicativo Dash e define as principais configurações, incluindo o cache e os temas para os estilos visuais.
Utilize este arquivo para centralizar as configurações do servidor e iniciar o aplicativo.

Dependências:
-------------
- dash
- dash_bootstrap_components
- flask_caching

Instalação:
-------------
Certifique-se de instalar as dependências necessárias: 
- > pip install dash dash-bootstrap-components Flask-Caching

Descrição das Configurações:
----------------------------
- Tema: SANDSTONE do Dash Bootstrap Components
- Cache: Configurado com 'simple' como cache padrão e um tempo limite de 300 segundos (5 minutos).

Parâmetros do Cache:
--------------------
CACHE_TYPE:
Define o tipo de backend do cache:
- 'simple': Armazena os dados de cache na memória do servidor. É uma opção fácil e rápida para desenvolvimento.
- 'redis': Requer um servidor Redis e é recomendado para ambientes de produção, onde o cache precisa ser compartilhado.
- 'filesystem': Armazena o cache em arquivos locais. Útil para persistir dados temporários.

CACHE_DEFAULT_TIMEOUT:
Tempo, em segundos, para o cache expirar automaticamente. Neste caso, está definido para 300 segundos (5 minutos).
Esse valor pode ser ajustado conforme a necessidade do projeto.

Uso do Cache:
-------------
- O cache pode ser aplicado em callbacks do Dash para otimizar o desempenho, evitando processamento repetitivo para dados que
  não mudam com frequência.
- Para utilizar o cache em um callback, basta aplicar o decorador `@cache.memoize(timeout=N)`, onde `N` é o tempo de cache em segundos.















Precisamos em Network Access, adicionar o IP 0.0.0.0/0, para que qualquer máquina possa acessar o banco de dados.


[//]: # (![Docker]&#40;img/img_1.png&#41;)