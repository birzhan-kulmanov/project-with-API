from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

characters = requests.get('https://rickandmortyapi.com/api/character').json()


class Characters:
    def __init__(self, character_id, name, status, species, character_type, gender, image, created, origin, location):
        self.character_id = character_id
        self.name = name
        self.status = status
        self.species = species
        self.character_type = character_type
        self.gender = gender
        self.image = image
        self.created = created
        self.origin = origin
        self.location = location


character_objects = []
for i in range(len(characters['results'])):
    character_objects.append(
        Characters(characters["results"][i]["id"],
                   characters["results"][i]["name"],
                   characters["results"][i]["status"],
                   characters["results"][i]["species"],
                   characters["results"][i]["type"],
                   characters["results"][i]["gender"],
                   characters["results"][i]["image"],
                   characters["results"][i]["created"],
                   characters["results"][i]["origin"]["name"],
                   characters["results"][i]["location"]["name"]))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', character_objects=character_objects)


@app.route('/character/<string:name>')
def character_detail(name):
    character = None
    for i in range(len(character_objects)):
        if character_objects[i].name == name:
            character = character_objects[i]
            break
    return render_template('character_detail.html', character=character)


@app.route('/edit-character/<string:name>', methods=['GET', 'POST'])
def edit(name):
    for i in range(len(character_objects)):
        if character_objects[i].name == name:
            character = character_objects[i]
            break
    if request.method == "POST":
        character.name = request.form['name']
        character.origin = request.form['origin']
        character.location = request.form['location']
        return redirect('/')
    else:
        return render_template('edit-character.html', character=character)


if __name__ == '__main__':
    app.run(debug=True)
