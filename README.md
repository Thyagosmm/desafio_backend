# API de Gestão Escolar

Uma API RESTful para gerenciamento de alunos, cursos e matrículas usando Flask e MySQL.

## 🚀 Funcionalidades
- Cadastro de alunos e cursos
- Matrícula de alunos em cursos
- Consulta de relacionamentos N:M
- CRUD completo para todas as entidades

## ⚙️ Configuração

### Pré-requisitos
- Python 3.9+
- Conta no [FreeDB.tech](https://freedb.tech)

### Instalação
1. Clonar repositório:

git clone https://github.com/seu-usuario/projeto-flask.git
cd projeto-flask

2. Abrir o terminal powershell e executar:

Criar ambiente virtual:

python -m venv venv

Ativar ambiente virtual:

venv\Scripts\activate

Instalar dependencias:

pip install -r requirements.txt

Rodar aplicação:

python app.py

3. Execução de testes e visualizar no banco online:

No terminal irá aparecer isso:

Running on http://localhost:5000

Você irá no postman e criará um aluno:

(POST) http://localhost:5000/alunos/novoaluno

{
    "nome": "Alberto Campos",
    "email": "alberto@escola.com"
}

O retorno será esse:

{
    "id": 1,
    "message": "Aluno criado com sucesso!"
}

entre agora no banco online e visualize o novo usuario criado:

https://phpmyadmin.freedb.tech

servidor: sql.freedb.tech
usuario: freedb_hostname
senha: 4%j?8z$cH&ubVJA
