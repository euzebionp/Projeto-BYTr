from flask import Blueprint, request, jsonify
from models import Empresa, Avaliador, Avaliacao, db # Certifique-se que 'db' está importado corretamente
from schemas import AvaliacaoSchema, EmpresaSchema # Adicione EmpresaSchema
from utils import geocode_address
from config import config
import googlemaps
from pydantic import ValidationError, BaseModel #Para erros mais específicos
from sqlalchemy.exc import IntegrityError


api_bp = Blueprint('api', __name__, url_prefix='/api')
gmaps = googlemaps.Client(key=config.GOOGLE_MAPS_API_KEY)


@api_bp.route('/empresas', methods=['POST'])
def criar_empresa():
    schema = EmpresaSchema() # Usando o esquema EmpresaSchema
    data = request.get_json()
    try:
        validated_data = schema.parse_obj(data)
        latitude, longitude = geocode_address(validated_data.endereco)
        if latitude is None or longitude is None:
            return jsonify({"error": "Endereço não encontrado"}), 400

        empresa = Empresa(nome=validated_data.nome, endereco=validated_data.endereco, latitude=latitude, longitude=longitude)
        db.session.add(empresa)
        db.session.commit()
        return jsonify({"message": "Empresa criada com sucesso", "id": empresa.id}), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 422
    except IntegrityError as e:
        return jsonify({"error": "Empresa já existe"}), 409
    except Exception as e:
        db.session.rollback() # Importante para rollback em caso de erro
        return jsonify({"error": str(e)}), 500


@api_bp.route('/empresas/<int:empresa_id>', methods=['GET'])
def get_empresa(empresa_id):
    empresa = Empresa.query.get(empresa_id)
    if empresa:
        return jsonify(empresa.to_dict()) # Assumindo que Empresa tem um método to_dict()
    return jsonify({"error": "Empresa não encontrada"}), 404


@api_bp.route('/avaliacoes', methods=['POST'])
def criar_avaliacao():
    schema = AvaliacaoSchema()
    data = request.get_json()
    try:
        validated_data = schema.parse_obj(data)
        avaliacao = Avaliacao(**validated_data.dict())
        db.session.add(avaliacao)
        db.session.commit()
        return jsonify({"message": "Avaliação criada com sucesso"}), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 422
    except IntegrityError as e:
        return jsonify({"error": "Erro de integridade do banco de dados"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



@api_bp.route('/avaliacoes/search', methods=['GET'])
def search_avaliacoes():
    empresa_id = request.args.get('empresa_id')
    # Adicione mais parâmetros de pesquisa conforme necessário (ex: data, avaliador_id)

    query = Avaliacao.query
    if empresa_id:
        query = query.filter_by(empresa_id=empresa_id)

    avaliacoes = query.all()
    return jsonify([avaliacao.to_dict() for avaliacao in avaliacoes]) # Assumindo que Avaliacao tem um método to_dict()