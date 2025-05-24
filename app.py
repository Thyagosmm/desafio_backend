import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar Flask e SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # Esta linha estava faltando!

# Modelos
class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    matriculas = db.relationship('Matricula', backref='aluno', passive_deletes=True)

class Curso(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    matriculas = db.relationship('Matricula', backref='curso', passive_deletes=True)

class Matricula(db.Model):
    __tablename__ = 'matriculas'
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id', ondelete='CASCADE'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id', ondelete='CASCADE'), nullable=False)

# Rotas para Alunos
@app.route('/alunos/novoaluno', methods=['POST'])
def criar_aluno():
    data = request.get_json()
    try:
        aluno = Aluno(nome=data['nome'], email=data['email'])
        db.session.add(aluno)
        db.session.commit()
        return jsonify({'message': 'Aluno criado com sucesso!', 'id': aluno.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Email já cadastrado'}), 400
    except Exception as e:
        return jsonify({'message': 'Erro ao criar aluno', 'error': str(e)}), 400

@app.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = Aluno.query.all()
    return jsonify([{'id': a.id, 'nome': a.nome, 'email': a.email} for a in alunos])

@app.route('/alunos/<int:id>', methods=['GET'])
def obter_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    cursos = [{'curso_id': m.curso_id, 'titulo': m.curso.titulo} for m in aluno.matriculas]
    return jsonify({**aluno.__dict__, 'cursos': cursos})

@app.route('/alunos/atualizaaluno', methods=['PUT'])
def atualizar_aluno():
    data = request.get_json()
    aluno = Aluno.query.get_or_404(data['id'])
    try:
        if 'nome' in data: aluno.nome = data['nome']
        if 'email' in data: aluno.email = data['email']
        db.session.commit()
        return jsonify({'message': 'Aluno atualizado com sucesso!'})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Novo email já está em uso'}), 400

@app.route('/alunos/removealuno/<int:id>', methods=['DELETE'])
def remover_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    return jsonify({'message': 'Aluno removido com sucesso!'})

# Rotas para Cursos
@app.route('/cursos/novocurso', methods=['POST'])
def criar_curso():
    data = request.get_json()
    try:
        curso = Curso(titulo=data['titulo'], descricao=data.get('descricao', ''))
        db.session.add(curso)
        db.session.commit()
        return jsonify({'message': 'Curso criado com sucesso!', 'id': curso.id}), 201
    except Exception as e:
        return jsonify({'message': 'Erro ao criar curso', 'error': str(e)}), 400

@app.route('/cursos', methods=['GET'])
def listar_cursos():
    cursos = Curso.query.all()
    return jsonify([{'id': c.id, 'titulo': c.titulo, 'descricao': c.descricao} for c in cursos])

@app.route('/cursos/<int:id>', methods=['GET'])
def obter_curso(id):
    curso = Curso.query.get_or_404(id)
    alunos = [{'aluno_id': m.aluno_id, 'nome': m.aluno.nome} for m in curso.matriculas]
    return jsonify({**curso.__dict__, 'alunos': alunos})

@app.route('/cursos/atualizacurso', methods=['PUT'])
def atualizar_curso():
    data = request.get_json()
    curso = Curso.query.get_or_404(data['id'])
    if 'titulo' in data: curso.titulo = data['titulo']
    if 'descricao' in data: curso.descricao = data['descricao']
    db.session.commit()
    return jsonify({'message': 'Curso atualizado com sucesso!'})

@app.route('/cursos/removecurso/<int:id>', methods=['DELETE'])
def remover_curso(id):
    curso = Curso.query.get_or_404(id)
    db.session.delete(curso)
    db.session.commit()
    return jsonify({'message': 'Curso removido com sucesso!'})

# Rotas para Matrículas
@app.route('/matriculas', methods=['POST'])
def criar_matricula():
    data = request.get_json()
    if Matricula.query.filter_by(aluno_id=data['aluno_id'], curso_id=data['curso_id']).first():
        return jsonify({'message': 'Matrícula já existe'}), 400
        
    aluno = Aluno.query.get_or_404(data['aluno_id'])
    curso = Curso.query.get_or_404(data['curso_id'])
    
    matricula = Matricula(aluno_id=aluno.id, curso_id=curso.id)
    db.session.add(matricula)
    db.session.commit()
    return jsonify({'message': 'Matrícula criada com sucesso!'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)