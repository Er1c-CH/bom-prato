from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, LoginFuncionario
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    senha = data.get('senha')

    login = LoginFuncionario.query.filter_by(username=username).first()
    if login and check_password_hash(login.senha, senha):
        access_token = create_access_token(identity=username)
        login.ultimo_login = db.func.now()
        db.session.commit()
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Credenciais inválidas'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    id_funcionario = data.get('id_funcionario')
    username = data.get('username')
    senha = data.get('senha')

    if LoginFuncionario.query.filter_by(username=username).first():
        return jsonify({'message': 'Username já existe'}), 409

    senha_hash = generate_password_hash(senha)

    novo_login = LoginFuncionario(id_funcionario=id_funcionario, username=username, senha=senha_hash)
    db.session.add(novo_login)
    db.session.commit()

    return jsonify({'message': 'Registro realizado com sucesso!'}), 201
