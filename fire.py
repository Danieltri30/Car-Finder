#FIrebase backened as service
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Fetch service account key JSON file contents
cred = credentials.Certificate("path/to/serviceAccountKey.json")

#Init app with service account, grant admin privleges 
firebase_admin.initialize_app(cred, {
    'databaseURL':'https://carfinder-a7372-default-rtdb.firebaseio.com/' 
    })

#Save 
ref = db.reference('py/')
car_list = ref.child('cars')

#BELOW WILL BE FUNCTIONS TO DO CRUD WITHIN DATABASE


#CREATE
# will be used to add new cars to DB
def add_car(model, color, manufacturer, price, typeof, noru, mileage, mpg, transmission_type, fuel):
    try:
        # Create a new entry in the database and get the unique key
        newcar_ref = car_list.push()
        rkey = newcar_ref.key
        
        # Define the new car with the key included
        new_car = {
            "carID": rkey,
            "model": model,
            "color": color,
            "manufacturer": manufacturer,
            "price": price,
            "typeof": typeof,  # typeof refers to sedan, coupe, etc.
            "noru": noru,  # noru means "new or used?"
            "mileage": mileage,
            "mpg": mpg,
            "transmission_type": transmission_type,  # transmission_type refers to automatic/manual/hybrid car
            "fuel": fuel  # fuel refers to gasoline/electric/hybrid
        }
        
        # Set the new car data to the reference with the unique key
        newcar_ref.set(new_car)
        print(f"New car added with key {rkey}: {new_car}")
        return rkey
    except Exception as e:
        print(f"Error: unable to add the car to the database. {e}")
        return None
    
#READ
#Will be used to read from database
def show_all_cars():
    full_list = car_list.get()
    if full_list:
        for firebasekey,carinfo in full_list.items():
            car_id = carinfo.get("carID","Unkown ID")
            print(f"Car ID:{car_id}")
            for key,value in carinfo.items():
                 print(f"  {key}: {value}")
    else:
        print("No cars found.")

#UPDATE
#Update specific values within the DB
def update_car(carID, updates):
    cref = car_list.child(carID)
    try:
        cref.update(updates)
        print(f"Car with the id {carID} has successfully been updated with {updates}")
    except Exception as e:
        print(f"Error: Unable to update car. {e}")

#DELETE
#Will be used to delete a car from DB 
def deleteCar(carID):
    cref = car_list.child(carID) 
    try:
        cref.delete()
        print(f"Car with the id {carID} has sucessfully been deleted")
    except Exception as e:
        print(f"Error: Unable to delete car.{e}")

#END OF CRUD CODE FOR THE LIST OF CARS DATABASE
