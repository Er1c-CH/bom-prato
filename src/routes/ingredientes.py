from flask import Blueprint, request, jsonify
from sqlalchemy import text
from flask_jwt_extended import jwt_required
from models import db

ingredientes_bp = Blueprint('ingredientes', __name__, url_prefix='/ingredientes')

@ingredientes_bp.route('', methods=['POST'])
@jwt_required()
def create_ingrediente():
    data = request.get_json()
    nome = data.get('nome')
    preco = data.get('preco')
    quantidade = data.get('quantidade', 0)

    if not nome or not preco:
        return jsonify({'message': 'Nome e preço são obrigatórios'}), 400

    sql_insert_query = text("""
    INSERT INTO ingrediente (nome, preco, quantidade)
    VALUES (:nome, :preco, :quantidade)
    RETURNING id_ingrediente;
    """)
    result = db.session.execute(sql_insert_query, {'nome': nome, 'preco': preco, 'quantidade': quantidade})
    db.session.commit()

    id_ingrediente = result.fetchone()[0]

    return jsonify({'message': 'Ingrediente criado com sucesso!', 'id_ingrediente': id_ingrediente}), 201

@ingredientes_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_ingrediente(id):
    sql_query = text("SELECT id_ingrediente, nome, preco, quantidade FROM ingrediente WHERE id_ingrediente = :id;")
    result = db.session.execute(sql_query, {'id': id})
    ingrediente = result.mappings().fetchone()

    if not ingrediente:
        return jsonify({'message': 'Ingrediente não encontrado'}), 404

    return jsonify({
        'id_ingrediente': ingrediente['id_ingrediente'],
        'nome': ingrediente['nome'],
        'preco': str(ingrediente['preco']),
        'quantidade': ingrediente['quantidade']
    })

@ingredientes_bp.route('', methods=['GET'])
@jwt_required()
def get_ingredientes():
    sql_query = text("SELECT id_ingrediente, nome, preco, quantidade FROM ingrediente;")
    result = db.session.execute(sql_query)
    ingredientes = result.mappings().fetchall()

    ingredientes_list = [{
        'id_ingrediente': ingrediente['id_ingrediente'],
        'nome': ingrediente['nome'],
        'preco': str(ingrediente['preco']),
        'quantidade': ingrediente['quantidade']
    } for ingrediente in ingredientes]

    return jsonify(ingredientes_list)

@ingredientes_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_ingrediente(id):
    data = request.get_json()
    nome = data.get('nome')
    preco = data.get('preco')
    quantidade = data.get('quantidade')

    sql_check_query = text("SELECT COUNT(1) FROM ingrediente WHERE id_ingrediente = :id;")
    result = db.session.execute(sql_check_query, {'id': id})
    if result.fetchone()[0] == 0:
        return jsonify({'message': 'Ingrediente não encontrado'}), 404

    sql_update_query = text("""
    UPDATE ingrediente
    SET nome = COALESCE(:nome, nome), preco = COALESCE(:preco, preco), quantidade = COALESCE(:quantidade, quantidade)
    WHERE id_ingrediente = :id;
    """)
    db.session.execute(sql_update_query, {'nome': nome, 'preco': preco, 'quantidade': quantidade, 'id': id})
    db.session.commit()

    return jsonify({'message': 'Ingrediente atualizado com sucesso!'})

@ingredientes_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_ingrediente(id):
    sql_check_query = text("SELECT COUNT(1) FROM ingrediente WHERE id_ingrediente = :id;")
    result = db.session.execute(sql_check_query, {'id': id})
    if result.fetchone()[0] == 0:
        return jsonify({'message': 'Ingrediente não encontrado'}), 404

    sql_delete_query = text("DELETE FROM ingrediente WHERE id_ingrediente = :id;")
    db.session.execute(sql_delete_query, {'id': id})
    db.session.commit()

    return jsonify({'message': 'Ingrediente deletado com sucesso!'})
