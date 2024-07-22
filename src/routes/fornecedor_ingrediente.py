from flask import Blueprint, request, jsonify
from sqlalchemy import text
from flask_jwt_extended import jwt_required
from models import db

fornecedor_ingrediente_bp = Blueprint('fornecedor_ingrediente', __name__, url_prefix='/fornecedor_ingrediente')

@fornecedor_ingrediente_bp.route('', methods=['POST'])
@jwt_required()
def add_ingrediente_to_fornecedor():
    data = request.get_json()
    id_fornecedor = data.get('id_fornecedor')
    id_ingrediente = data.get('id_ingrediente')
    preco_fornecido = data.get('preco_fornecido')

    if not id_fornecedor or not id_ingrediente or not preco_fornecido:
        return jsonify({'message': 'ID do fornecedor, ID do ingrediente e preço fornecido são obrigatórios'}), 400

    sql_insert_query = text("""
    INSERT INTO fornecedor_ingrediente (id_fornecedor, id_ingrediente, preco_fornecido)
    VALUES (:id_fornecedor, :id_ingrediente, :preco_fornecido)
    ON CONFLICT (id_fornecedor, id_ingrediente) 
    DO UPDATE SET preco_fornecido = EXCLUDED.preco_fornecido;
    """)
    db.session.execute(sql_insert_query, {'id_fornecedor': id_fornecedor, 'id_ingrediente': id_ingrediente, 'preco_fornecido': preco_fornecido})
    db.session.commit()

    return jsonify({'message': 'Ingrediente adicionado/atualizado com sucesso ao fornecedor!'}), 201

@fornecedor_ingrediente_bp.route('/<int:id_fornecedor>', methods=['GET'])
@jwt_required()
def get_ingredientes_by_fornecedor(id_fornecedor):
    sql_query = text("""
    SELECT fi.id_fornecedor, fi.id_ingrediente, i.nome, fi.preco_fornecido
    FROM fornecedor_ingrediente fi
    JOIN ingrediente i ON fi.id_ingrediente = i.id_ingrediente
    WHERE fi.id_fornecedor = :id_fornecedor;
    """)
    result = db.session.execute(sql_query, {'id_fornecedor': id_fornecedor})
    ingredientes = result.mappings().fetchall()

    ingredientes_list = [{
        'id_fornecedor': ingrediente['id_fornecedor'],
        'id_ingrediente': ingrediente['id_ingrediente'],
        'nome': ingrediente['nome'],
        'preco_fornecido': ingrediente['preco_fornecido']
    } for ingrediente in ingredientes]

    return jsonify(ingredientes_list)

@fornecedor_ingrediente_bp.route('/<int:id_fornecedor>/<int:id_ingrediente>', methods=['DELETE'])
@jwt_required()
def delete_ingrediente_from_fornecedor(id_fornecedor, id_ingrediente):
    sql_delete_query = text("DELETE FROM fornecedor_ingrediente WHERE id_fornecedor = :id_fornecedor AND id_ingrediente = :id_ingrediente;")
    db.session.execute(sql_delete_query, {'id_fornecedor': id_fornecedor, 'id_ingrediente': id_ingrediente})
    db.session.commit()

    return jsonify({'message': 'Ingrediente removido do fornecedor com sucesso!'})
