from flask import Flask, request
import re

app = Flask('my-todos-app')


@app.route('/todo', methods=['POST'])
def add_item():
    d = request.data.decode().split(" ", 1)
    identifier = d[0]
    description = d[1]
    if re.search(r"^[a-zA-Z0-9_]+$", identifier) and ('\n' not in description) and ('\r' not in description):
        with open('todos.txt', 'a') as f:
            f.write(identifier)
            f.write(" False ")
            f.write(description)
            f.write("\n")  # TODO korektni pridani nove radky
        return '', 201
    else:
        return 'Nevalidni vstup', 400 # TODO popsat detailneji?


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
                identifier = line.strip("\n").split(" ", 2)[0]
                if identifier != item:
                    f.write(line)
                else:
                    todo_exists = True
        if todo_exists:
            return '', 204
        else:
            return 'Úkol není na seznamu', 404
    except IOError:
        return 'Seznam úkolů neexistuje, přidej první úkol', 404


@app.route('/<item>/set-done', methods=['PUT'])
def set_done(item):
    try:
        with open("todos.txt", "r") as f:
            lines = f.readlines()

        with open("todos.txt", "w") as f:
            todo_exists = False
            for line in lines:
                spl = line.split(" ", 2)
                identifier = spl[0]
                description = spl[2]
                if identifier == item:
                    todo_exists = True
                    newline = identifier + " True " + description
                    f.write(newline)
                else:
                    f.write(line)

        if todo_exists:
            return '', 204
        else:
            return 'Úkol není na seznamu', 404

    except IOError:
        return 'Seznam úkolů neexistuje, přidej první úkol', 404


@app.route('/<item>/set-not-done', methods=['PUT'])
def set_not_done(item):
    try:
        with open("todos.txt", "r") as f:
            lines = f.readlines()

        with open("todos.txt", "w") as f:
            todo_exists = False
            for line in lines:
                spl = line.split(" ", 2)
                identifier = spl[0]
                description = spl[2]
                if identifier == item:
                    todo_exists = True
                    newline = identifier + " False " + description
                    f.write(newline)
                else:
                    f.write(line)

        if todo_exists:
            return '', 204
        else:
            return 'Úkol není na seznamu', 404

    except IOError:
        return 'Seznam úkolů neexistuje, přidej první úkol', 404


if __name__ == '__main__':
    app.run(debug=True)