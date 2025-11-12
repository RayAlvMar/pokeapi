from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests

app = Flask(__name__)
app.secret_key = 'llavesitasecreta:3'
POKEAPI = "https://pokeapi.co/api/v2/pokemon/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def buscar_pokemonsito():
    pokemonsito = request.form.get('pokemonsito', '').strip().lower()
    if not pokemonsito:
        flash('Por favor ingresa un nombre de Pokémon.', 'error')
        return redirect(url_for('index'))

    try:
        resp = requests.get(f"{POKEAPI}{pokemonsito}")
        if resp.status_code == 200:
            pokemon_data = resp.json()
            pokemon_info = {
                'name': pokemon_data['name'].title(),
                'id': pokemon_data['id'],
                'height': pokemon_data['height'] / 10,
                'weight': pokemon_data['weight'] / 10,
                'types': [t['type']['name'] for t in pokemon_data['types']],
                'image': pokemon_data['sprites']['front_default'],
                'abilities': [a['ability']['name'].title() for a in pokemon_data['abilities']]
            }
            return render_template('pokemon.html', pokemon=pokemon_info)
        else:
            flash(f'Pokémon "{pokemonsito}" no encontrado.', 'error')
            return redirect(url_for('index'))
    except requests.exceptions.RequestException:
        flash('Error al conectar con la API de Pokémon.', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)