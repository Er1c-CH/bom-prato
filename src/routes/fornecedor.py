from flask import Blueprint, request, jsonify
from sqlalchemy import text
from flask_jwt_extended import jwt_required
from models import db

fornecedor_bp = Blueprint('fornecedor', __name__, url_prefix='/fornecedor')

@fornecedor_bp.route('', methods=['POST'])
@jwt_required()
def create_fornecedor():
    data = request.get_json()
    nome = data.get('nome')
    cnpj = data.get('cnpj')

    if not nome or not cnpj:
        return jsonify({'message': 'Nome e CNPJ são obrigatórios'}), 400

    sql_insert_query = text("""
    INSERT INTO fornecedor (nome, cnpj)
    VALUES (:nome, :cnpj)
    RETURNING id_fornecedor;
    """)
    result = db.session.execute(sql_insert_query, {'nome': nome, 'cnpj': cnpj})
    db.session.commit()

    id_fornecedor = result.fetchone()[0]

    return jsonify({'message': 'Fornecedor criado com sucesso!', 'id_fornecedor': id_fornecedor}), 201

@fornecedor_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_fornecedor(id):
    sql_query = text("""
    SELECT id_fornecedor, nome, cnpj
    FROM fornecedor
    WHERE id_fornecedor = :id;
    """)
    result = db.session.execute(sql_query, {'id': id})
    fornecedor = result.mappings().fetchone()

    if fornecedor:
        return jsonify({
            'id_fornecedor': fornecedor['id_fornecedor'],
            'nome': fornecedor['nome'],
            'cnpj': fornecedor['cnpj']
        })
    else:
        return jsonify({'message': 'Fornecedor não encontrado'}), 404

@fornecedor_bp.route('', methods=['GET'])
@jwt_required()
def get_fornecedores():
    sql_query = text("""
    SELECT id_fornecedor, nome, cnpj
    FROM fornecedor;
    """)
    result = db.session.execute(sql_query)
    fornecedores = result.mappings().fetchall()

    fornecedores_list = [{
        'id_fornecedor': fornecedor['id_fornecedor'],
        'nome': fornecedor['nome'],
        'cnpj': fornecedor['cnpj']
    } for fornecedor in fornecedores]

    return jsonify(fornecedores_list)

@fornecedor_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_fornecedor(id):
    data = request.get_json()
    nome = data.get('nome')
    cnpj = data.get('cnpj')

    sql_check_query = text("SELECT COUNT(1) FROM fornecedor WHERE id_fornecedor = :id;")
    result = db.session.execute(sql_check_query, {'id': id})
    if result.fetchone()[0] == 0:
        return jsonify({'message': 'Fornecedor não encontrado'}), 404

    sql_update_query = text("""
    UPDATE fornecedor
    SET nome = COALESCE(:nome, nome), cnpj = COALESCE(:cnpj, cnpj)
    WHERE id_fornecedor = :id;
    """)
    db.session.execute(sql_update_query, {'nome': nome, 'cnpj': cnpj, 'id': id})
    db.session.commit()

    return jsonify({'message': 'Fornecedor atualizado com sucesso!'})

@fornecedor_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_fornecedor(id):
    sql_check_query = text("SELECT COUNT(1) FROM fornecedor WHERE id_fornecedor = :id;")
    result = db.session.execute(sql_check_query, {'id': id})
    if result.fetchone()[0] == 0:
        return jsonify({'message': 'Fornecedor não encontrado'}), 404

    sql_delete_query = text("DELETE FROM fornecedor WHERE id_fornecedor = :id;")
    db.session.execute(sql_delete_query, {'id': id})
    db.session.commit()

    return jsonify({'message': 'Fornecedor deletado com sucesso!'})
