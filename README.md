# Notass
Projeto básico para demonstrar um web aplicativo de notas criado com Python.

Demo: https://notass.discloud.app/

## Observações
Não foram adotadas medidas profundas de segurança nem nada do tipo, somente foi adicionado o básico para o projeto funcionar.

## Tecnologias usadas
- Uvicorn: Servidor web.
- FastAPI: Framework web.
- Pydantic: Framwork para estruturação de dados.
- SQLAlchemy: Framework para comunicação com banco de dados.
- bcrypt: Biblioteca para manipular hash de senhas.
- python-jose: Biblioteca para manipular o padrão de dados JWT. 
- Jinja2: Framework para redenrizar páginas html.
- python-decouple: Biblioteca para manipular variáveis de ambiente.

## Executar o projeto
Antes de qualquer opção, tenha o arquvo **.env** configurado seguindo o exemplo do arquivo **.env.exemplo**.

- Docker compose: Na raiz do projeto execute ```docker compose up -d``` ou variantes.

- Direto: Instale ás depêndencias do arquivo **requirements.txt** e execute na raiz do projeto ```python main.py``` ou ```uvicorn main:app```.

## Banco de dados
Para uma experiência mais simples, foi utilizado o banco de dados sqlite. Todos os dados (usuários e notas) do projeto ficam armazenados no arquvio **sqlite.db** na raíz do projeto.