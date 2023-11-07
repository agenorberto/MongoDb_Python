from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client.veiculo
collection_carros = db.carros

@app.route("/")
def index():
    return render_template ("index.html")

@app.route("/lista")
def listar():
    retorno_carros = list (collection_carros.find())
    return render_template("listar.html", carros = retorno_carros)


@app.route("/cadastra")
def insere_veiculo():
    return render_template("cadastrar.html")

@app.route ("/cadastrar_bd", methods=['POST'])
def cadastra_veiculo():
    carro = {
        'marca':request.form['marca'],
        'modelo':request.form['modelo'],
        'ano':request.form['ano'],
        'preco':request.form['preco'],
        'categoria':request.form['categoria'],
        'placa' :request.form['placa']
    }
    collection_carros.insert_one(carro)
    return redirect("/lista")


@app.route("/<idCarros>/editar")
def editar_veiculo(idCarros):
    carro = collection_carros.find_one({"_id": ObjectId(idCarros)})
    return render_template("/atualiza.html", carros = carro)

@app.route("/atualiza_bd", methods=["POST"])
def atualiza_veiculo():
    idCarros = request.form['id']
    carro = {
        'marca': request.form['marca'],
        'modelo': request.form['modelo'],
        'ano': request.form['ano'],
        'preco': request.form['preco'],
        'categoria': request.form['categoria'],
        'placa' :request.form['placa']
    }
    collection_carros.update_one({'_id': ObjectId(idCarros)}, {'$set': carro})

    return redirect("/lista")

@app.route("/<idCarros>/excluir")
def excluir_veiculo(idCarros):
    collection_carros.delete_one({"_id": ObjectId(idCarros)})

    retorno_carros = list(collection_carros.find())
    return redirect("/lista")

if __name__ == '__main__':
    app.run(debug=True)
