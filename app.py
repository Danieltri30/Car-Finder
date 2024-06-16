from flask import Flask, render_template, request
import fire

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    usage = request.args.get('usage', None)
    transmission = request.args.get('transmission', None)
    fuel = request.args.get('fuel', None)

    # Call filter_cars with query parameters to get filtered car data
    filtered_cars = fire.filter_cars(usage=usage, transmission=transmission, fuel=fuel)

    # Render index.html template and pass filtered car data as clist
    return render_template('index.html', clist=filtered_cars)

@app.route('/createLogin', methods=['POST', 'GET'])
def createLogin():
    if request.method == 'POST':
        return render_template('login.html')
    else:
        return render_template('createLogin.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        return render_template('homepageEmployee.html')
    else:
        return render_template('login.html')


@app.route('/carsPosted', methods=['GET'])
def carsPosted():
    clist = fire.get_all_cars()
    return render_template('carsPosted.html', clist=clist)


@app.route('/addCar', methods=['POST', 'GET'])
def addCar():
    return render_template('addCar.html')


@app.route('/deleteCar', methods=['POST', 'GET'])
def deleteCar():
    return render_template('deleteCar.html')


@app.route('/updateCar', methods=['POST', 'GET'])
def updateCar():
    return render_template('updateCar.html')


if __name__ == "__main__":
    app.run(debug=True)
