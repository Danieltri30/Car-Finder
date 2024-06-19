from functools import wraps
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from firebase_admin import auth, credentials
import fire

app = Flask(__name__)
app.secret_key = 'sharanya'

login_manager = LoginManager()
login_manager.init_app(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session or session['user'].get('role') != role:
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@login_manager.user_loader
def load_user(uid):
    current_user = auth.get_user(uid)
    return current_user

@app.route('/', methods=['POST', 'GET'])
def index():
    user = session.get('user')
    user_role = user['role'] if user else None
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
        return render_template('index.html', clist = clist, user_role=user_role)
    else:
        #Otherwise, return the normal home page
        return render_template('index.html', user_role=user_role)

@app.route('/createLogin', methods=['POST', 'GET'])
def createLogin():
    if request.method == 'POST':
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        role = request.form['role']
        
        if password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(str(password1)) < 5:
            flash('Password must be at least 5 characters.', category='error')
        else:
            try:
                user = auth.create_user(
                    email = email,
                    password = password1
                )
            except Exception as e:
                flash('Information is not valid')
                return redirect(url_for('createLogin'))
            auth.set_custom_user_claims(user.uid, {'role': role})
            flash('Account created!', category='success')
            return redirect(url_for('login'))

    return render_template('createLogin.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.get_user_by_email(email)
            session['user'] = {
                'uid': user.uid,
                'email': user.email,
                'role': user.custom_claims.get('role')
            }
        except Exception as e:
            flash('Account does not exist')
            return redirect(url_for('login'))
        if session['user']['role'] == 'Employee':
            return redirect(url_for('homepageEmployee'))
        else:
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/carsPosted', methods=['GET'])
def carsPosted():
    clist = fire.get_all_cars()
    return render_template('carsPosted.html', clist=clist)


@app.route('/addCar', methods=['POST', 'GET'])
@role_required('Employee')
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
        
        if make == "" or model == "" or year == "" or color == "" or mileage == "" or mpg == "" or bstyle == "" or price == "":
            flash("All fields must be filled out.", category='error')
            return redirect(url_for('addCar'))
        else:
            fire.add_car(make, model, year, color, mileage, mpg, tran, fuel, bstyle, cond, price)
            return redirect(url_for('homepageEmployee'))
    else:
        return render_template('addCar.html')


@app.route('/deleteCar', methods=['POST', 'GET'])
@role_required('Employee')
def deleteCar():
    if request.method == 'POST':
        index = request.form['index']
        clist = fire.get_all_cars()
        
        if index == '':
            flash("Please enter a Car Number.", category='error')
            return redirect(url_for('deleteCar', clist=clist))
        elif int(index) < 1 or int(index) > len(clist):
            flash("Invalid Car Number.", category='error')
            return redirect(url_for('deleteCar', clist=clist))
        else:
            index = int(index)
            fire.delete_car(clist[index-1]['ID'])
            clist = fire.get_all_cars()
            return redirect(url_for('deleteCar', clist=clist))
    else:
        clist = fire.get_all_cars()
        return render_template('deleteCar.html', clist=clist)

@app.route('/updateCar', methods=['POST', 'GET'])
@role_required('Employee')
def updateCar():
    if request.method == 'POST':
        index = request.form['index']
        attr = request.form['car_attribute']
        updates = request.form['toupdate']
        clist = fire.get_all_cars()
        
        
        if index == '':
            flash("Please enter a Car Number.", category='error')
            return redirect(url_for('updateCar', clist=clist))
        elif int(index) < 1 or int(index) > len(clist):
            flash("Invalid Car Number.", category='error')
            return redirect(url_for('updateCar', clist=clist))
        else:
            update = dict()
            if attr == "make":
                update['Make'] = updates
            elif attr == "model":
                update['Model'] = updates
            elif attr == "year":
                update['Year'] = updates
            elif attr == "color":
                update['Color'] = updates
            elif attr == "mileage":
                update['Mileage'] = updates
            elif attr == "mpg":
                update['MPG'] = updates
            elif attr == "transmission":
                update['Transmission'] = updates
            elif attr == "fuel_type":
                update['Fuel'] = updates
            elif attr == "type":
                update['Type'] = updates
            elif attr == "noru":
                update['NorU'] = updates
            elif attr == "price":
                update['Price'] = updates
            index = int(index)
            
            fire.update_car(clist[index-1]['ID'], update)
            clist = fire.get_all_cars()
            return redirect(url_for('updateCar', clist=clist))
    else:
        clist = fire.get_all_cars()
        return render_template('updateCar.html', clist=clist)

@app.route('/homepageEmployee', methods=['POST','GET'])
@role_required('Employee')
def homepageEmployee():
    user_role = session['user']['role']
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
        return render_template('homepageEmployee.html', user_role=user_role, clist=clist)
    else:
        return render_template('homepageEmployee.html', user_role=user_role)
        
#Gets role and returns them to their homepage
@app.route('/homepage')
def homepage():
	user_role = session.get('user', {}).get('role')
	if user_role == 'Employee':
		return redirect(url_for('homepageEmployee'))
	else:
		return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
