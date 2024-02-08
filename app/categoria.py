from flask import Flask,request,jsonify
from gevent.pywsgi import WSGIServer
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Obtener los valores de conexión desde variables de entorno
db_user = os.environ.get('DB_USER', 'user')
db_password = os.environ.get('DB_PASSWORD', 'passwd')
db_host = os.environ.get('DB_HOST', '127.0.0.1')
db_port = os.environ.get('DB_PORT', '3306')
db_name = os.environ.get('DB_NAME', 'db')




app = Flask(__name__)
db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


class Categoria(db.Model):
    cat_id = db.Column(db.Integer,primary_key=True)
    cat_nom = db.Column(db.String(100))
    cat_desp = db.Column(db.String(100))

    def __init__(self,cat_nom,cat_desp):
        self.cat_nom = cat_nom
        self.cat_desp = cat_desp


with app.app_context():
    db.create_all()



#Schema categoria 

class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id','cat_nom','cat_desp')


## una categoria
categoria_schema = CategoriaSchema()
###muchas respuestas
categorias_schema = CategoriaSchema(many=True)



##### Metodo Get 
@app.route('/categoria',methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)


#### get categoria por id
@app.route('/categoria/<id>',methods=['GET'])
def get_categoria_x_id(id):
    una_categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(una_categoria)


#### Método POST 
@app.route('/categoria',methods=['POST'])
def insert_categoria():
    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']

    nuevaCategoria = Categoria(cat_nom, cat_desp)

    db.session.add(nuevaCategoria)
    db.session.commit()
    return categoria_schema.jsonify(nuevaCategoria)


#### Method update
@app.route('/categoria/<id>',methods=['PUT'])
def update_categoria(id):
    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']

    actualizarCategoria = Categoria.query.get(id)

    actualizarCategoria.cat_nom = cat_nom
    actualizarCategoria.cat_desp = cat_desp

    db.session.commit()


    return categoria_schema.jsonify(actualizarCategoria)



#### DELETE 

@app.route('/categoria/<id>',methods=['DELETE'])
def delete_categoria(id):
    eliminarCategoria = Categoria.query.get(id)
    db.session.delete(eliminarCategoria)
    db.session.commit()
    return categoria_schema.jsonify(eliminarCategoria)

@app.route('/',methods=['GET'])
def index():
    return jsonify({'Mensaje': 'Bienvenido'})


@app.route('/hello')
def hello():
    return 'Hello, World'


if __name__=="__main__":
    #app.run(debug=True)
    http_server = WSGIServer(("0.0.0.0", 8090), app)
    http_server.serve_forever()
