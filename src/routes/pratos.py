from flask import Blueprint, request, jsonify
from sqlalchemy import text
from flask_jwt_extended import jwt_required
from models import db

pratos_bp = Blueprint('pratos', __name__, url_prefix='/pratos')

@pratos_bp.route('', methods=['POST'])
@jwt_required()
def create_prato():
    data = request.get_json()
    nome = data.get('nome')
    preco = data.get('preco')

    if not nome or not preco:
        return jsonify({'message': 'Nome e preço são obrigatórios'}), 400

    sql_insert_query = text("""
    INSERT INTO prato (nome, preco)
    VALUES (:nome, :preco)
    RETURNING id_prato;
    """)
    result = db.session.execute(sql_insert_query, {'nome': nome, 'preco': preco})
    db.session.commit()

    id_prato = result.fetchone()[0]

    return jsonify({'message': 'Prato criado com sucesso!', 'id_prato': id_prato}), 201

@pratos_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_prato(id):
    sql_query = text("SELECT id_prato, nome, preco FROM prato WHERE id_prato = :id;")
    result = db.session.execute(sql_query, {'id': id})
    prato = result.mappings().fetchone()

    if not prato:
        return jsonify({'message': 'Prato não encontrado'}), 404

    return jsonify({
        'id_prato': prato['id_prato'],
        'nome': prato['nome'],
        'preco': str(prato['preco'])
    })

@pratos_bp.route('', methods=['GET'])
@jwt_required()
def get_pratos():
    sql_query = text("SELECT id_prato, nome, preco FROM prato;")
    result = db.session.execute(sql_query)
    pratos = result.mappings().fetchall()

    pratos_list = [{
        'id_prato': prato['id_prato'],
        'nome': prato['nome'],
        'preco': str(prato['preco'])
    } for prato in pratos]

    return jsonify(pratos_list)

@pratos_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_prato(id):
    data = request.get_json()
    nome = data.get('nome')
    preco = data.get('preco')

    sql_check_query = text("SELECT COUNT(1) FROM prato WHERE id_prato = :id;")
    result = db.session.execute(sql_check_query, {'id': id})
    if result.fetchone()[0] == 0:
        return jsonify({'message': 'Prato não encontrado'}), 404

    sql_update_query = text("""
    UPDATE prato
    SET nome = COALESCE(:nome, nome), preco = COALESCE(:preco, preco)
    WHERE id_prato = :id;
    """)
    db.session.execute(sql_update_query, {'nome': nome, 'preco': preco, 'id': id})
    db.session.commit()

    return jsonify({'message': 'Prato atualizado com sucesso!'})

@pratos_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_prato(id):
    sql_check_query = text("SELECT COUNT(1) FROM prato WHERE id_prato = :id;")
    result = db.session.execute(sql_check_query, {'id': id})
    if result.fetchone()[0] == 0:
        return jsonify({'message': 'Prato não encontrado'}), 404

    sql_delete_query = text("DELETE FROM prato WHERE id_prato = :id;")
    db.session.execute(sql_delete_query, {'id': id})
    db.session.commit()

    return jsonify({'message': 'Prato deletado com sucesso!'})
