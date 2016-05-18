# SALIC api

API aberta para o portal NOVO SALIC. Tem por objetivo expor os dados de projetos da lei Rouanet.


## Instalação Automatizada

Execute como root o script **install.sh**

`chmod +x install.sh`

`./install.sh`

Se tudo ocorrer bem, a aplicação deve estar instalada em **/opt/salic/salic-api/**, pronta para uso, bastando apenas configurar alguns parâmetros

## Instalação Manual

### Dependências básicas

-	`python-dev`
-	`python-pip`
-	`freetds-dev`

### Pacotes python

Basta executar 

`pip install -r requirements.txt`

## Configuração

Copie o arquivo `config_example.py` para `config.py` e o edite de acordo com o seu ambiente.

## Execução

Por padrão a aplicação executa com o web server **Tornado**

O executável é o arquivo  **run.py**

`python run.py`

Caso tenha optado pela instalação automatizada, basta executar

`/etc/init.d/salic-api start`


Ao executar

`/etc/init.d/salic-api`

Você pode conferir os demais comandos

## Teste

Para verificar se a API está de fato executando corretamente, faça uma para a URL

[http://localhost:8000/test](http://localhost:8000/test)

Se tudo estiver correto, você deve obter uma resposta com conteúdo:

`{"content": "API is up and running :D"}`

## License

Copyright (c) 2016 - 2016 LABICOM/LDA UFG

Licensed under the [GPL License](http://www.gnu.org/licenses/gpl.html).