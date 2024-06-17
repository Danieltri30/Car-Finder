from flask import Flask, render_template, request
import fire

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':     # If home page wants to submit the form with fields filled in,
        #make = request.form['make']     # Take in all the fields of the form
        #model = request.form['model']    # Leaving these commented out until the front end's home page fields are sorted out
        #year = request.form['year']
        #color = request.form['color']
        #mileage = request.form['mileage']
        #mpg = request.form['mpg']
        tran = request.form['transmission']
        fuel = request.form['fuel']
        #bstyle = request.form['type']
        cond = request.form['condition']    
        #price = request.form['price']
        
        # Call filter_cars with query parameters to get filtered car data
        clist = fire.filter_cars(None, None, None, None, None, None, tran, fuel, None, cond, None)
        
        # Render index.html template and pass filtered car data as clist
        return render_template('index.html', clist = clist)
    else:
        #Otherwise, return the normal home page
        return render_template('index.html')

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
    if request.method == 'POST':
        make = request.form['make']     # Take in all the fields of the form
        model = request.form['model']    # Leaving these commented out until the front end's home page fields are sorted out
        year = request.form['year']
        color = request.form['color']
        mileage = request.form['mileage']
        mpg = request.form['mpg']
        tran = request.form['transmission']
        fuel = request.form['fuel']
        bstyle = request.form['type']
        cond = request.form['condition']    
        price = request.form['price']
        
        fire.add_car(make, model, year, color, mileage, mpg, tran, fuel, bstyle, cond, price)
        return render_template('homepageEmployee.html')
    else:
        return render_template('addCar.html')


@app.route('/deleteCar', methods=['POST', 'GET'])
def deleteCar():
    if request.method == 'POST':
        return render_template('homepageEmployee.html')
    else:
        clist = fire.get_all_cars()
        return render_template('deleteCar.html', clist=clist)

@app.route('/updateCar', methods=['POST', 'GET'])
def updateCar():
    if request.method == 'POST':
        return render_template('homepageEmployee.html')
    else:
        clist = fire.get_all_cars()
        return render_template('updateCar.html', clist=clist)

if __name__ == "__main__":
    app.run(debug=True)
