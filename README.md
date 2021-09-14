# Medicar

## Requisitos
- Python 3.8.10
- Docker
- docker-compose

## Configurando a Aplicação

### 1 - Crie um arquivo .env dentro do diretório **desafio-intmed/medicar**
Utilize o arquivo .env.sample como base para configurar o seu .env, copie as 
variáveis de ambiente configuradas no arquivo .env.sample e cole em seu .env

### 2 - Aplique as migrates para que você possa ter acesso ao banco de dados da aplicação
Você deve aplicar as migrates criadas a partir dos models da aplicação, assim você
terá um esquema de banco de dados para utilizar. Em um terminal, dentro do diretório 
**desafio-intmed/medicar** execute o comando a baixo:
~~~Shel
$ python3 manage.py migrate
~~~

### 3 - Crie um usuário administrador para gerenciar sua aplicação
Ainda no mesmo diretório diretório **desafio-intmed/medicar**, execute o comando a baixo e siga as instruções:
~~~Shel
$ python3 manage.py createsuperuser
~~~
~~~Shel
Usuário (leave blank to use 'user'): 
Endereço de email: 
Password: 
Password (again):
~~~

## Rodando a Aplicação

### 1 - Execute os containers docker para rodar a aplicação, perceba que o compose se encontra na pasta **desafio_intmed**, então para executar o compose, altere seu diretório para a pasta **desafio-intmed** e execute o comando a baixo:
~~~Shel
$ docker-compose up 
~~~

~~~Shel
Starting desafio-intmed_web_1 ... done
Attaching to desafio-intmed_web_1
web_1  | Watching for file changes with StatReloader
~~~

### 2 - Abra um navegador e verifique a url da aplicação, teste a porta 8000, certifique-se de que ela não esteja em uso na sua máquina
> localhost:8000

### 3 - Realize o login na página de administração do django, utilize as credenciais que você criou para o seu super usuário
> localhost:8000/admin
