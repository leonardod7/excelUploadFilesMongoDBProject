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

- Python
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

#### <font color=gray>4) Requisitos Não Funcionais:</font>

- A aplicação deverá ser responsiva.
- A aplicação deverá utilizar o banco de dados MongoDB Atlas.
- A aplicação deverá ser hospedada no Heroku.
- O back-end da aplicação deverá ser desenvolvida em Python.
- O front-end da aplicação deverá ser desenvolvida em Dash Plotly.
- A aplicação deverá ser desenvolvida utilizando o framework Flask.
- A aplicação deverá ser desenvolvida utilizando o padrão de arquitetura MVC (Model-View-Controller).

Estamos utilizando esse conceito no projeto, onde o DAO lida com o acesso ao banco de dados, as classes como SPE representam o modelo de negócio e o Dash atua como uma camada de visualização (View)





## <font color=#ffcc00> Conhecendo o Projeto:</font>

#### <font color=#ffcc00>1) Arquitetura de Pastas do Projeto</font>

O projeto possui a seguinte divisão de pastas:

- > **.venv** - Ambiente virtual do Python.
- > **assets** - Contém os arquivos de imagem e formatação css.
- > **dao** - Contém as classes de CRUD da aplicação com o banco de dados.
- > **model** - Contém as classes de modelo da aplicação.
- > **pages** - Cada arquivo representa uma página da aplicação.
- > **app** - Arquivo com as configurações do app.
- > **index** - Arquivo principal responsável por iniciar a aplicação.



















[//]: # (![Docker]&#40;img/img_1.png&#41;)