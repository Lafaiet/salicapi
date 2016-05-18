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