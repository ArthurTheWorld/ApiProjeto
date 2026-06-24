# ApiProjeto

Projeto pratico com uma API Flask para cadastro e listagem de usuarios, banco de dados MySQL e Nginx atuando como servidor web e proxy reverso.

## Tecnologias utilizadas

- Python
- Flask
- MySQL
- Nginx
- Docker
- Docker Compose

## Estrutura dos containers

- `nginx`: servidor web e proxy reverso.
- `api`: backend Flask responsavel pelos endpoints da aplicacao.
- `mysql`: banco de dados da aplicacao.

Fluxo principal:

```text
Navegador -> Nginx -> API Flask -> MySQL
```

## Portas

- Site: `http://localhost`
- API via proxy reverso: `http://localhost/api`
- MySQL: `localhost:3306`

Internamente, a API Flask roda na porta `5000`, mas o acesso principal deve ser feito pelo Nginx usando o caminho `/api`.

## Como executar

Antes de iniciar, verifique se o Docker Desktop esta aberto e funcionando.

Na pasta do projeto, execute:

```bash
docker compose up --build
```

Depois acesse no navegador:

```text
http://localhost
```

Para testar se a API esta funcionando pelo proxy reverso:

```text
http://localhost/api/health
```

O retorno esperado e:

```json
{
  "status": "ok"
}
```

## Parar os containers

Para parar a aplicacao:

```bash
docker compose down
```

Para parar e remover tambem os dados do banco, use:

```bash
docker compose down -v
```

Use `down -v` apenas quando quiser recriar o banco do zero.

## Endpoints da API

### Verificar status da API

```http
GET /api/health
```

### Listar usuarios

```http
GET /api/users
```

### Cadastrar usuario

```http
POST /api/users
```

Corpo da requisicao:

```json
{
  "name": "João da Silva",
  "email": "joao@email.com"
}
```

## Banco de dados

O banco MySQL e criado automaticamente pelo Docker Compose com o nome:

```text
appdb
```

Credenciais padrao:

```text
Usuario: root
Senha: root
Porta: 3306
```
