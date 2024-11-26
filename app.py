from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import api_bp
from config import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.register_blueprint(api_bp)

if __name__ == '__main__':
    db.create_all()  # Cria as tabelas do banco de dados
    app.run(debug=True) #  debug=True apenas para desenvolvimento!