from flask import Blueprint, request, jsonify
from sqlalchemy import text
from flask_jwt_extended import jwt_required
from models import db

prato_ingredientes_bp = Blueprint('prato_ingredientes', __name__, url_prefix='/prato_ingredientes')

@prato_ingredientes_bp.route('', methods=['POST'])
@jwt_required()
def add_ingredientes_to_prato():
    data = request.get_json()
    id_prato = data.get('id_prato')
    ingredientes = data.get('ingredientes')  # Lista de dicionários com nome e quantidade

    if not id_prato or not ingredientes:
        return jsonify({'message': 'ID do prato e ingredientes são obrigatórios'}), 400

    for ingrediente in ingredientes:
        nome = ingrediente.get('nome')
        quantidade = ingrediente.get('quantidade')

        if not nome or not quantidade:
            return jsonify({'message': 'Nome e quantidade dos ingredientes são obrigatórios'}), 400

        sql_select_query = text("SELECT id_ingrediente FROM ingrediente WHERE nome = :nome;")
        result = db.session.execute(sql_select_query, {'nome': nome})
        ingrediente_id = result.fetchone()

        if not ingrediente_id:
            return jsonify({'message': f'Ingrediente {nome} não encontrado'}), 404

        id_ingrediente = ingrediente_id[0]

        sql_insert_query = text("""
        INSERT INTO prato_ingrediente (id_prato, id_ingrediente, quantidade_utilizada)
        VALUES (:id_prato, :id_ingrediente, :quantidade_utilizada)
        ON CONFLICT (id_prato, id_ingrediente) 
        DO UPDATE SET quantidade_utilizada = EXCLUDED.quantidade_utilizada;
        """)
        db.session.execute(sql_insert_query, {'id_prato': id_prato, 'id_ingrediente': id_ingrediente, 'quantidade_utilizada': quantidade})
    
    db.session.commit()

    return jsonify({'message': 'Ingredientes adicionados/atualizados com sucesso!'}), 201

@prato_ingredientes_bp.route('/<int:id_prato>', methods=['GET'])
@jwt_required()
def get_ingredientes_by_prato(id_prato):
    sql_query = text("""
    SELECT pi.id_prato, i.nome, pi.quantidade_utilizada
    FROM prato_ingrediente pi
    JOIN ingrediente i ON pi.id_ingrediente = i.id_ingrediente
    WHERE pi.id_prato = :id_prato;
    """)
    result = db.session.execute(sql_query, {'id_prato': id_prato})
    ingredientes = result.mappings().fetchall()

    ingredientes_list = [{
        'id_prato': ingrediente['id_prato'],
        'nome': ingrediente['nome'],
        'quantidade_utilizada': ingrediente['quantidade_utilizada']
    } for ingrediente in ingredientes]

    return jsonify(ingredientes_list)

@prato_ingredientes_bp.route('/<int:id_prato>/<string:nome_ingrediente>', methods=['DELETE'])
@jwt_required()
def delete_ingrediente_from_prato(id_prato, nome_ingrediente):
    sql_select_query = text("SELECT id_ingrediente FROM ingrediente WHERE nome = :nome;")
    result = db.session.execute(sql_select_query, {'nome': nome_ingrediente})
    ingrediente_id = result.fetchone()

    if not ingrediente_id:
        return jsonify({'message': f'Ingrediente {nome_ingrediente} não encontrado'}), 404

    id_ingrediente = ingrediente_id[0]

    sql_delete_query = text("DELETE FROM prato_ingrediente WHERE id_prato = :id_prato AND id_ingrediente = :id_ingrediente;")
    db.session.execute(sql_delete_query, {'id_prato': id_prato, 'id_ingrediente': id_ingrediente})
    db.session.commit()

    return jsonify({'message': 'Ingrediente removido do prato com sucesso!'})

@prato_ingredientes_bp.route('/<int:id_prato>', methods=['PUT'])
@jwt_required()
def update_ingredientes_of_prato(id_prato):
    data = request.get_json()
    ingredientes = data.get('ingredientes')

    if not ingredientes:
        return jsonify({'message': 'Ingredientes são obrigatórios'}), 400

    for ingrediente in ingredientes:
        nome = ingrediente.get('nome')
        quantidade = ingrediente.get('quantidade')

        if not nome or not quantidade:
            return jsonify({'message': 'Nome e quantidade dos ingredientes são obrigatórios'}), 400

        sql_select_query = text("SELECT id_ingrediente FROM ingrediente WHERE nome = :nome;")
        result = db.session.execute(sql_select_query, {'nome': nome})
        ingrediente_id = result.fetchone()

        if not ingrediente_id:
            return jsonify({'message': f'Ingrediente {nome} não encontrado'}), 404

        id_ingrediente = ingrediente_id[0]

        sql_update_query = text("""
        INSERT INTO prato_ingrediente (id_prato, id_ingrediente, quantidade_utilizada)
        VALUES (:id_prato, :id_ingrediente, :quantidade_utilizada)
        ON CONFLICT (id_prato, id_ingrediente) 
        DO UPDATE SET quantidade_utilizada = EXCLUDED.quantidade_utilizada;
        """)
        db.session.execute(sql_update_query, {'id_prato': id_prato, 'id_ingrediente': id_ingrediente, 'quantidade_utilizada': quantidade})
    
    db.session.commit()

    return jsonify({'message': 'Ingredientes atualizados com sucesso!'}), 200
