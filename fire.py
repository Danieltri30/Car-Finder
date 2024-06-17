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
        car.update({updates})
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
        # Set the database cursor to the document containing all cars in the database
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
        
def filter_cars(make, model, year, color, mileage, mpg, transmission, fueltype, bodystyle, noru, price):
    db_cursor = db.collection('Cars')  # Get a reference to every document in the Cars table

    cond_filt = FieldFilter('NorU', '==', noru)     # First run individual filters on the supplied fields
    tran_filt = FieldFilter('Transmission', '==', transmission)
    fuel_filt = FieldFilter('Fuel', '==', fueltype)

    master_filt = And(filters=[cond_filt, tran_filt, fuel_filt])  # Aggregate them together with an AND filter
    
    # Run the query on that aggregate filter, and stream it to get the filtered cars
    cars = db_cursor.where(filter=master_filt).stream()    
    car_list = []
    for c in cars:
        car = c.to_dict()
        car['ID'] = c.id
        car_list.append(car)
    # Returned the results of the query to the front end page as a list of cars with the filter parameters
    return car_list
#END OF CRUD CODE FOR THE LIST OF CARS DATABASE
