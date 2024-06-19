#Firebase backened as service
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter, Or, And
#Fetch service account key JSON file contents
cred = credentials.Certificate(r"firestore_serviceAccountKey.json")

#Init app with service account, grant admin privleges 
firebase_admin.initialize_app(cred)

db = firestore.client()

#BELOW WILL BE FUNCTIONS TO DO CRUD WITHIN DATABASE



#CREATE
# will be used to add new cars to DB
def add_car(make, model, year, color, mileage, mpg, transmission, fueltype, bodystyle, noru, price):
    try:
        # Set the database cursor to the document containing all cars in the database
        db_cursor = db.collection('Cars').document()
        
        # Define the new car from parameters passed 
        new_car = {
            'Make': make,
            'Model': model,
            'Year': year,
            'Color': color,
            'Mileage': mileage,
            'MPG': mpg,
            'Transmission': transmission, # Transmission refers to automatic/manual cars
            'Fuel': fueltype,             # Fuel refers to gasoline/electric/hybrid
            'Type': bodystyle,            # Type refers to sedan, coupe, etc.
            'NorU': noru,                 # NorU means "new or used?"
            'Price': price
        }
        
        # Create a new document for the new car containing its fields and information
        db_cursor.set(new_car)
        # Return the id of the document representing the id of the newly added car
        return db_cursor.id
    except Exception as e:
        print(f"Error: unable to add the car to the database. {e}")
        return None
    
#READ
#Will be used to read from database
def get_all_cars():
    cars = (db.collection('Cars').stream()) # Get a reference to every document in the Cars table
    
    carList = []
    for c in cars:           # Transform each car document to a dict containing its fields and data
        car = c.to_dict()
        car['ID'] = c.id     # Add the ID of each car to the dict
        carList.append(car)  # Append all the dicts to a list
        
    if cars:
        return carList       # Return the list of dicts containing the all cars and their data
    else:
        print("No cars found.")
        
def get_car(carID):
    db_cursor = db.collection('Cars').document(carID)
    c = db_cursor.get()      # Get a reference to the particular car document by its ID
    
    if c.exists:             # If its found, turn it into a dictionary
        car = c.to_dict()
        car['ID'] = c.id     # Add it's id to the dict
        return car           # and return the dict containing the car and all of its data
    else:
        print("Car not found.")
          
#UPDATE
#Update specific values within the DB
def update_car(carID, updates):
    car = db.collection('Cars').document(carID)
    try:
        car.update(updates)
        print(f"Car with the id {carID} has successfully been updated with {updates}")
    except Exception as e:
        print(f"Error: Unable to update car. {e}")

#DELETE
#Will be used to delete a car from DB 
def delete_car(carID):
    car = db.collection('Cars').document(carID) 
    try:
        car.delete()
        print(f"Car with the id {carID} has sucessfully been deleted")
    except Exception as e:
        print(f"Error: Unable to delete car.{e}")


def add_user(username, password, perms):
    try:
        # Set the database cursor to the document containing all users in the database
        db_cursor = db.collection('Users').document()
        
        new_user = {
            'Username' : username,
            'Password' : password,
            'Permissions' : perms
        }
        
        # Create a new document for the new user containing its fields and information
        db_cursor.set(new_user)
        # Return the id of the document representing the id of the newly added user
        return db_cursor.id
    except Exception as e:
        print(f"Error: unable to add the user to the database. {e}")
        return None
    
def delete_user(username):
    user = db.collection('User').document(username) 
    try:
        user.delete()
        print(f"User with the username :  {username} has sucessfully been deleted")
    except Exception as e:
        print(f"Error: Unable to delete user.{e}")  


def get_all_users():
    user = (db.collection('Users').stream()) # Get a reference to every document in the Users table
    
    uList = []
    for u in user:           # Transform each user document to a dict containing its fields and data
        us = u.to_dict()
        us['ID'] = u.id     # Add the ID of each user to the dict
        uList.append(us)  # Append all the dicts to a list
        
    if us:
        return uList       # Return the list of dicts containing the all cars and their data
    else:
        print("Error: No users within the database.")

def filter_cars(make, model, year_range, color, mileage_range, mpg_range, tran, bstyle, cond, price_range):
    db_cursor = db.collection('Cars')  # Get a reference to every document in the Cars table

    # filter cars into cars list
    make_filter = FieldFilter("Make", "==",  make)
    model_filter = FieldFilter("Model", "==", model)
    year_low_filter = FieldFilter("Year", ">=", year_range[0])
    year_high_filter = FieldFilter("Year", "<=", year_range[1])
    color_filter = FieldFilter("Color", "==", color)
    mileage_low_filter = FieldFilter("Mileage", ">=", mileage_range[0])
    mileage_high_filter = FieldFilter("Mileage", "<=", mileage_range[1])
    mpg_low_filter = FieldFilter("MPG", ">=", mpg_range[0])
    mpg_high_filter = FieldFilter("MPG", "<=", mpg_range[1])
    trans_filter = FieldFilter("Transmission", "==", tran)
    type_filter = FieldFilter("Type", "==", bstyle)
    cond_filter = FieldFilter("NorU", "==", cond)
    price_low_filter = FieldFilter("Price", ">=", price_range[0])
    price_high_filter = FieldFilter("Price", "<=", price_range[1])

    filters_list = []
    if make != None: filters_list.append(make_filter)
    
    if model != None: filters_list.append(model_filter)
    
    if year_range[0] != year_range[1]:
        filters_list.append(year_low_filter)
        filters_list.append(year_high_filter)
    else:
        filters_list.append(FieldFilter('Year', '>', 0))
        
    if color != None: filters_list.append(color_filter)
    
    if mileage_range[0] != mileage_range[1]:
        filters_list.append(mileage_low_filter)
        filters_list.append(mileage_high_filter)
    else:
        filters_list.append(FieldFilter("Mileage", ">=", 0))

    if mpg_range[0] != mpg_range[1]:
        filters_list.append(mpg_low_filter)
        filters_list.append(mpg_high_filter)
    else:
        filters_list.append(FieldFilter("MPG" , ">" , 0))   

    if tran != "Any":
        filters_list.append(trans_filter)
    else:
        filters_list.append(FieldFilter("Transmission", "in", ["Automatic", "Manual"]))
    
    '''if fuel != "Any":
        filters_list.append(fuel_filter)
    else:
        filters_list.append(FieldFilter("Fuel", "in", ["Electric", "Gasoline", "Hybrid"]))'''

    if bstyle != "Any":
        filters_list.append(type_filter)
    else:
        filters_list.append(FieldFilter("Type", "in", ["Sedan", "Pickup", "SUV" , "Coupe","Roadster", "Convertible"]))
  
    if cond != "Any":
        filters_list.append(cond_filter)
    else:
        filters_list.append(FieldFilter("NorU", "in", ["New", "Used"]))

    if price_range[0] != price_range[1]:
        filters_list.append(price_low_filter)
        filters_list.append(price_high_filter)
    else:
        filters_list.append(FieldFilter("Price", ">=", 0))
    
    master_filter = And(filters=filters_list)

    print("Applied Filters:")
    for f in filters_list:
        print(f.__dict__)

    cars = db_cursor.where(filter=master_filter).stream()

    car_list = []

    '''for c in cars:
        for attr in c:
            if()'''
        
    for c in cars:
        car = c.to_dict()
        car['ID'] = c.id
        car_list.append(car)
    # Returned the results of the query to the front end page as a list of cars with the filter parameters
        
    print("Filtered Cars:")
    for car in car_list:
        print(car)
    return car_list

#END OF CRUD CODE FOR THE LIST OF CARS DATABASE

