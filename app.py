from flask import Flask, render_template, request, redirect

app = Flask(__name__)

pets = [
    {"id": 1, "name": "Bruno", "type": "Dog", "available": True},
    {"id": 2, "name": "Misty", "type": "Cat", "available": True},
    {"id": 3, "name": "Coco", "type": "Rabbit", "available": False},
]
next_id = 4


@app.route('/')
def home():
    total = len(pets)
    available = sum(1 for p in pets if p["available"])
    adopted = total - available
    return render_template('index.html', total=total, available=available, adopted=adopted)


@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    global next_id
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        pet_type = request.form.get('type', '').strip()
        if name and pet_type:
            pets.append({"id": next_id, "name": name, "type": pet_type, "available": True})
            next_id += 1
        return redirect('/pets')
    return render_template('add_pet.html')


@app.route('/pets')
def view_pets():
    return render_template('view_pets.html', pets=pets)


@app.route('/adopt/<int:pet_id>')
def adopt(pet_id):
    for p in pets:
        if p["id"] == pet_id:
            p["available"] = False
    return redirect('/pets')


@app.route('/release/<int:pet_id>')
def release(pet_id):
    for p in pets:
        if p["id"] == pet_id:
            p["available"] = True
    return redirect('/pets')


@app.route('/delete/<int:pet_id>')
def delete(pet_id):
    global pets
    pets = [p for p in pets if p["id"] != pet_id]
    return redirect('/pets')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
