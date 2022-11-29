from flask import Flask, request
import re

app = Flask('my-todos-app')


@app.route('/todo', methods=['POST'])
def add_item():
    d = request.data.decode()
    if re.search(r"^[a-zA-Z0-9_]+$", d):
        with open('todos.txt', 'a') as f:
            f.write(d)
            f.write("\n")  # TODO korektni pridani nove radky
        return '', 201
    else:
        return 'Nevalidni vstup', 400


@app.route('/todos')
def get_all():
    try:
        with open("todos.txt") as f:
            result = f.read()
        return result
    except IOError:
        return "Seznam úkolů neexistuje, přidej první úkol", 404


@app.route('/todo/<item>', methods=['DELETE'])
def delete_item(item):
    try:
        with open("todos.txt", "r") as f:
            lines = f.readlines()
        with open("todos.txt", "w") as f:
            todo_exists = False
            for line in lines:
                if line.strip("\n") != item:
                    f.write(line)
                else:
                    todo_exists = True
        if todo_exists:
            return '', 204
        else:
            return 'Úkol není na seznamu', 404
    except IOError:
        return 'Seznam úkolů neexistuje, přidej první úkol', 404


if __name__ == '__main__':
    app.run(debug=True)