from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

POKEAPI ="https://pokeapi.co/api/v2/pokemon/"
app = Flask(__name__)
app.secret_key = 'llavesitasecreta:3'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def buscar_pokemonsito():
    pokemonsito = request.form.get('pokemonsito', '').strip().lower()
    if not pokemonsito:
        flash('Por favor ingresa un nombre de Pokémon.', 'error')
        return redirect(url_for('index'))
    
    response = requests.get(f"{POKEAPI}{pokemonsito}")

    if response.status_code == 200:
        pokemon_data = response.json()
        return render_template('pokemon.html', pokemon=pokemon_data)

if __name__ == '__main__':
    app.run(debug=True)