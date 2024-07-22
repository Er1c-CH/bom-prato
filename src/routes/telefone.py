from flask import Blueprint, request, jsonify
from sqlalchemy import text
from flask_jwt_extended import jwt_required
from models import db

telefone_bp = Blueprint('telefone', __name__, url_prefix='/telefone')

@telefone_bp.route('', methods=['POST'])
@jwt_required()
def create_telefone():
    data = request.get_json()
    id_fornecedor = data.get('id_fornecedor')
    numero = data.get('numero')

    if not id_fornecedor or not numero:
        return jsonify({'message': 'ID do fornecedor e número são obrigatórios'}), 400

    sql_insert_query = text("""
    INSERT INTO telefone (id_fornecedor, numero)
    VALUES (:id_fornecedor, :numero);
    """)
    db.session.execute(sql_insert_query, {'id_fornecedor': id_fornecedor, 'numero': numero})
    db.session.commit()

    return jsonify({'message': 'Telefone criado com sucesso!'}), 201

@telefone_bp.route('/<int:id_fornecedor>', methods=['GET'])
@jwt_required()
def get_telefones_by_fornecedor(id_fornecedor):
    sql_query = text("""
    SELECT id_fornecedor, numero
    FROM telefone
    WHERE id_fornecedor = :id_fornecedor;
    """)
    result = db.session.execute(sql_query, {'id_fornecedor': id_fornecedor})
    telefones = result.mappings().fetchall()

    telefones_list = [{
        'id_fornecedor': telefone['id_fornecedor'],
        'numero': telefone['numero']
    } for telefone in telefones]

    return jsonify(telefones_list)

@telefone_bp.route('/<int:id_fornecedor>/<string:numero>', methods=['DELETE'])
@jwt_required()
def delete_telefone(id_fornecedor, numero):
    sql_delete_query = text("DELETE FROM telefone WHERE id_fornecedor = :id_fornecedor AND numero = :numero;")
    db.session.execute(sql_delete_query, {'id_fornecedor': id_fornecedor, 'numero': numero})
    db.session.commit()

    return jsonify({'message': 'Telefone deletado com sucesso!'})
