from flask import Flask, request
import re
from datetime import date

app = Flask('my-todos-app')


@app.route('/todo', methods=['POST'])
def add_item():
    d = request.data.decode().split(" ", 2)
    identifier = d[0]
    deadline = d[1]
    description = d[2]

    if re.search(r"^[a-zA-Z0-9_]+$", identifier) \
            and re.search(r"^([0-9]{4}-[0-9]{2}-[0-9]{2})$", deadline) \
            and ('\n' not in description) \
            and ('\r' not in description):
        with open('todos.txt', 'a') as f:  # TODO korektni pridani nove radky
            f.write(identifier + " False " + deadline + " " + description + "\n")
        return '', 201
    else:
        return 'Nevalidni vstup', 400  # TODO neměly by být generické responses ve vlastní metodě/objektu/proměnné?


@app.route('/todos')
def get_todos():
    try:
        params = request.args
        if len(params) == 0:
            with open("todos.txt") as f:
                result = f.read()
            return result
        else:
            with open("todos.txt") as f:
                lines = f.readlines()

            for p in params:
                p_value = params.get(p)
                if p in ["date_from", "date_to", "is_done"]:
                    lines = filter_todos(p, p_value, lines)
                elif p == "sort_by" and p_value == "urgency":
                    lines = sort_todos(lines)
                elif p == "count" and p_value.isnumeric():
                    continue
                else:
                    return "Chybné parametry", 400

            if "count" in params:
                lines = head_todos(int(params.get("count")), lines)

            return ''.join(lines)

    except IOError:
        return "Seznam úkolů neexistuje, přidej první úkol", 404


@app.route('/most-urgent')
def get_most_urgent():
    with open("todos.txt") as f:
        lines = f.readlines()

    lines = filter_todos("date_from", "now", lines)
    lines = sort_todos(lines)
    lines = head_todos(1, lines)

    return ''.join(lines) # TODO jak udělat redirect s parametry? nemělo by to obsahovat i filtr na is_done=False?


@app.route('/todo/<item>', methods=['DELETE'])
def delete_item(item):
    try:
        with open("todos.txt", "r") as f:
            lines = f.readlines()

        with open("todos.txt", "w") as f:
            todo_exists = False
            for line in lines:
                identifier = line.strip("\n").split(" ", 1)[0]
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
    return change_is_done_status(item, "True", "todos.txt")


@app.route('/<item>/set-not-done', methods=['PUT'])
def set_not_done(item):
    return change_is_done_status(item, "False", "todos.txt")


def change_is_done_status(item, is_done_value, file):
    try:
        with open(file, "r") as f:
            lines = f.readlines()

        with open(file, "w") as f:
            todo_exists = False

            for line in lines:
                spl = line.split(" ", 3)
                identifier = spl[0]
                deadline = spl[2]
                description = spl[3]

                if identifier == item:
                    todo_exists = True
                    newline = identifier + " " + is_done_value + " " + deadline + " " + description
                    f.write(newline)
                else:
                    f.write(line)

        if todo_exists:
            return '', 204
        else:
            return 'Úkol není na seznamu', 404

    except IOError:
        return 'Seznam úkolů neexistuje, přidej první úkol', 404


def filter_todos(param, value, todos):
    if value == "now":
        value = str(date.today())

    filtered = []

    if param == "date_from":
        for t in todos:
            if t.split(" ", 3)[2] >= value:
                filtered.append(t)
    elif param == "date_to":
        for t in todos:
            if t.split(" ", 3)[2] <= value:
                filtered.append(t)
    else:
        for t in todos:
            if t.split(" ", 3)[1] == value:
                filtered.append(t)

    return filtered


def sort_todos(todos):
    d = {t.split()[2]: t.strip() for t in todos}
    keysort = sorted([k for k in d])
    sorted_todos=[]

    for k in keysort:
        sorted_todos.append(d[k] + '\n')

    return sorted_todos


def head_todos(number_of_todos, todos):
    head = todos[0:number_of_todos]
    return head


if __name__ == '__main__':
    app.run(debug=True)