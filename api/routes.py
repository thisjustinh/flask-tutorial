from flask import render_template, request
from blockchain.blockchain import Block, Blockchain, import_chain
from api import app
import json
import os.path


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, '../blockchain/blockchains.json')


@app.route('/')
@app.route('/index')
def home():
    return render_template('home.html')


@app.route('/all', methods=['GET', 'POST'])
def display_all():
    if request.method == 'GET':
        if request.args.get('password') != 'admin':
            return 'Error'
    elif request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            return 'Error'
            
    with open(json_path, 'r') as file:
        chains = file.read()
    chains = json.loads(chains)
    chain_list = []

    for key, value in chains.items():
        chain_list.append(import_chain(value))
    return render_template('all.html', chains=chain_list)


@app.route('/chain/<id>')
def display_one(id):
    with open(json_path, 'r') as file:
        chains = file.read()
    chains = json.loads(chains)
    chain = import_chain(chains['chain' + f'{id}'])
    return render_template('blockchain.html', id=id, chain=chain)
