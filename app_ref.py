from flask import Flask, request

app_ref = Flask('my-test-app')


@app_ref.route("/")
def ahoj():
    print(request.args)
    return "nazdar!"


@app_ref.route("/nene/")
def nene():
    data = [123, 456, 789, 987, 654]
    poradi = request.args['poradi']
    poradi = int(poradi)

    if poradi < 0 or poradi > len(data) - 1:
        poradi = 0
    try:
        result = str(data[poradi])
    except:
        return "neni v seznamu", 404

    return result


@app_ref.route("/nene2/<item>")
def nene2(item):
    data = [123, 456, 789, 987, 654]
    poradi = int(item)
    try:
        result = str(data[poradi])
    except:
        return "neznam", 404
    return result


@app_ref.route("/testujeme-post", methods=['GET', 'POST'])
def test_post():
    if request.method == 'POST':
        d = request.data.decode()
        print(d)
        return "POST"
    else:
        return "GET"


if __name__ == "__main__":
    app_ref.run()