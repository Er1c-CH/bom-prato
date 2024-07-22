from flask import Blueprint, request, jsonify
from sqlalchemy import text
from flask_jwt_extended import jwt_required
from datetime import date, timedelta
from models import db

clientes_bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@clientes_bp.route('/com_cartao', methods=['POST'])
@jwt_required()
def create_cliente_com_cartao():
    data = request.get_json()
    nome = data.get('nome')
    cpf = data.get('cpf')

    data_emissao = date.today()
    validade = data_emissao + timedelta(days=365)
    
    sql_cartao_query = text("""
    INSERT INTO cartao_dependencia (validade, pontos, data_emissao)
    VALUES (:validade, :pontos, :data_emissao)
    RETURNING id_cartao;
    """)
    result_cartao = db.session.execute(sql_cartao_query, {
        'validade': validade,
        'pontos': 0,
        'data_emissao': data_emissao
    })
    db.session.commit()
    
    id_cartao = result_cartao.fetchone()[0]

    sql_cliente_query = text("""
    INSERT INTO cliente (nome, cpf, id_cartao)
    VALUES (:nome, :cpf, :id_cartao)
    RETURNING id_cliente;
    """)
    result_cliente = db.session.execute(sql_cliente_query, {'nome': nome, 'cpf': cpf, 'id_cartao': id_cartao})
    db.session.commit()

    id_cliente = result_cliente.fetchone()[0]

    return jsonify({'message': 'Cliente criado com sucesso!', 'id_cliente': id_cliente, 'id_cartao': id_cartao}), 201

@clientes_bp.route('/sem_cartao', methods=['POST'])
@jwt_required()
def create_cliente_sem_cartao():
    data = request.get_json()
    nome = data.get('nome')
    cpf = data.get('cpf')

    sql_query = text("""
    INSERT INTO cliente (nome, cpf)
    VALUES (:nome, :cpf)
    RETURNING id_cliente;
    """)
    result = db.session.execute(sql_query, {'nome': nome, 'cpf': cpf})
    db.session.commit()

    id_cliente = result.fetchone()[0]

    return jsonify({'message': 'Cliente criado com sucesso!', 'id_cliente': id_cliente}), 201

@clientes_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_cliente(id):
    sql_query = text("""
    SELECT id_cliente, nome, cpf, id_cartao
    FROM cliente
    WHERE id_cliente = :id;
    """)
    result = db.session.execute(sql_query, {'id': id})
    cliente = result.mappings().fetchone()

    if cliente:
        return jsonify({
            'id_cliente': cliente['id_cliente'],
            'nome': cliente['nome'],
            'cpf': cliente['cpf'],
            'id_cartao': cliente['id_cartao']
        })
    else:
        return jsonify({'message': 'Cliente não encontrado'}), 404

@clientes_bp.route('', methods=['GET'])
@jwt_required()
def get_clientes():
    sql_query = text("""
    SELECT id_cliente, nome, cpf, id_cartao
    FROM cliente;
    """)
    result = db.session.execute(sql_query)
    clientes = result.mappings().fetchall()

    clientes_list = [{
        'id_cliente': cliente['id_cliente'],
        'nome': cliente['nome'],
        'cpf': cliente['cpf'],
        'id_cartao': cliente['id_cartao']
    } for cliente in clientes]

    return jsonify(clientes_list)

@clientes_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_cliente(id):
    data = request.get_json()
    nome = data.get('nome')
    cpf = data.get('cpf')
    id_cartao = data.get('id_cartao', None)

    sql_check_query = text("SELECT COUNT(1) FROM cliente WHERE id_cliente = :id;")
    result = db.session.execute(sql_check_query, {'id': id})
    if result.fetchone()[0] == 0:
        return jsonify({'message': 'Cliente não encontrado'}), 404

    sql_update_query = text("""
    UPDATE cliente
    SET nome = COALESCE(:nome, nome), cpf = COALESCE(:cpf, cpf), id_cartao = COALESCE(:id_cartao, id_cartao)
    WHERE id_cliente = :id;
    """)
    db.session.execute(sql_update_query, {'nome': nome, 'cpf': cpf, 'id_cartao': id_cartao, 'id': id})
    db.session.commit()

    return jsonify({'message': 'Cliente atualizado com sucesso!'})

@clientes_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_cliente(id):
    sql_check_query = text("SELECT COUNT(1) FROM cliente WHERE id_cliente = :id;")
    result = db.session.execute(sql_check_query, {'id': id})
    if result.fetchone()[0] == 0:
        return jsonify({'message': 'Cliente não encontrado'}), 404

    sql_delete_query = text("DELETE FROM cliente WHERE id_cliente = :id;")
    db.session.execute(sql_delete_query, {'id': id})
    db.session.commit()

    return jsonify({'message': 'Cliente deletado com sucesso!'})
