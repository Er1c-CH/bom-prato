from flask import Blueprint, request, jsonify
from sqlalchemy import text
from flask_jwt_extended import jwt_required
from models import db, LoginFuncionario

funcionarios_bp = Blueprint('funcionarios', __name__, url_prefix='/funcionarios')

@funcionarios_bp.route('', methods=['POST'])
@jwt_required()
def create_funcionario():
    data = request.get_json()
    nome = data.get('nome')
    cpf = data.get('cpf')
    cargo = data.get('cargo')
    turno = data.get('turno')
    salario = data.get('salario')
    data_nascimento = data.get('data_nascimento')

    sql_insert_query = text("""
    INSERT INTO funcionario (nome, cpf, cargo, turno, salario, data_nascimento)
    VALUES (:nome, :cpf, :cargo, :turno, :salario, :data_nascimento)
    RETURNING id_funcionario;
    """)
    result = db.session.execute(sql_insert_query, {
        'nome': nome,
        'cpf': cpf,
        'cargo': cargo,
        'turno': turno,
        'salario': salario,
        'data_nascimento': data_nascimento
    })
    db.session.commit()

    id_funcionario = result.fetchone()[0]

    return jsonify({'message': 'Funcionario criado com sucesso!', 'id_funcionario': id_funcionario}), 201

@funcionarios_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_funcionario(id):
    sql_query = text("""
    SELECT id_funcionario, nome, cpf, cargo, turno, salario, data_nascimento
    FROM funcionario
    WHERE id_funcionario = :id;
    """)
    result = db.session.execute(sql_query, {'id': id})
    funcionario = result.mappings().fetchone()

    if funcionario is None:
        return jsonify({'message': 'Funcionario não encontrado'}), 404

    return jsonify({
        'id_funcionario': funcionario['id_funcionario'],
        'nome': funcionario['nome'],
        'cpf': funcionario['cpf'],
        'cargo': funcionario['cargo'],
        'turno': funcionario['turno'],
        'salario': funcionario['salario'],
        'data_nascimento': funcionario['data_nascimento']
    })

@funcionarios_bp.route('', methods=['GET'])
@jwt_required()
def get_funcionarios():
    sql_query = text("""
    SELECT id_funcionario, nome, cpf, cargo, turno, salario, data_nascimento
    FROM funcionario;
    """)
    result = db.session.execute(sql_query)
    funcionarios = result.mappings().fetchall()

    return jsonify([{
        'id_funcionario': funcionario['id_funcionario'],
        'nome': funcionario['nome'],
        'cpf': funcionario['cpf'],
        'cargo': funcionario['cargo'],
        'turno': funcionario['turno'],
        'salario': funcionario['salario'],
        'data_nascimento': funcionario['data_nascimento']
    } for funcionario in funcionarios])

@funcionarios_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_funcionario(id):
    data = request.get_json()
    
    sql_check_query = text("SELECT COUNT(1) FROM funcionario WHERE id_funcionario = :id;")
    result = db.session.execute(sql_check_query, {'id': id})
    if result.fetchone()[0] == 0:
        return jsonify({'message': 'Funcionario não encontrado'}), 404

    sql_query = text("""
    UPDATE funcionario
    SET nome = COALESCE(:nome, nome),
        cpf = COALESCE(:cpf, cpf),
        cargo = COALESCE(:cargo, cargo),
        turno = COALESCE(:turno, turno),
        salario = COALESCE(:salario, salario),
        data_nascimento = COALESCE(:data_nascimento, data_nascimento)
    WHERE id_funcionario = :id;
    """)
    db.session.execute(sql_query, {
        'nome': data.get('nome'),
        'cpf': data.get('cpf'),
        'cargo': data.get('cargo'),
        'turno': data.get('turno'),
        'salario': data.get('salario'),
        'data_nascimento': data.get('data_nascimento'),
        'id': id
    })
    db.session.commit()
    
    return jsonify({'message': 'Funcionario atualizado com sucesso!'})

@funcionarios_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_funcionario(id):
    sql_check_query = text("SELECT COUNT(1) FROM funcionario WHERE id_funcionario = :id;")
    result = db.session.execute(sql_check_query, {'id': id})
    if result.fetchone()[0] == 0:
        return jsonify({'message': 'Funcionario não encontrado'}), 404

    sql_query = text("DELETE FROM funcionario WHERE id_funcionario = :id;")
    db.session.execute(sql_query, {'id': id})
    db.session.commit()

    return jsonify({'message': 'Funcionario deletado com sucesso!'})
